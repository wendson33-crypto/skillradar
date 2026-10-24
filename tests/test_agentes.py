# tests/test_agentes.py
# Testes unitários para Agente Extrator e Agente Orientador (com e sem Gemini, schemas e validações anti-alucinação).

import os
import json
import pytest

from Execution.dados import (
    carregar_taxonomia,
    carregar_vagas_demo,
    carregar_competencias_cursos,
    carregar_cursos_areas,
)
from Execution.agentes.matcher import executar_matching_curso
from Execution.agentes.extrator import (
    ExtratorSaida,
    inferir_senioridade,
    pos_validar_competencias,
    executar_extracao_vaga,
    gerar_hash_texto_vaga,
    carregar_cache_extrator,
    salvar_cache_extrator,
)
from Execution.agentes.orientador import (
    Insight,
    ItemTrilha,
    OrientadorSaida,
    extrair_numeros_de_texto,
    coletar_numeros_dos_fatos,
    validar_anti_alucinacao_numerica,
    gerar_plano_b_templates,
    executar_orientador_curso,
)


@pytest.fixture
def taxonomia():
    return carregar_taxonomia("data/taxonomia_competencias.csv")


@pytest.fixture
def vagas_demo():
    return carregar_vagas_demo("data/vagas_demo.csv")


# ==============================================================================
# 1. Testes do Agente Extrator (Plano B, Validação Pydantic e Cache)
# ==============================================================================

def test_inferir_senioridade_padroes():
    # Arrange & Act & Assert
    assert inferir_senioridade("Estagiário de Desenvolvimento", "HTML e CSS") == "estagio"
    assert inferir_senioridade("Desenvolvedor Frontend Jr", "React e JS") == "junior"
    assert inferir_senioridade("Analista de Dados Pleno", "Python e SQL") == "pleno"
    assert inferir_senioridade("Engenheiro de Software Sênior", "Arquitetura Cloud") == "senior"
    assert inferir_senioridade("Programador", "Sem nível informado") == "nao_informado"


def test_extrator_pos_validacao_rejeita_termos_inventados(taxonomia):
    # Arrange
    competencias_recebidas = ["JavaScript", "Docker", "TecnologiaInventada", "Python", "SuperFrameworkInexistente"]
    nao_mapeadas_iniciais = ["LinguagemZ"]

    # Act
    validas, nao_mapeadas = pos_validar_competencias(
        competencias_recebidas,
        nao_mapeadas_iniciais,
        taxonomia,
    )

    # Assert
    assert "JavaScript" in validas
    assert "Docker" in validas
    assert "Python" in validas
    assert "TecnologiaInventada" not in validas
    assert "SuperFrameworkInexistente" not in validas

    # Termos não pertencentes à taxonomia são realocados para nao_mapeadas
    assert "TecnologiaInventada" in nao_mapeadas
    assert "SuperFrameworkInexistente" in nao_mapeadas
    assert "LinguagemZ" in nao_mapeadas


def test_extrator_reproduz_esperadas_nas_30_vagas_demo(taxonomia, vagas_demo):
    # Arrange & Act
    for _, row in vagas_demo.iterrows():
        esperadas = [c.strip() for c in str(row["competencias_esperadas"]).split("|") if c.strip()]
        vaga_dict = row.to_dict()

        res = executar_extracao_vaga(
            vaga=vaga_dict,
            mapa_taxonomia=taxonomia,
            sem_gemini=True,
        )

        # Assert
        assert isinstance(res, ExtratorSaida)
        assert set(res.competencias) == set(esperadas), (
            f"Vaga {row['vaga_id']}: esperado {esperadas}, obteve {res.competencias}"
        )


def test_extrator_cache_em_arquivo(tmp_path, taxonomia):
    # Arrange
    caminho_cache_teste = str(tmp_path / "cache_teste.json")
    vaga_mock = {
        "vaga_id": "V_TESTE",
        "titulo": "Desenvolvedor Backend Exemplo",
        "requisitos_texto": "Conhecimento em Python e Docker.",
        "senioridade": "pleno",
    }

    # Act 1: Primeira execução gera cache
    res1 = executar_extracao_vaga(
        vaga=vaga_mock,
        mapa_taxonomia=taxonomia,
        sem_gemini=True,
        caminho_cache=caminho_cache_teste,
    )

    # Assert 1
    assert os.path.exists(caminho_cache_teste)
    cache = carregar_cache_extrator(caminho_cache_teste)
    hash_vaga = gerar_hash_texto_vaga(vaga_mock["titulo"], vaga_mock["requisitos_texto"])
    assert hash_vaga in cache

    # Act 2: Segunda execução lê do cache
    res2 = executar_extracao_vaga(
        vaga=vaga_mock,
        mapa_taxonomia=taxonomia,
        sem_gemini=True,
        caminho_cache=caminho_cache_teste,
    )

    # Assert 2
    assert res1.competencias == res2.competencias
    assert res1.senioridade == res2.senioridade


# ==============================================================================
# 2. Testes do Agente Orientador (Templates, Anti-alucinação e Schemas)
# ==============================================================================

def test_orientador_extracao_e_validacao_numerica():
    # Arrange
    fatos_exemplo = {
        "amostra_n": 17,
        "aderencia_antes_pct": 68.1,
        "aderencia_depois_pct": 76.4,
        "trilha_base": [
            {"modulo": "M1", "curso": "C1", "carga_horaria": 12, "peso": 4},
            {"modulo": "M2", "curso": "C1", "carga_horaria": 16, "peso": 2},
        ],
    }

    # Act
    nums_permitidos = coletar_numeros_dos_fatos(fatos_exemplo)

    # Assert
    assert 17.0 in nums_permitidos
    assert 68.1 in nums_permitidos
    assert 76.4 in nums_permitidos
    assert 12.0 in nums_permitidos
    assert 16.0 in nums_permitidos
    assert 2.0 in nums_permitidos  # len(trilha_base)

    # Texto legítimo com números dos fatos
    texto_legitimo = "Os 2 módulos da trilha elevam a aderência de 68,1% para 76,4% em 17 vagas."
    assert validar_anti_alucinacao_numerica(texto_legitimo, nums_permitidos) is True

    # Texto com número inventado (alucinado)
    texto_alucinado = "Os 2 módulos garantem aumento salarial de 95% para os alunos."
    assert validar_anti_alucinacao_numerica(texto_alucinado, nums_permitidos) is False


def test_orientador_plano_b_templates_com_dados_reais():
    # Arrange
    df_cursos = carregar_competencias_cursos("data/competencias_cursos.csv")
    tax = carregar_taxonomia("data/taxonomia_competencias.csv")
    df_vagas = carregar_vagas_demo("data/vagas_demo.csv")
    df_cursos_areas = carregar_cursos_areas("data/cursos_areas.csv")

    from Execution.dados import calcular_area_principal_vaga

    mapa_tax = dict(
        zip(
            tax["competencia_padrao"].str.strip(),
            tax["area"].str.strip(),
        )
    )
    vagas_com_area = []
    for _, v in df_vagas.iterrows():
        comps = [c.strip() for c in v["competencias_esperadas"].split("|") if c.strip()]
        area = calcular_area_principal_vaga(comps, comp_area_map=mapa_tax)
        item = v.to_dict()
        item["area"] = area
        item["competencias"] = comps
        vagas_com_area.append(item)

    resultado_matcher = executar_matching_curso(
        curso="Técnico em Desenvolvimento de Sistemas",
        df_cursos=df_cursos,
        df_taxonomia=tax,
        df_cursos_areas=df_cursos_areas,
        vagas_com_area=vagas_com_area,
    )

    fatos = {
        "curso": resultado_matcher["curso"],
        "amostra_n": resultado_matcher["amostra_n"],
        "lacunas": resultado_matcher["lacunas"][:5],
        "sem_modulo": resultado_matcher["sem_modulo"],
        "trilha_base": resultado_matcher["trilha_base"],
        "aderencia_antes_pct": resultado_matcher["aderencia_antes_pct"],
        "aderencia_depois_pct": resultado_matcher["aderencia_depois_pct"],
    }

    # Act
    saida = executar_orientador_curso(fatos, sem_gemini=True)

    # Assert
    assert isinstance(saida, OrientadorSaida)
    assert len(saida.insights) <= 3
    assert len(saida.trilha) == 3

    # Todos os insights devem ter origem="template" no modo sem gemini
    for ins in saida.insights:
        assert ins.origem == "template"
        assert len(ins.texto) <= 280
        assert ins.titulo

    # A trilha deve conter exatamente os 3 módulos da trilha-base oficial
    modulos_esperados = [
        "Banco Realtime NoSQL",
        "CI/CD e Deploy em Nuvem",
        "Multi-agentes e Gemini API",
    ]
    modulos_obtidos = [item.modulo for item in saida.trilha]
    assert modulos_obtidos == modulos_esperados

    # Verifica se os campos determinísticos foram preservados
    for item in saida.trilha:
        assert item.carga_horaria in (12, 16)
        assert item.peso is not None
        assert len(item.competencias_cobertas) > 0


def test_orientador_rejeita_modulo_inventado_e_aciona_fallback():
    # Arrange: simula fatos válidos
    fatos = {
        "curso": "Qualificação em IA Generativa",
        "amostra_n": 24,
        "lacunas": [{"competencia": "SQL", "frequencia": 13}],
        "sem_modulo": [],
        "trilha_base": [
            {"curso": "Curso A", "modulo": "Modulo Real", "carga_horaria": 20, "competencias_cobertas": ["SQL"], "peso": 13}
        ],
        "aderencia_antes_pct": 31.4,
        "aderencia_depois_pct": 50.0,
    }

    # Act: no modo sem_gemini aciona templates seguros
    saida = executar_orientador_curso(fatos, sem_gemini=True)

    # Assert
    modulos_na_saida = [item.modulo for item in saida.trilha]
    assert modulos_na_saida == ["Modulo Real"]
    assert "Modulo Inventado Pelo Modelo" not in modulos_na_saida
