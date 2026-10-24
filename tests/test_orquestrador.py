# tests/test_orquestrador.py
# Testes unitários para o Orquestrador CLI central e integração determinística de 3 camadas.

import json
import os
import pytest

from Execution.orquestrador import (
    gerar_slug,
    sanitizar_para_firestore,
    executar_pipeline,
)


def test_gerar_slug_normalizacao():
    # Arrange & Act & Assert
    assert gerar_slug("Técnico em Desenvolvimento de Sistemas") == "tecnico-em-desenvolvimento-de-sistemas"
    assert gerar_slug("Qualificação em IA Generativa") == "qualificacao-em-ia-generativa"
    assert gerar_slug("Análise & Ciência de Dados / Big Data") == "analise-ciencia-de-dados-big-data"
    assert gerar_slug("   Espaços   Múltiplos   ") == "espacos-multiplos"


def test_sanitizar_para_firestore_remove_nan_e_infinity():
    # Arrange
    dados_com_problemas = {
        "normal": 42.5,
        "nulo": None,
        "invalido_nan": float("nan"),
        "invalido_inf": float("inf"),
        "lista": [10, float("nan"), 20],
        "submapa": {
            "valor": float("-inf"),
            "texto": "ok",
        },
    }

    # Act
    sanitizado = sanitizar_para_firestore(dados_com_problemas)

    # Assert
    assert sanitizado["normal"] == 42.5
    assert sanitizado["invalido_nan"] is None
    assert sanitizado["invalido_inf"] is None
    assert sanitizado["lista"] == [10, None, 20]
    assert sanitizado["submapa"]["valor"] is None
    assert sanitizado["submapa"]["texto"] == "ok"


def test_executar_pipeline_dry_run_completo_e_tabela_referencia(tmp_path):
    # Arrange
    pasta_temp_teste = str(tmp_path / "temp_teste")

    # Act
    resultado = executar_pipeline(
        modo="demo",
        sem_gemini=True,
        dry_run=True,
        pasta_temp=pasta_temp_teste,
    )

    # Assert
    assert resultado["sucesso"] is True
    assert resultado["modo_demo"] is True
    assert resultado["arquivo_dry_run"] is not None
    assert os.path.exists(resultado["arquivo_dry_run"])

    # Carrega o payload gerado e valida estrutura e coleções
    with open(resultado["arquivo_dry_run"], "r", encoding="utf-8") as f:
        payload = json.load(f)

    assert "contexto" in payload
    assert "vagas_ativas" in payload
    assert "lacunas_cursos" in payload
    assert "trilhas_sugeridas" in payload
    assert "insights" in payload
    assert "competencias_demandadas" in payload

    # 1. Validação de Vagas e Contexto
    assert len(payload["vagas_ativas"]) == 30
    assert payload["contexto"]["atual"]["total_vagas"] == 30
    assert payload["contexto"]["atual"]["modo_demo"] is True

    # 2. Validação da Tabela Oficial de Referência (Directives/agentes/agentes.md §8)
    lacunas = payload["lacunas_cursos"]
    assert len(lacunas) == 4

    # Técnico em Desenvolvimento de Sistemas
    tds = lacunas["tecnico-em-desenvolvimento-de-sistemas"]
    assert tds["amostra_n"] == 17
    assert tds["cobertura_pct"] == 48.6
    assert tds["cobertura_ponderada_pct"] == 66.4
    assert tds["kpis"]["salario_mediano"] == 5250
    assert tds["kpis"]["salario_n"] == 16

    # Qualificação em IA Generativa
    ia = lacunas["qualificacao-em-ia-generativa"]
    assert ia["amostra_n"] == 24
    assert ia["cobertura_pct"] == 31.4
    assert ia["cobertura_ponderada_pct"] == 29.7

    # Qualificação em Análise de Dados
    dados = lacunas["qualificacao-em-analise-de-dados"]
    assert dados["amostra_n"] == 7
    assert dados["cobertura_pct"] == 47.8
    assert dados["cobertura_ponderada_pct"] == 65.9

    # Qualificação em Infraestrutura e Nuvem
    infra = lacunas["qualificacao-em-infraestrutura-e-nuvem"]
    assert infra["amostra_n"] == 6
    assert infra["cobertura_pct"] == 43.8
    assert infra["cobertura_ponderada_pct"] == 62.9

    # 3. Validação de Trilhas e Insights
    trilhas = payload["trilhas_sugeridas"]
    assert len(trilhas) == 4
    tds_trilha = trilhas["tecnico-em-desenvolvimento-de-sistemas"]
    assert len(tds_trilha["modulos"]) == 3
    assert tds_trilha["aderencia_antes_pct"] == 68.1
    assert tds_trilha["aderencia_depois_pct"] == 76.4

    # 4. Validação de IDs e Escopos de Insights
    insights = payload["insights"]
    assert len(insights) > 0
    for doc_id, ins in insights.items():
        assert doc_id.startswith("coordenacao-")
        assert ins["origem"] in ("template", "gemini")
        assert len(ins["texto"]) <= 280
