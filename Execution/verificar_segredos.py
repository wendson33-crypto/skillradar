"""Script de verificação automática de segredos e credenciais.

Examina os arquivos do projeto para garantir que nenhuma chave do Gemini,
token do GitHub ou chave privada de conta de serviço seja versionada.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# Padrões de segredos proibidos
PADROES_PROIBIDOS: list[tuple[str, re.Pattern[str]]] = [
    (
        "Chave Web Firebase (fora de docs/js/config.js)",
        re.compile(r"AIza[0-9A-Za-z_\-]{35}"),
    ),
    (
        "Token Pessoal do GitHub (ghp_)",
        re.compile(r"ghp_[0-9A-Za-z]{36}"),
    ),
    (
        "Token Fine-Grained do GitHub (github_pat_)",
        re.compile(r"github_pat_[0-9A-Za-z_]{40,}"),
    ),
    (
        "Chave Privada de Conta de Serviço (BEGIN PRIVATE KEY)",
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ),
    (
        "Campo de Chave Privada em JSON",
        re.compile(r'"private_key"\s*:'),
    ),
    (
        "Chave Gemini com valor atribuído",
        re.compile(r"GEMINI_API_KEY\s*=\s*[\"']?[A-Za-z0-9_\-]{10,}[\"']?"),
    ),
]

# Diretórios e extensões ignorados por padrão
IGNORAR_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".temp",
    ".vercel",
}

IGNORAR_EXTENSOES = {
    ".pyc",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".pdf",
    ".zip",
    ".lock",
}

# Arquivos específicos e padrões ignorados pelo .gitignore
IGNORAR_ARQUIVOS_EXATOS = {
    ".env",
    "mcp_config.json",
}

IGNORAR_PREFIXOS_NOMES = (
    "serviceAccount",
    ".env.",
)

IGNORAR_SUFIXOS_NOMES = (
    "-sa.json",
    ".json.key",
)


def caminho_ignorado(caminho_rel: Path) -> bool:
    """Verifica se o caminho está dentro de diretórios ou arquivos ignorados pelo .gitignore."""
    partes = caminho_rel.parts
    for parte in partes:
        if parte in IGNORAR_DIRS:
            return True
        if parte.startswith(".venv") or parte == "venv":
            return True

    if caminho_rel.suffix.lower() in IGNORAR_EXTENSOES:
        return True

    nome = caminho_rel.name
    if nome in IGNORAR_ARQUIVOS_EXATOS:
        return True

    for prefixo in IGNORAR_PREFIXOS_NOMES:
        if nome.startswith(prefixo) and nome != ".env.example":
            return True

    for sufixo in IGNORAR_SUFIXOS_NOMES:
        if nome.endswith(sufixo):
            return True

    return False


def verificar_conteudo(
    conteudo: str, caminho_rel: Path
) -> list[tuple[int, str]]:
    """Verifica um texto contra os padrões proibidos, retornando (linha, tipo_erro)."""
    violacoes: list[tuple[int, str]] = []
    caminho_str = str(caminho_rel).replace("\\", "/")

    # Exceção permitida pelo design: docs/js/config.js pode conter AIza
    eh_firebase_config = caminho_str.endswith("docs/js/config.js")

    # Arquivo .env.example vazio é permitido
    eh_env_example = caminho_rel.name == ".env.example"

    # Na diretiva de segurança, a tabela de documentação exemplifica os padrões
    eh_doc_seguranca = caminho_str.endswith("Directives/seguranca/seguranca.md")

    for i, linha in enumerate(conteudo.splitlines(), start=1):
        # Ignora linhas da tabela de definição de padrões na diretiva de segurança
        if eh_doc_seguranca and linha.strip().startswith("|"):
            continue

        for desc, padrao in PADROES_PROIBIDOS:
            if eh_firebase_config and ("Firebase" in desc or "AIza" in desc):
                continue

            if eh_env_example and "GEMINI_API_KEY" in desc:
                continue

            if padrao.search(linha):
                violacoes.append((i, desc))

    return violacoes


def verificar_arquivo(caminho: Path, raiz: Path) -> list[tuple[Path, int, str]]:
    """Verifica um arquivo individual."""
    rel = caminho.relative_to(raiz)
    if caminho_ignorado(rel):
        return []

    try:
        conteudo = caminho.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    violacoes = verificar_conteudo(conteudo, rel)
    return [(rel, num_linha, desc) for num_linha, desc in violacoes]


def escanear_projeto(raiz: Path) -> list[tuple[Path, int, str]]:
    """Percorre recursivamente os arquivos do projeto buscando segredos."""
    todas_violacoes: list[tuple[Path, int, str]] = []

    for caminho_arquivo in raiz.rglob("*"):
        if caminho_arquivo.is_file():
            violacoes = verificar_arquivo(caminho_arquivo, raiz)
            todas_violacoes.extend(violacoes)

    return todas_violacoes


def main() -> int:
    """Execução principal do script de verificação."""
    raiz = Path(__file__).resolve().parent.parent
    violacoes = escanear_projeto(raiz)

    if not violacoes:
        print("[OK] Nenhum segredo detectado nos arquivos do projeto.")
        return 0

    print(
        f"[ERRO DE SEGURANÇA] {len(violacoes)} potencial(is) segredo(s) encontrado(s):"
    )
    for rel, linha, desc in violacoes:
        # Importante: nunca exibe o valor secreto, apenas arquivo, linha e tipo
        print(f"  - {rel}:{linha} -> {desc}")

    print("\nCorrija as violações antes de efetuar commits ou deploys.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
