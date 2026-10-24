"""Suite de testes do Agente Matcher determinístico (Etapa 2).

Valida integralmente os critérios de aceite e números de referência
definidos em Directives/agentes/agentes.md §5 e §8:
- Caso pequeno com cálculos manuais
- Tabela oficial de referência para os 4 cursos
- Trilha-base gulosa, cargas horárias e saltos de aderência
- Cálculo de salário mediano e pontos médios por área
- Conformidade estrutural dos dados de gráficos (Plotly/Firestore)
"""

from __future__ import annotations

import pytest

from Execution.dados import (
    carregar_competencias_cursos,
    carregar_cursos_areas,
    carregar_taxonomia,
    carregar_vagas_demo,
    calcular_area_principal_vaga,
)
from Execution.agentes.matcher import (
    calcular_aderencia_vaga,
    calcular_trilha_base,
    calcular_salario_mediano,
    calcular_salario_por_area,
    executar_matching_curso,
)


@pytest.fixture(scope="module")
def ambiente_dados():
    df_cursos = carregar_competencias_cursos()
    df_taxonomia = carregar_taxonomia()
    df_vagas = carregar_vagas_demo()
    df_cursos_areas = carregar_cursos_areas()

    mapa_tax = dict(
        zip(
            df_taxonomia["competencia_padrao"].str.strip(),
            df_taxonomia["area"].str.strip(),
        )
    )

    vagas_com_area = []
    for _, v in df_vagas.iterrows():
        comps = [
            c.strip()
            for c in v["competencias_esperadas"].split("|")
            if c.strip()
        ]
        area = calcular_area_principal_vaga(comps, comp_area_map=mapa_tax)
        item = v.to_dict()
        item["area"] = area
        item["competencias"] = comps
        vagas_com_area.append(item)

    return {
        "df_cursos": df_cursos,
        "df_taxonomia": df_taxonomia,
        "df_cursos_areas": df_cursos_areas,
        "vagas_com_area": vagas_com_area,
    }


def test_matcher_caso_pequeno():
    """Valida o caso pequeno com valores calculados à mão (agentes.md §8):

    - 3 vagas: {SQL, Docker}, {SQL, Python, Docker, Docker}, {Docker}
    - Curso ensina SQL e Python
    - cobertura_pct == 66.7
    - cobertura_ponderada_pct == 50.0
    - lacuna única Docker: freq 3, pct_vagas 100.0
    """
    vagas_pequenas = [
        {"area": "desenvolvimento", "competencias": ["SQL", "Docker"]},
        {"area": "desenvolvimento", "competencias": ["SQL", "Python", "Docker", "Docker"]},
        {"area": "desenvolvimento", "competencias": ["Docker"]},
    ]

    import pandas as pd
    df_cursos_fake = pd.DataFrame(
        [
            {"curso": "Curso Teste", "modulo": "Mod 1", "competencia": "SQL", "carga_horaria": "40"},
            {"curso": "Curso Teste", "modulo": "Mod 2", "competencia": "Python", "carga_horaria": "40"},
        ]
    )
    df_tax_fake = pd.DataFrame(
        [
            {"competencia_padrao": "SQL", "sinonimos": "sql", "area": "dados"},
            {"competencia_padrao": "Python", "sinonimos": "python", "area": "desenvolvimento"},
            {"competencia_padrao": "Docker", "sinonimos": "docker", "area": "infraestrutura"},
        ]
    )
    df_ca_fake = pd.DataFrame(
        [{"curso": "Curso Teste", "area_foco": "desenvolvimento"}]
    )

    resultado = executar_matching_curso(
        curso="Curso Teste",
        df_cursos=df_cursos_fake,
        df_taxonomia=df_tax_fake,
        df_cursos_areas=df_ca_fake,
        vagas_com_area=vagas_pequenas,
    )

    assert resultado["amostra_n"] == 3
    assert resultado["cobertura_pct"] == 66.7
    assert resultado["cobertura_ponderada_pct"] == 50.0
    assert len(resultado["lacunas"]) == 1
    assert resultado["lacunas"][0]["competencia"] == "Docker"
    assert resultado["lacunas"][0]["frequencia"] == 3
    assert resultado["lacunas"][0]["pct_vagas"] == 100.0


def test_tabela_referencia_desenvolvimento_de_sistemas(ambiente_dados):
    """Valida números do Técnico em Desenvolvimento de Sistemas (agentes.md §8):

    - amostra_n == 17
    - cobertura_pct == 48.6
    - cobertura_ponderada_pct == 66.4
    - Maiores lacunas: TypeScript (4), Firebase (3), Inglês Técnico (3)
    - Trilha-base: Banco Realtime NoSQL (12h), CI/CD e Deploy em Nuvem (12h), Multi-agentes e Gemini API (16h)
    - Aderência média: 68.1 antes, 76.4 depois
    - Salário mediano: 5250 (16 vagas)
    """
    res = executar_matching_curso(
        curso="Técnico em Desenvolvimento de Sistemas",
        df_cursos=ambiente_dados["df_cursos"],
        df_taxonomia=ambiente_dados["df_taxonomia"],
        df_cursos_areas=ambiente_dados["df_cursos_areas"],
        vagas_com_area=ambiente_dados["vagas_com_area"],
    )

    assert res["amostra_n"] == 17
    assert res["cobertura_pct"] == 48.6
    assert res["cobertura_ponderada_pct"] == 66.4

    # Top lacunas
    top_lacunas = [(l["competencia"], l["frequencia"]) for l in res["lacunas"][:3]]
    assert top_lacunas == [("TypeScript", 4), ("Firebase", 3), ("Inglês Técnico", 3)]

    # Trilha-base
    trilha = res["trilha_base"]
    assert len(trilha) == 3
    assert trilha[0]["modulo"] == "Banco Realtime NoSQL"
    assert trilha[0]["carga_horaria"] == 12
    assert trilha[1]["modulo"] == "CI/CD e Deploy em Nuvem"
    assert trilha[1]["carga_horaria"] == 12
    assert trilha[2]["modulo"] == "Multi-agentes e Gemini API"
    assert trilha[2]["carga_horaria"] == 16

    # Aderências e Salário
    assert res["aderencia_antes_pct"] == 68.1
    assert res["aderencia_depois_pct"] == 76.4
    assert res["salario_mediano"] == 5250
    assert res["salario_n"] == 16


def test_tabela_referencia_ia_generativa(ambiente_dados):
    """Valida números da Qualificação em IA Generativa:

    - amostra_n == 24
    - cobertura_pct == 31.4
    - cobertura_ponderada_pct == 29.7
    - Maiores lacunas: SQL (13), APIs REST (10), Docker (10)
    """
    res = executar_matching_curso(
        curso="Qualificação em IA Generativa",
        df_cursos=ambiente_dados["df_cursos"],
        df_taxonomia=ambiente_dados["df_taxonomia"],
        df_cursos_areas=ambiente_dados["df_cursos_areas"],
        vagas_com_area=ambiente_dados["vagas_com_area"],
    )

    assert res["amostra_n"] == 24
    assert res["cobertura_pct"] == 31.4
    assert res["cobertura_ponderada_pct"] == 29.7
    top_lacunas = [(l["competencia"], l["frequencia"]) for l in res["lacunas"][:3]]
    assert top_lacunas == [("SQL", 13), ("APIs REST", 10), ("Docker", 10)]


def test_tabela_referencia_analise_de_dados(ambiente_dados):
    """Valida números da Qualificação em Análise de Dados:

    - amostra_n == 7
    - cobertura_pct == 47.8
    - cobertura_ponderada_pct == 65.9
    - Maiores lacunas: Docker (3), Agentes de IA (1), APIs REST (1)
    """
    res = executar_matching_curso(
        curso="Qualificação em Análise de Dados",
        df_cursos=ambiente_dados["df_cursos"],
        df_taxonomia=ambiente_dados["df_taxonomia"],
        df_cursos_areas=ambiente_dados["df_cursos_areas"],
        vagas_com_area=ambiente_dados["vagas_com_area"],
    )

    assert res["amostra_n"] == 7
    assert res["cobertura_pct"] == 47.8
    assert res["cobertura_ponderada_pct"] == 65.9
    top_lacunas = [(l["competencia"], l["frequencia"]) for l in res["lacunas"][:3]]
    assert top_lacunas == [("Docker", 3), ("Agentes de IA", 1), ("APIs REST", 1)]


def test_tabela_referencia_infraestrutura_e_nuvem(ambiente_dados):
    """Valida números da Qualificação em Infraestrutura e Nuvem:

    - amostra_n == 6
    - cobertura_pct == 43.8
    - cobertura_ponderada_pct == 62.9
    - Maiores lacunas: AWS (2), Infraestrutura como Código (2), Inglês Técnico (2)
    """
    res = executar_matching_curso(
        curso="Qualificação em Infraestrutura e Nuvem",
        df_cursos=ambiente_dados["df_cursos"],
        df_taxonomia=ambiente_dados["df_taxonomia"],
        df_cursos_areas=ambiente_dados["df_cursos_areas"],
        vagas_com_area=ambiente_dados["vagas_com_area"],
    )

    assert res["amostra_n"] == 6
    assert res["cobertura_pct"] == 43.8
    assert res["cobertura_ponderada_pct"] == 62.9
    top_lacunas = [(l["competencia"], l["frequencia"]) for l in res["lacunas"][:3]]
    assert top_lacunas == [("AWS", 2), ("Infraestrutura como Código", 2), ("Inglês Técnico", 2)]


def test_conformidade_estruturas_grafico(ambiente_dados):
    """Verifica se os formatos dos gráficos atendem rigorosamente o front-end e regras do Firestore."""
    res = executar_matching_curso(
        curso="Técnico em Desenvolvimento de Sistemas",
        df_cursos=ambiente_dados["df_cursos"],
        df_taxonomia=ambiente_dados["df_taxonomia"],
        df_cursos_areas=ambiente_dados["df_cursos_areas"],
        vagas_com_area=ambiente_dados["vagas_com_area"],
    )
    graficos = res["graficos"]

    # Radar
    assert "radar" in graficos
    assert len(graficos["radar"]["eixos"]) == 6
    assert len(graficos["radar"]["mercado"]) == 6
    assert len(graficos["radar"]["curso"]) == 6

    # Top Tecnologias
    assert "top_tecnologias" in graficos
    assert len(graficos["top_tecnologias"]["competencias"]) <= 10
    assert len(graficos["top_tecnologias"]["pct"]) == len(graficos["top_tecnologias"]["competencias"])
    assert len(graficos["top_tecnologias"]["cobertas"]) == len(graficos["top_tecnologias"]["competencias"])

    # Vagas por Semana
    assert "vagas_semana" in graficos
    assert len(graficos["vagas_semana"]["semanas"]) > 0
    assert len(graficos["vagas_semana"]["total"]) == len(graficos["vagas_semana"]["semanas"])

    # Matriz (não pode ter arrays aninhados no primeiro nível; usa lista de dicionários com 'valores')
    assert "matriz" in graficos
    assert "competencias" in graficos["matriz"]
    assert "linhas" in graficos["matriz"]
    for linha in graficos["matriz"]["linhas"]:
        assert "modulo" in linha
        assert "valores" in linha
        assert len(linha["valores"]) == len(graficos["matriz"]["competencias"])


def test_salario_por_area(ambiente_dados):
    """Verifica agrupamento de salários por área para gráfico de box plot."""
    sal_area = calcular_salario_por_area(ambiente_dados["vagas_com_area"])
    assert "desenvolvimento" in sal_area
    assert "dados" in sal_area
    assert "infraestrutura" in sal_area
    assert len(sal_area["desenvolvimento"]) == 16
