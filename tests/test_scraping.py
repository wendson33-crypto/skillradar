# tests/test_scraping.py
# Testes unitários para Web Scraping, robots.txt, sanitização de PII, deduplicação e modo demo.

import os
import re
from datetime import datetime, timedelta
import pytest

from Execution.scrapers.base import BaseScraper, USER_AGENT_PADRAO
from Execution.scrapers.fonte_vagas_1 import FonteVagasPortalRegional
from Execution.agentes.coletor import (
    remover_pii,
    limpar_texto_requisitos,
    gerar_vaga_id,
    sanitizar_registro_vaga,
    deduplicar_vagas,
    carregar_vagas_demo_brutas,
    executar_coleta,
    RE_EMAIL,
    RE_TELEFONE,
)

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


# ==============================================================================
# 1. Testes de robots.txt e Governança de Acesso (Sem Rede)
# ==============================================================================

def test_robots_txt_bloqueado_em_memoria():
    # Arrange
    caminho_robots = os.path.join(FIXTURES_DIR, "robots_bloqueado.txt")
    with open(caminho_robots, "r", encoding="utf-8") as f:
        conteudo_robots = f.read()

    scraper = BaseScraper()
    url_proibida = "https://empresa.com.br/vagas/desenvolvedor"

    # Act
    pode = scraper.pode_coletar(url_proibida, robots_txt_content=conteudo_robots)

    # Assert
    assert pode is False, "robots.txt restritivo deve impedir acesso à rota /vagas"
    with pytest.raises(PermissionError):
        scraper.baixar(url_proibida)


def test_robots_txt_permitido_em_memoria():
    # Arrange
    caminho_robots = os.path.join(FIXTURES_DIR, "robots_permitido.txt")
    with open(caminho_robots, "r", encoding="utf-8") as f:
        conteudo_robots = f.read()

    scraper = BaseScraper()
    url_permitida = "https://empresa.com.br/vagas/lista"
    url_proibida = "https://empresa.com.br/admin/dashboard"

    # Act
    pode_vagas = scraper.pode_coletar(url_permitida, robots_txt_content=conteudo_robots)
    pode_admin = scraper.pode_coletar(url_proibida)

    # Assert
    assert pode_vagas is True, "Rota /vagas deve ser permitida"
    assert pode_admin is False, "Rota /admin deve ser bloqueada"


def test_user_agent_padrao_identificado():
    # Arrange & Act
    scraper = BaseScraper()

    # Assert
    assert "SkillRadarBot" in scraper.user_agent
    assert "SENAI Ourinhos" in scraper.user_agent


# ==============================================================================
# 2. Testes de Extração contra Fixture HTML Real (Sem Rede)
# ==============================================================================

def test_extrair_vagas_de_fixture_html():
    # Arrange
    caminho_fixture = os.path.join(FIXTURES_DIR, "pagina_vagas_exemplo.html")
    with open(caminho_fixture, "r", encoding="utf-8") as f:
        html_fixture = f.read()

    scraper = FonteVagasPortalRegional()

    # Act
    vagas = scraper.extrair(html_fixture)

    # Assert
    assert len(vagas) == 3, f"Deveria ter extraído 3 vagas, obteve {len(vagas)}"

    vaga1 = vagas[0]
    assert vaga1["titulo"] == "Desenvolvedor Front-end React"
    assert vaga1["empresa"] == "OurinhoTech Soluções"
    assert vaga1["cidade"] == "Ourinhos/SP"
    assert vaga1["salario_min"] == 4000
    assert vaga1["salario_max"] == 6000
    assert vaga1["data"] == "2026-10-23"
    assert vaga1["fonte_url"].endswith("/vagas/detalhes/101")

    vaga2 = vagas[1]
    assert vaga2["titulo"] == "Analista de Suporte e Redes"
    assert vaga2["empresa"] == "Conecta Vale Telecom"
    assert vaga2["salario_min"] is None, "Salário 'A combinar' deve ser None"
    assert vaga2["salario_max"] is None, "Salário 'A combinar' deve ser None"
    assert vaga2["fonte_url"] == "https://externo.com/vagas/202"

    vaga3 = vagas[2]
    assert vaga3["titulo"] == "Desenvolvedor Backend Python Pleno"
    assert vaga3["salario_min"] == 7500
    assert vaga3["salario_max"] == 7500
    # Data relativa 'há 2 dias'
    data_esperada = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    assert vaga3["data"] == data_esperada


# ==============================================================================
# 3. Testes de Sanitização de PII (LGPD) e Normalização
# ==============================================================================

def test_remocao_rigorosa_de_emails_e_telefones():
    # Arrange
    texto_com_pii = (
        "Vaga para desenvolvedor. Interessados enviar CV para rh@empresa.com.br "
        "ou entrar em contato pelo telefone (14) 99876-5432. "
        "Plantão comercial no +55 14 3302-4000 ou 14 98888-7777. "
        "E-mail alternativo: contato.vagas@sub.dominio.org."
    )

    # Act
    texto_limpo = limpar_texto_requisitos(texto_com_pii)

    # Assert
    assert "rh@empresa.com.br" not in texto_limpo
    assert "contato.vagas@sub.dominio.org" not in texto_limpo
    assert "(14) 99876-5432" not in texto_limpo
    assert "3302-4000" not in texto_limpo
    assert "98888-7777" not in texto_limpo
    assert RE_EMAIL.search(texto_limpo) is None
    assert RE_TELEFONE.search(texto_limpo) is None
    # Mantém conteúdo sem PII
    assert "Vaga para desenvolvedor." in texto_limpo


def test_normalizacao_de_salario_e_nunca_zero():
    # Arrange & Act
    min_combinar, max_combinar = FonteVagasPortalRegional._extrair_salario("A combinar")
    min_faixa, max_faixa = FonteVagasPortalRegional._extrair_salario("R$ 3.500,00 a R$ 5.000,00")
    min_fixo, max_fixo = FonteVagasPortalRegional._extrair_salario("R$ 4.200")
    min_vazio, max_vazio = FonteVagasPortalRegional._extrair_salario(None)
    min_zero, max_zero = FonteVagasPortalRegional._extrair_salario("R$ 0,00")

    # Assert
    assert min_combinar is None and max_combinar is None
    assert min_faixa == 3500 and max_faixa == 5000
    assert min_fixo == 4200 and max_fixo == 4200
    assert min_vazio is None and max_vazio is None
    assert min_zero is None and max_zero is None, "Salário zero deve ser tratado como None"


# ==============================================================================
# 4. Testes de Deduplicação e Identificador Estável
# ==============================================================================

def test_deduplicacao_gera_mesmo_vaga_id_com_variacoes():
    # Arrange
    t1, e1, c1 = "Desenvolvedor Front-End", "Tech Soluções", "Ourinhos/SP"
    t2, e2, c2 = "  desenvolvedor   front-end  ", "TECH SOLUÇÕES", "ourinhos/sp "

    # Act
    id1 = gerar_vaga_id(t1, e1, c1)
    id2 = gerar_vaga_id(t2, e2, c2)

    # Assert
    assert id1 == id2, "Mesma vaga com variações de caixa e espaço deve ter mesmo vaga_id"
    assert len(id1) == 12, "vaga_id deve ter exatamente 12 caracteres (sha1[:12])"


def test_deduplicar_vagas_elimina_duplicatas():
    # Arrange
    vaga_base = {
        "titulo": "Desenvolvedor Python",
        "empresa": "Dados S/A",
        "cidade": "Ourinhos",
        "data": "2026-10-20",
        "salario_min": 5000,
        "salario_max": 7000,
        "requisitos_texto": "Python e SQL.",
    }
    vaga_repetida = {
        "titulo": "  desenvolvedor python  ",
        "empresa": "DADOS S/A",
        "cidade": "ourinhos",
        "data": "2026-10-24",  # Mais recente
        "salario_min": 5000,
        "salario_max": 7000,
        "requisitos_texto": "Python, SQL e Docker.",
    }

    # Act
    resultado = deduplicar_vagas([vaga_base, vaga_repetida])

    # Assert
    assert len(resultado) == 1, "Deveria restar apenas 1 vaga deduplicada"
    assert resultado[0]["data"] == "2026-10-24", "Deve prevalecer o registro mais recente"
    assert "Docker" in resultado[0]["requisitos_texto"]


# ==============================================================================
# 5. Testes de Fallback, Modo Demo e Saída Intermediária
# ==============================================================================

def test_carregar_vagas_demo_brutas_e_ausencia_pii():
    # Arrange & Act
    vagas_demo = carregar_vagas_demo_brutas("data/vagas_demo.csv")

    # Assert
    assert len(vagas_demo) == 30, f"Devem existir 30 vagas demo, encontrou {len(vagas_demo)}"

    for v in vagas_demo:
        assert v["modo_demo"] is True
        assert "vaga_id" in v
        assert len(v["vaga_id"]) == 12
        assert v["titulo"]
        assert v["empresa"]
        assert v["cidade"]
        # Garante ausência total de e-mails ou telefones nos requisitos
        req = v["requisitos_texto"]
        assert "@" not in req, f"Vaga {v['vaga_id']} possui @ em requisitos"
        assert RE_TELEFONE.search(req) is None


def test_executar_coleta_modo_demo_salva_arquivo_intermediario():
    # Arrange
    pasta_temp_teste = ".temp"

    # Act
    resultado = executar_coleta(
        scraper=None,
        modo_demo=True,
        caminho_demo="data/vagas_demo.csv",
        pasta_temp=pasta_temp_teste,
    )

    # Assert
    assert resultado["sucesso"] is True
    assert resultado["modo_demo"] is True
    assert resultado["total"] == 30
    assert os.path.exists(resultado["arquivo_intermediario"])
    assert "vagas_brutas_" in resultado["arquivo_intermediario"]


def test_executar_coleta_fallback_quando_scraper_falha():
    # Arrange: simula um scraper que lança erro de conexão
    class ScraperComFalha(BaseScraper):
        def coletar(self, url=None):
            raise ConnectionError("Rede indisponível (simulação de falha).")

    scraper_falho = ScraperComFalha()

    # Act: tenta executar em modo real, forçando o fallback para demo
    resultado = executar_coleta(
        scraper=scraper_falho,
        modo_demo=False,
        caminho_demo="data/vagas_demo.csv",
    )

    # Assert
    assert resultado["sucesso"] is True
    assert resultado["modo_demo"] is True, "Deve acionar fallback para modo_demo = True"
    assert resultado["total"] == 30
    assert len(resultado["erros"]) > 0
    assert "Rede indisponível" in resultado["erros"][0]
