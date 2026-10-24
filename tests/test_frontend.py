# tests/test_frontend.py
# Validações automatizadas de estrutura, acessibilidade e integridade da interface estática (Etapa 7)

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"

def test_arquivos_estaticos_essenciais_existem():
    """Valida se todos os arquivos obrigatórios da Etapa 7 foram gerados."""
    arquivos_esperados = [
        DOCS / "index.html",
        DOCS / "style.css",
        DOCS / "css" / "tokens.css",
        DOCS / "css" / "app.css",
        DOCS / "js" / "theme-init.js",
        DOCS / "js" / "config.js",
        DOCS / "js" / "theme.js",
        DOCS / "js" / "views.js",
        DOCS / "js" / "charts.js",
        DOCS / "js" / "firebase.js",
        DOCS / "js" / "demo-data.js",
        DOCS / "js" / "app.js",
        DOCS / "data" / "demo_payload.json",
    ]

    for arquivo in arquivos_esperados:
        assert arquivo.exists(), f"Arquivo essencial ausente: {arquivo}"
        assert arquivo.stat().st_size > 0, f"Arquivo vazio: {arquivo}"

def test_ids_obrigatorios_html():
    """Valida a presença de todos os seletores e IDs exigidos pelo Edital e pelas Diretivas."""
    conteudo_html = (DOCS / "index.html").read_text(encoding="utf-8")
    
    ids_obrigatorios = [
        "togglePerfil",
        "tabAluno",
        "tabCoordenacao",
        "selectCurso",
        "liveIndicator",
        "toggleTheme",
        "sidebarNav",
        "navAluno",
        "navCoordenacao",
        "appMain",
        "kpiContainer",
        "kpiVagas",
        "kpiCobertura",
        "kpiLacunas",
        "kpiSalario",
        "iaInsights",
        "viewAluno",
        "perfilSection",
        "formPerfil",
        "perfilNivel",
        "perfilStatus",
        "vagasSection",
        "filtroVagas",
        "inputBuscaVaga",
        "filtroArea",
        "filtroSalario",
        "listaVagas",
        "estadoVazioVagas",
        "aderenciaSection",
        "aderenciaChart",
        "tbodyAderencia",
        "trilhaSection",
        "trilhaAprendizado",
        "trilhaResumo",
        "viewCoordenacao",
        "visualizacaoGraficos",
        "radarChart",
        "tbodyRadar",
        "topTecnologiasChart",
        "tbodyTopTecnologias",
        "salarioChart",
        "tbodySalario",
        "vagasSemanaChart",
        "tbodyVagasSemana",
        "lacunasSection",
        "btnRelatorio",
        "tabelaLacunas",
        "matrizSection",
        "matrizCompetencias",
        "amostraInfo",
        "bottomNav",
    ]
    
    for seletor_id in ids_obrigatorios:
        assert f'id="{seletor_id}"' in conteudo_html, f"ID obrigatório '{seletor_id}' não encontrado em docs/index.html"

def test_acessibilidade_e_semantica_wcag():
    """Valida atributos de acessibilidade WCAG 2.1 AA no HTML."""
    conteudo_html = (DOCS / "index.html").read_text(encoding="utf-8")
    assert '<html lang="pt-BR"' in conteudo_html
    assert 'class="skip-link"' in conteudo_html
    assert 'role="tablist"' in conteudo_html
    assert 'role="tab"' in conteudo_html
    assert 'role="tabpanel"' in conteudo_html
    assert 'aria-controls="viewAluno"' in conteudo_html
    assert 'aria-controls="viewCoordenacao"' in conteudo_html
    assert 'role="region"' in conteudo_html
    assert 'role="status"' in conteudo_html

def test_payload_demo_offline_integro():
    """Valida se o payload offline contém todas as coleções com dados íntegros."""
    caminho_payload = DOCS / "data" / "demo_payload.json"
    dados = json.loads(caminho_payload.read_text(encoding="utf-8"))
    
    assert "contexto" in dados
    assert "atual" in dados["contexto"]
    assert "vagas_ativas" in dados
    assert len(dados["vagas_ativas"]) == 30
    assert "lacunas_cursos" in dados
    assert "tecnico-em-desenvolvimento-de-sistemas" in dados["lacunas_cursos"]
    assert "trilhas_sugeridas" in dados
    assert "tecnico-em-desenvolvimento-de-sistemas" in dados["trilhas_sugeridas"]
