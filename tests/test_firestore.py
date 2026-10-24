# tests/test_firestore.py
# Testes unitários para Firestore Client, validações de arrays, lotes e regras de segurança.

import json
import os
from unittest.mock import MagicMock
import pytest

from Execution.firestore_cliente import (
    tem_arrays_aninhados,
    converter_payload_para_operacoes,
    gravar_lote,
    verificar_configuracao_firebase,
)


def test_tem_arrays_aninhados_detecta_matriz_invalida():
    # Arrange
    dados_validos_mapas = {
        "modulo": "M1",
        "valores": [1, 0, 1],  # Array simples de inteiros é permitido
    }
    dados_invalidos_matriz_z = {
        "z": [[1, 0], [0, 1]],  # Array dentro de array (rejeitado pelo Firestore)
    }

    # Act & Assert
    assert tem_arrays_aninhados(dados_validos_mapas) is False
    assert tem_arrays_aninhados(dados_invalidos_matriz_z) is True


def test_converter_payload_para_operacoes_estruturacao():
    # Arrange
    payload_mock = {
        "contexto": {
            "atual": {"total_vagas": 30, "modo_demo": True},
        },
        "vagas_ativas": {
            "vaga1": {"titulo": "Dev Python", "salario_min": 4000},
        },
        "lacunas_cursos": {
            "tds": {"curso": "Técnico", "cobertura_pct": 50.0},
        },
        "trilhas_sugeridas": {
            "tds": {"curso": "Técnico", "modulos": []},
        },
        "insights": {
            "ins1": {"titulo": "Insight 1", "texto": "Texto"},
        },
        "competencias_demandadas": {
            "python": {"frequencia": 10},
        },
    }

    # Act
    operacoes = converter_payload_para_operacoes(payload_mock)

    # Assert
    assert len(operacoes) == 6
    caminhos = [op[0] for op in operacoes]
    assert "contexto/atual" in caminhos
    assert "vagas_ativas/vaga1" in caminhos
    assert "lacunas_cursos/tds" in caminhos
    assert "trilhas_sugeridas/tds" in caminhos
    assert "insights/ins1" in caminhos
    assert "competencias_demandadas/python" in caminhos


def test_converter_payload_bloqueia_arrays_aninhados():
    # Arrange: payload com matriz bidimensional direta
    payload_invalido = {
        "lacunas_cursos": {
            "curso_erro": {
                "graficos": {
                    "matriz_bidimensional": [[1, 0], [0, 1]],
                }
            }
        }
    }

    # Act & Assert
    with pytest.raises(ValueError, match="arrays aninhados"):
        converter_payload_para_operacoes(payload_invalido)


def test_gravar_lote_divide_em_blocos_de_500():
    # Arrange: cria 1050 operações fictícias
    operacoes_ficticias = [
        (f"colecao/doc_{i}", {"indice": i})
        for i in range(1050)
    ]

    mock_db = MagicMock()
    mock_batch = MagicMock()
    mock_db.batch.return_value = mock_batch

    # Act
    total = gravar_lote(mock_db, operacoes_ficticias, tamanho_lote=500)

    # Assert
    assert total == 1050
    # Deve criar exatamente 3 lotes (500 + 500 + 50)
    assert mock_db.batch.call_count == 3
    assert mock_batch.commit.call_count == 3
    assert mock_batch.set.call_count == 1050


def test_verificar_configuracao_firebase_seguranca():
    # Arrange & Act
    status = verificar_configuracao_firebase()

    # Assert
    assert isinstance(status, dict)
    assert "sdk_instalado" in status
    assert "variavel_credenciais_definida" in status
    assert "arquivo_credenciais_existe" in status
    assert "pronto_para_gravar" in status
    # Nenhuma chave, token ou conteúdo confidencial pode estar exposto
    for v in status.values():
        assert isinstance(v, bool)


def test_firestore_rules_integridade():
    # Arrange
    caminho_rules = "firestore.rules"
    assert os.path.exists(caminho_rules)

    with open(caminho_rules, "r", encoding="utf-8") as f:
        conteudo = f.read()

    # Assert
    assert "rules_version = '2';" in conteudo
    assert "allow write: if false;" in conteudo
    assert "match /interesses_alunos/{id}" in conteudo
    assert "request.resource.data.keys().hasOnly" in conteudo
    assert "allow read: if colecao in" in conteudo
