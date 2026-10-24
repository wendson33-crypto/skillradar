"""Execution/deploy_github.py
Módulo de automação de publicação do SkillRadar no GitHub.

Implementa a criação determinística do repositório público e o envio
atômico de arquivos para a branch main via GitHub REST API, com pré-checagem
de segredos e respeito estrito ao .gitignore e às regras da LGPD.
"""

from __future__ import annotations

import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

from dotenv import dotenv_values
from Execution.verificar_segredos import caminho_ignorado, escanear_projeto


def requisicao_github(
    endpoint: str,
    token: str,
    metodo: str = "GET",
    dados: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Executa requisições autenticadas para a API REST do GitHub."""
    url = f"https://api.github.com{endpoint}" if endpoint.startswith("/") else endpoint
    payload = json.dumps(dados).encode("utf-8") if dados is not None else None

    req = urllib.request.Request(
        url,
        data=payload,
        method=metodo,
        headers={
            "Authorization": f"token {token}",
            "User-Agent": "SkillRadar-Deployer",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            corpo = resp.read().decode("utf-8")
            return json.loads(corpo) if corpo else {}
    except urllib.error.HTTPError as e:
        erro_msg = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Erro na API do GitHub [{e.code}] ({url}): {erro_msg}") from e


def obter_usuario_autenticado(token: str) -> str:
    """Retorna o login do usuário autenticado no GitHub."""
    dados = requisicao_github("/user", token)
    login = dados.get("login")
    if not login:
        raise ValueError("Não foi possível identificar o usuário do GitHub.")
    return login


def garantir_repositorio_publico(usuario: str, repo: str, token: str) -> dict[str, Any]:
    """Cria o repositório público se ele não existir, ou retorna os dados se já existir."""
    try:
        dados = requisicao_github(f"/repos/{usuario}/{repo}", token)
        print(f"[GITHUB] Repositório '{usuario}/{repo}' já existe.")
        return dados
    except RuntimeError as e:
        if "404" not in str(e):
            raise

    print(f"[GITHUB] Criando repositório público '{usuario}/{repo}'...")
    novo_repo = requisicao_github(
        "/user/repos",
        token,
        metodo="POST",
        dados={
            "name": repo,
            "description": "🎯 SkillRadar — Inteligência de Carreira & Alinhamento Curricular - SENAI Ourinhos",
            "private": False,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": False,
            "auto_init": True,
        },
    )
    print(f"[GITHUB] Repositório criado com sucesso: {novo_repo.get('html_url')}")
    return novo_repo


def listar_arquivos_para_publicacao(raiz: Path) -> list[Path]:
    """Coleta todos os arquivos válidos para publicação, ignorando itens protegidos."""
    arquivos: list[Path] = []
    for caminho in raiz.rglob("*"):
        if caminho.is_file():
            rel = caminho.relative_to(raiz)
            if not caminho_ignorado(rel):
                arquivos.append(caminho)
    return sorted(arquivos)


def criar_blob_git(usuario: str, repo: str, token: str, caminho_arquivo: Path) -> str:
    """Envia o conteúdo de um arquivo como um Git Blob e retorna seu SHA."""
    conteudo_bytes = caminho_arquivo.read_bytes()
    b64_content = base64.b64encode(conteudo_bytes).decode("utf-8")

    resposta = requisicao_github(
        f"/repos/{usuario}/{repo}/git/blobs",
        token,
        metodo="POST",
        dados={"content": b64_content, "encoding": "base64"},
    )
    return resposta["sha"]


def publicar_arquivos_atomicamente(
    usuario: str,
    repo: str,
    token: str,
    arquivos: list[Path],
    mensagem_commit: str,
) -> str:
    """Envia todos os arquivos como uma árvore atômica para a branch main."""
    print(f"[DEPLOY] Gerando blobs para {len(arquivos)} arquivos...")
    tree_items: list[dict[str, str]] = []

    for idx, arq in enumerate(arquivos, start=1):
        rel = str(arq.relative_to(RAIZ_PROJETO)).replace("\\", "/")
        sha_blob = criar_blob_git(usuario, repo, token, arq)
        tree_items.append({
            "path": rel,
            "mode": "100644",
            "type": "blob",
            "sha": sha_blob,
        })
        if idx % 20 == 0 or idx == len(arquivos):
            print(f"  - Processados {idx}/{len(arquivos)} arquivos...")

    # Cria a nova árvore
    print("[DEPLOY] Criando árvore do Git (Tree)...")
    res_tree = requisicao_github(
        f"/repos/{usuario}/{repo}/git/trees",
        token,
        metodo="POST",
        dados={"tree": tree_items},
    )
    sha_tree = res_tree["sha"]

    # Obtém o commit pai mais recente da branch main (se houver)
    pais: list[str] = []
    try:
        ref_main = requisicao_github(f"/repos/{usuario}/{repo}/git/ref/heads/main", token)
        sha_commit_pai = ref_main["object"]["sha"]
        pais.append(sha_commit_pai)
    except Exception:
        pass  # Repositório vazio inicializado sem commits

    # Cria o commit
    print(f"[DEPLOY] Criando commit atômico: '{mensagem_commit}'...")
    res_commit = requisicao_github(
        f"/repos/{usuario}/{repo}/git/commits",
        token,
        metodo="POST",
        dados={
            "message": mensagem_commit,
            "tree": sha_tree,
            "parents": pais,
        },
    )
    sha_novo_commit = res_commit["sha"]

    # Atualiza ou cria a referência da branch main
    print("[DEPLOY] Atualizando referência da branch 'main'...")
    try:
        requisicao_github(
            f"/repos/{usuario}/{repo}/git/refs/heads/main",
            token,
            metodo="PATCH",
            dados={"sha": sha_novo_commit, "force": True},
        )
    except Exception:
        requisicao_github(
            f"/repos/{usuario}/{repo}/git/refs",
            token,
            metodo="POST",
            dados={"ref": "refs/heads/main", "sha": sha_novo_commit},
        )

    url_repo = f"https://github.com/{usuario}/{repo}"
    print(f"[DEPLOY CONCLUÍDO] Repositório publicado com sucesso: {url_repo}")
    return url_repo


def executar_deploy(nome_repo: str = "skillradar") -> str:
    """Fluxo orquestrado completo de deploy."""
    print("=" * 60)
    print("[INICIO] DEPLOY AUTOMATIZADO NO GITHUB (ETAPA 9)")
    print("=" * 60)

    # 1. Pré-checagem de segurança
    print("\n[PASSO 1/4] Executando varredura preventiva de segredos...")
    violacoes = escanear_projeto(RAIZ_PROJETO)
    if violacoes:
        print("[ERRO FATAL] Segredos detectados antes do deploy:")
        for rel, linha, desc in violacoes:
            print(f"  - {rel}:{linha} -> {desc}")
        sys.exit(1)
    print("[OK] Pre-checagem de seguranca aprovada (0 segredos).")

    # 2. Leitura do Token
    print("\n[PASSO 2/4] Validando autenticacao GitHub...")
    env_vals = dotenv_values(RAIZ_PROJETO / ".env")
    token = env_vals.get("GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("[ERRO FATAL] Variavel GITHUB_TOKEN nao encontrada no .env!")
        sys.exit(1)

    usuario = obter_usuario_autenticado(token)
    print(f"[OK] Usuario GitHub autenticado: {usuario}")

    # 3. Criação/Verificação do Repositório
    print("\n[PASSO 3/4] Verificando repositorio no GitHub...")
    garantir_repositorio_publico(usuario, nome_repo, token)

    # 4. Upload dos Arquivos
    print("\n[PASSO 4/4] Enviando arquivos do projeto...")
    arquivos = listar_arquivos_para_publicacao(RAIZ_PROJETO)
    print(f"[INFO] {len(arquivos)} arquivos qualificados para publicacao.")

    msg = "feat: inicializacao oficial do SkillRadar com arquitetura de 3 camadas e painel estatico"
    url_publica = publicar_arquivos_atomicamente(usuario, nome_repo, token, arquivos, msg)

    print("\n" + "=" * 60)
    print(f"[SUCESSO] Repositorio publico disponivel em: {url_publica}")
    print("=" * 60)
    return url_publica



if __name__ == "__main__":
    try:
        executar_deploy()
    except Exception as erro:
        print(f"\n[FALHA NO DEPLOY]: {erro}")
        sys.exit(1)
