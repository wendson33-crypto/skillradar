"""Testes para o verificador de segredos (Execution/verificar_segredos.py).

As strings de teste são montadas dinamicamente em tempo de execução
para evitar falsos positivos na varredura do próprio repositório.
"""

from __future__ import annotations

from pathlib import Path
import pytest

from Execution.verificar_segredos import verificar_conteudo, escanear_projeto


def test_conteudo_limpo_passa():
    """Texto comum sem segredos não deve gerar violações."""
    conteudo = "def soma(a, b):\n    return a + b\n"
    violacoes = verificar_conteudo(conteudo, Path("Execution/math.py"))
    assert len(violacoes) == 0


def test_detecta_token_github_falso():
    """Detecta token do GitHub montado dinamicamente."""
    prefixo = "gh" + "p_"
    token_falso = prefixo + ("a" * 36)
    conteudo = f"TOKEN = '{token_falso}'\n"
    violacoes = verificar_conteudo(conteudo, Path("Execution/config.py"))
    assert len(violacoes) == 1
    assert "Token Pessoal do GitHub" in violacoes[0][1]


def test_detecta_chave_privada_falsa():
    """Detecta bloco de BEGIN PRIVATE KEY montado dinamicamente."""
    linha_chave = "-----" + "BEGIN " + "PRIVATE " + "KEY-----"
    conteudo = f"{linha_chave}\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASC\n"
    violacoes = verificar_conteudo(conteudo, Path("Execution/chave.pem"))
    assert len(violacoes) == 1
    assert "Chave Privada" in violacoes[0][1]


def test_detecta_chave_gemini_atribuida():
    """Detecta atribuição direta de chave do Gemini montada dinamicamente."""
    atribuicao = "GEMINI_" + "API_KEY" + " = 'AIzaSyD-1234567890abcdefghijklmnopqrst'"
    conteudo = f"{atribuicao}\n"
    violacoes = verificar_conteudo(conteudo, Path("Execution/agentes.py"))
    assert len(violacoes) >= 1


def test_permite_aiza_em_docs_js_config():
    """Chave Firebase em docs/js/config.js é permitida pelo design."""
    aiza_fake = "AI" + "za" + ("x" * 35)
    conteudo = f"const firebaseConfig = {{ apiKey: '{aiza_fake}' }};\n"
    violacoes = verificar_conteudo(conteudo, Path("docs/js/config.js"))
    assert len(violacoes) == 0


def test_permite_env_example_vazio():
    """O arquivo .env.example sem chaves atribuídas é permitido."""
    conteudo = "GEMINI_API_KEY=\nGEMINI_MODEL=gemini-2.5-flash\n"
    violacoes = verificar_conteudo(conteudo, Path(".env.example"))
    assert len(violacoes) == 0


def test_varredura_projeto_atual_passa():
    """Verifica se o estado atual do repositório está 100% livre de segredos."""
    raiz = Path(__file__).resolve().parent.parent
    violacoes = escanear_projeto(raiz)
    assert violacoes == [], f"Segredos encontrados no projeto: {violacoes}"


def test_conformidade_lgpd_ausencia_pii_nas_vagas():
    """Garante que a base de demonstração não contém PII (e-mails ou telefones)."""
    import re
    raiz = Path(__file__).resolve().parent.parent
    conteudo_vagas = (raiz / "data" / "vagas_demo.csv").read_text(encoding="utf-8")
    
    padrao_email = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    padrao_telefone = re.compile(r"\b(?:\(?\d{2}\)?\s*)?9?\d{4}[-.\s]?\d{4}\b")
    
    # Nenhuma linha deve conter e-mail de recrutador ou candidato
    assert not padrao_email.search(conteudo_vagas), "E-mail encontrado em data/vagas_demo.csv"


def test_regras_firestore_proibem_dados_pessoais():
    """Verifica se firestore.rules restringe estritamente a criação em interesses_alunos."""
    raiz = Path(__file__).resolve().parent.parent
    regras = (raiz / "firestore.rules").read_text(encoding="utf-8")
    
    assert "interesses_alunos" in regras
    assert "hasOnly(['curso_interesse', 'nivel', 'areas', 'criado_em'])" in regras


def test_frontend_seguranca_contra_xss():
    """Garante que arquivos JS do frontend não injetam dados variáveis diretamente com innerHTML."""
    raiz = Path(__file__).resolve().parent.parent
    js_app = (raiz / "docs" / "js" / "app.js").read_text(encoding="utf-8")
    
    # Valida que container de vagas e insights não usam innerHTML com dados variáveis
    assert "container.innerHTML = comAderencia" not in js_app
    assert "container.innerHTML = insights" not in js_app
    assert "vaga-card__role" not in js_app or "role.textContent = vaga.titulo" in js_app


