"""Suite de testes automatizados da camada de dados (Etapa 1).

Cobre integralmente os critérios de aceite de Directives/dados/dados.md §7:
- Integridade estrutural de competencias_cursos.csv
- Consistência e unicidade da taxonomia de competências
- Validação das competências esperadas de vagas_demo.csv
- Correspondência determinística de sinônimos sobre requisitos_texto
- Contagens globais de demanda de mercado
- Determinação da área principal das 30 vagas de demonstração
- Casos de borda (limites de palavras, sobreposição de termos e normalização)
"""

from __future__ import annotations

from collections import Counter
import pytest

from Execution.dados import (
    carregar_competencias_cursos,
    carregar_cursos_areas,
    carregar_taxonomia,
    carregar_vagas_demo,
    normalizar_texto,
    construir_indice_sinonimos,
    extrair_competencias_por_sinonimos,
    calcular_area_principal_vaga,
    calcular_contagens_demanda,
)


@pytest.fixture(scope="module")
def df_cursos():
    return carregar_competencias_cursos()


@pytest.fixture(scope="module")
def df_taxonomia():
    return carregar_taxonomia()


@pytest.fixture(scope="module")
def df_vagas():
    return carregar_vagas_demo()


@pytest.fixture(scope="module")
def df_cursos_areas():
    return carregar_cursos_areas()


def test_competencias_cursos_estrutura(df_cursos):
    """Critério 1: competencias_cursos.csv tem 60 linhas, 33 módulos, 47 competências distintas

    e a carga horária é igual em todas as linhas de um mesmo módulo.
    """
    assert len(df_cursos) == 60, f"Esperado 60 linhas, obteve {len(df_cursos)}"
    assert df_cursos["modulo"].nunique() == 33, f"Esperado 33 módulos, obteve {df_cursos['modulo'].nunique()}"
    assert df_cursos["competencia"].nunique() == 47, f"Esperado 47 competências distintas, obteve {df_cursos['competencia'].nunique()}"

    # Carga horária deve ser consistente dentro de cada módulo
    for modulo, grupo in df_cursos.groupby("modulo"):
        cargas = grupo["carga_horaria"].unique()
        assert len(cargas) == 1, f"Módulo '{modulo}' possui cargas horárias divergentes: {cargas}"


def test_taxonomia_unicidade_e_cobertura_dos_cursos(df_cursos, df_taxonomia):
    """Critério 2: Toda competência de competencias_cursos.csv existe na taxonomia,

    e a taxonomia não tem nomes repetidos.
    """
    # Sem duplicatas na taxonomia
    duplicados = df_taxonomia["competencia_padrao"].duplicated().sum()
    assert duplicados == 0, f"A taxonomia possui {duplicados} nomes repetidos"
    assert len(df_taxonomia) == 61, f"Esperado 61 competências na taxonomia, obteve {len(df_taxonomia)}"

    # Toda competência ensinada deve pertencer à taxonomia oficial
    comps_cursos = set(df_cursos["competencia"].str.strip())
    comps_taxonomia = set(df_taxonomia["competencia_padrao"].str.strip())
    faltantes = comps_cursos - comps_taxonomia
    assert not faltantes, f"Competências dos cursos não encontradas na taxonomia: {faltantes}"


def test_competencias_esperadas_pertencem_a_taxonomia(df_vagas, df_taxonomia):
    """Critério 3: Toda competência da coluna competencias_esperadas existe na taxonomia."""
    comps_taxonomia = set(df_taxonomia["competencia_padrao"].str.strip())
    for _, vaga in df_vagas.iterrows():
        esperadas = [c.strip() for c in vaga["competencias_esperadas"].split("|") if c.strip()]
        for c in esperadas:
            assert c in comps_taxonomia, f"Competência esperada '{c}' na vaga {vaga['vaga_id']} não está na taxonomia"


def test_extracao_sinonimos_bate_com_esperadas_nas_30_vagas(df_vagas, df_taxonomia):
    """Critério 4: Rodando a correspondência de sinônimos sobre requisitos_texto,

    o resultado é IGUAL a competencias_esperadas nas 30 vagas.
    """
    assert len(df_vagas) == 30, f"Esperado 30 vagas de demonstração, obteve {len(df_vagas)}"
    indice = construir_indice_sinonimos(df_taxonomia)

    for _, vaga in df_vagas.iterrows():
        vaga_id = vaga["vaga_id"]
        texto = vaga["requisitos_texto"]
        esperadas = [c.strip() for c in vaga["competencias_esperadas"].split("|") if c.strip()]
        extraidas = extrair_competencias_por_sinonimos(texto, indice_termos=indice)

        assert extraidas == esperadas, (
            f"Vaga {vaga_id} divergiu:\n"
            f"  Esperadas: {esperadas}\n"
            f"  Extraídas: {extraidas}"
        )


def test_contagens_globais_de_demanda(df_vagas):
    """Critério 5: Contagens globais de demanda: SQL 13, Docker 11, APIs REST 10, Kubernetes 4."""
    contagens = calcular_contagens_demanda(df_vagas)
    assert contagens.get("SQL") == 13, f"Esperado SQL 13, obteve {contagens.get('SQL')}"
    assert contagens.get("Docker") == 11, f"Esperado Docker 11, obteve {contagens.get('Docker')}"
    assert contagens.get("APIs REST") == 10, f"Esperado APIs REST 10, obteve {contagens.get('APIs REST')}"
    assert contagens.get("Kubernetes") == 4, f"Esperado Kubernetes 4, obteve {contagens.get('Kubernetes')}"


def test_areas_principais_das_vagas(df_vagas, df_taxonomia):
    """Critério 6: Área principal das vagas bate com a seção 4:

    desenvolvimento 17, dados 6, infraestrutura 6, ia 1.
    """
    mapa_areas = dict(zip(df_taxonomia["competencia_padrao"].str.strip(), df_taxonomia["area"].str.strip()))
    contagem_areas = Counter()

    for _, vaga in df_vagas.iterrows():
        comps = [c.strip() for c in vaga["competencias_esperadas"].split("|") if c.strip()]
        area = calcular_area_principal_vaga(comps, comp_area_map=mapa_areas)
        contagem_areas[area] += 1

    assert contagem_areas["desenvolvimento"] == 17, f"Desenvolvimento: esperado 17, obteve {contagem_areas['desenvolvimento']}"
    assert contagem_areas["dados"] == 6, f"Dados: esperado 6, obteve {contagem_areas['dados']}"
    assert contagem_areas["infraestrutura"] == 6, f"Infraestrutura: esperado 6, obteve {contagem_areas['infraestrutura']}"
    assert contagem_areas["ia"] == 1, f"IA: esperado 1, obteve {contagem_areas['ia']}"


def test_casos_de_borda_extracao(df_taxonomia):
    """Testa casos de borda especificados na diretiva:

    - 'java' não casa em 'javascript'
    - 'react native' casa como 'Desenvolvimento Mobile' e não 'React'
    - 'sql' não casa em 'nosql'
    - 'node.js' não quebra em 'node' e 'js'
    """
    indice = construir_indice_sinonimos(df_taxonomia)

    # 1. Java vs JavaScript
    res_js = extrair_competencias_por_sinonimos("Precisamos de programador JavaScript avançado", indice_termos=indice)
    assert res_js == ["JavaScript"], f"Esperado ['JavaScript'], obteve {res_js}"

    # 2. React Native -> Desenvolvimento Mobile
    res_rn = extrair_competencias_por_sinonimos("Vaga com React Native para mobile", indice_termos=indice)
    assert "Desenvolvimento Mobile" in res_rn
    assert "React" not in res_rn, f"'React' não deve ser casado quando há 'React Native', obteve {res_rn}"

    # 3. SQL vs NoSQL
    res_nosql = extrair_competencias_por_sinonimos("Experiência com NoSQL e MongoDB", indice_termos=indice)
    assert "Banco de Dados NoSQL" in res_nosql
    assert "SQL" not in res_nosql, f"'SQL' não deve casar dentro da palavra 'NoSQL', obteve {res_nosql}"

    # 4. Node.js
    res_node = extrair_competencias_por_sinonimos("Back-end utilizando Node.js e Express", indice_termos=indice)
    assert "Node.js" in res_node


def test_normalizacao_texto():
    """Valida função pura de normalização."""
    assert normalizar_texto("  Acentuação  É Importante! ") == "acentuacao e importante!"
    assert normalizar_texto("") == ""
    assert normalizar_texto("SQL   AVANÇADO\nCOM\tPYTHON") == "sql avancado com python"
