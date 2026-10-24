"""Módulo determinístico de camada de dados e taxonomia do SkillRadar.

Implementa a leitura segura dos CSVs em data/, normalização de texto,
extração de competências por sinônimos e cálculo de área principal de vagas.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Sequence

import pandas as pd

# Ordem fixa de prioridade para desempate na determinação da área da vaga
ORDEM_PRIORIDADE_AREAS: list[str] = [
    "desenvolvimento",
    "dados",
    "ia",
    "infraestrutura",
    "seguranca",
    "design",
    "gestao",
]


def obter_diretorio_dados() -> Path:
    """Retorna o caminho absoluto do diretório data/ do projeto."""
    return Path(__file__).resolve().parent.parent / "data"


def normalizar_texto(texto: str) -> str:
    """Normaliza texto: remove acentos (NFKD), converte para minúsculas e remove espaços extras.

    Exemplo:
        ' Lógica de Programação  ' -> 'logica de programacao'
    """
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    minusculas = sem_acento.lower()
    return re.sub(r"\s+", " ", minusculas).strip()


def carregar_competencias_cursos(caminho: Path | str | None = None) -> pd.DataFrame:
    """Carrega o arquivo competencias_cursos.csv com tratamento de tipos e valores."""
    p = Path(caminho) if caminho else obter_diretorio_dados() / "competencias_cursos.csv"
    df = pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8")
    # Limpeza básica de strings
    for col in df.columns:
        df[col] = df[col].str.strip()
    return df


def carregar_taxonomia(caminho: Path | str | None = None) -> pd.DataFrame:
    """Carrega o arquivo taxonomia_competencias.csv com o vocabulário controlado."""
    p = Path(caminho) if caminho else obter_diretorio_dados() / "taxonomia_competencias.csv"
    df = pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8")
    for col in df.columns:
        df[col] = df[col].str.strip()
    return df


def carregar_vagas_demo(caminho: Path | str | None = None) -> pd.DataFrame:
    """Carrega o arquivo vagas_demo.csv."""
    p = Path(caminho) if caminho else obter_diretorio_dados() / "vagas_demo.csv"
    df = pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8")
    for col in df.columns:
        df[col] = df[col].str.strip()
    return df


def carregar_cursos_areas(caminho: Path | str | None = None) -> pd.DataFrame:
    """Carrega o arquivo cursos_areas.csv com mapeamento de áreas de foco por curso."""
    p = Path(caminho) if caminho else obter_diretorio_dados() / "cursos_areas.csv"
    df = pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8")
    for col in df.columns:
        df[col] = df[col].str.strip()
    return df


def construir_indice_sinonimos(taxonomia: pd.DataFrame) -> list[tuple[str, str]]:
    """Gera lista de pares (termo_normalizado, competencia_padrao) ordenada do mais longo ao mais curto."""
    termos_map: list[tuple[str, str]] = []

    for _, row in taxonomia.iterrows():
        comp_padrao = row["competencia_padrao"].strip()
        sinonimos_raw = [s.strip() for s in row["sinonimos"].split("|") if s.strip()]
        
        # Considera tanto o nome padrão quanto todos os sinônimos listados
        todos_termos = {comp_padrao} | set(sinonimos_raw)
        for t in todos_termos:
            t_norm = normalizar_texto(t)
            if t_norm:
                termos_map.append((t_norm, comp_padrao))

    # Ordenar rigorosamente do mais longo para o mais curto
    termos_map.sort(key=lambda item: len(item[0]), reverse=True)
    return termos_map


def extrair_competencias_por_sinonimos(
    texto: str,
    taxonomia: pd.DataFrame | None = None,
    indice_termos: list[tuple[str, str]] | None = None,
) -> list[str]:
    """Extrai competências padronizadas de um texto bruto utilizando correspondência de sinônimos.

    Regras aplicadas conforme Diretiva de Dados §6:
    1. Normalização de texto e termos (sem acentos, minúsculas).
    2. Avaliação dos termos do mais longo para o mais curto.
    3. Substituição do trecho casado no texto de trabalho por espaços para evitar falsos positivos
       (ex.: 'java' não casa dentro de 'javascript'; 'sql' não casa em 'nosql').
    4. Exigência de limites de palavra: (?<![a-z0-9])termo(?![a-z0-9]).
    5. Preservação da ordem de aparecimento no texto.
    """
    if not texto:
        return []

    if indice_termos is None:
        if taxonomia is None:
            taxonomia = carregar_taxonomia()
        indice_termos = construir_indice_sinonimos(taxonomia)

    texto_normalizado = normalizar_texto(texto)
    texto_trabalho = texto_normalizado
    ocorrencias: list[tuple[int, str]] = []

    for termo_norm, comp_padrao in indice_termos:
        padrao = rf"(?<![a-z0-9]){re.escape(termo_norm)}(?![a-z0-9])"
        match = re.search(padrao, texto_trabalho)
        if match:
            ocorrencias.append((match.start(), comp_padrao))
            # Substitui por espaços do mesmo comprimento para preservar índices e limites
            texto_trabalho = re.sub(
                padrao, lambda m: " " * len(m.group(0)), texto_trabalho
            )

    # Ordena pelo índice da primeira ocorrência no texto
    ocorrencias.sort(key=lambda item: item[0])

    competencias_ordenadas: list[str] = []
    for _, comp in ocorrencias:
        if comp not in competencias_ordenadas:
            competencias_ordenadas.append(comp)

    return competencias_ordenadas


def calcular_area_principal_vaga(
    competencias: Sequence[str],
    taxonomia: pd.DataFrame | None = None,
    comp_area_map: dict[str, str] | None = None,
) -> str:
    """Calcula determinísticamente a área principal de uma vaga.

    Regras aplicadas conforme Diretiva de Dados §4:
    1. Mapeia cada competência para a área na taxonomia.
    2. Ignora a área 'geral'.
    3. A área com maior contagem de competências vence.
    4. Em caso de empate: prioridade fixa: desenvolvimento, dados, ia, infraestrutura, seguranca, design, gestao.
    5. Se a vaga possuir apenas competências 'geral', retorna 'geral'.
    """
    if comp_area_map is None:
        if taxonomia is None:
            taxonomia = carregar_taxonomia()
        comp_area_map = dict(
            zip(taxonomia["competencia_padrao"].str.strip(), taxonomia["area"].str.strip())
        )

    contagem_areas = Counter()
    tem_geral = False

    for c in competencias:
        area = comp_area_map.get(c.strip())
        if area:
            if area == "geral":
                tem_geral = True
            else:
                contagem_areas[area] += 1

    if not contagem_areas:
        return "geral" if tem_geral else "desenvolvimento"

    max_qtd = max(contagem_areas.values())
    candidatas = [area for area, qtd in contagem_areas.items() if qtd == max_qtd]

    for area in ORDEM_PRIORIDADE_AREAS:
        if area in candidatas:
            return area

    return candidatas[0]


def calcular_contagens_demanda(vagas: pd.DataFrame | Sequence[dict[str, Any]]) -> dict[str, int]:
    """Calcula a frequência total de demanda por competência a partir das vagas."""
    contador = Counter()
    if isinstance(vagas, pd.DataFrame):
        for _, r in vagas.iterrows():
            comps_raw = r.get("competencias_esperadas", "")
            if comps_raw:
                comps = [c.strip() for c in comps_raw.split("|") if c.strip()]
                for c in comps:
                    contador[c] += 1
    else:
        for v in vagas:
            comps = v.get("competencias")
            if comps is None:
                comps_raw = v.get("competencias_esperadas", "")
                comps = [c.strip() for c in comps_raw.split("|") if c.strip()]
            for c in comps:
                contador[c] += 1
    return dict(contador)
