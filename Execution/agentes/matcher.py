"""Agente Matcher determinístico do SkillRadar.

Compara competências ensinadas pelos cursos técnicos contra a demanda de vagas
de emprego da região, calculando coberturas, lacunas, trilha-base gulosa,
aderência de vagas e estruturas de dados prontas para os gráficos Plotly.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta
from typing import Any, Sequence

import pandas as pd

from Execution.dados import normalizar_texto


def calcular_aderencia_vaga(
    competencias_vaga: Sequence[str],
    competencias_curso: set[str],
) -> float | None:
    """Calcula a aderência percentual de uma vaga ao curso.

    Fórmula: Competências da vaga que o curso ensina ÷ competências da vaga × 100.
    Retorna None (null) se a vaga não tiver competências.
    """
    comps_unicas = list(dict.fromkeys(c.strip() for c in competencias_vaga if c.strip()))
    if not comps_unicas:
        return None
    cobertas = [c for c in comps_unicas if c in competencias_curso]
    return round((len(cobertas) / len(comps_unicas) * 100), 1)


def calcular_trilha_base(
    lacunas_abertas: dict[str, int],
    modulos_base: list[dict[str, Any]],
    limite_modulos: int = 3,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Gera a trilha-base por cobertura gulosa a partir dos módulos existentes no CSV.

    Regras (agentes.md §5):
    - A cada passo, escolhe o módulo da base (de qualquer curso) que cobre o maior peso
      (onde peso = soma das frequências das lacunas ainda abertas).
    - Empate: menor carga horária; depois curso e módulo em ordem alfabética.
    - Para ao atingir limite_modulos ou quando nenhum módulo cobrir lacuna aberta.
    - Lacunas não atendidas por nenhum módulo vão para sem_modulo.
    """
    trilha: list[dict[str, Any]] = []
    comps_atendidas: set[str] = set()

    # Módulos disponíveis indexados por (curso, modulo)
    modulos_agrupados: dict[tuple[str, str], dict[str, Any]] = {}
    for m in modulos_base:
        chave = (m["curso"], m["modulo"])
        if chave not in modulos_agrupados:
            modulos_agrupados[chave] = {
                "curso": m["curso"],
                "modulo": m["modulo"],
                "carga_horaria": int(m["carga_horaria"]),
                "competencias": set(),
            }
        modulos_agrupados[chave]["competencias"].add(m["competencia"])

    modulos_candidatos = list(modulos_agrupados.values())

    for _ in range(limite_modulos):
        melhor_modulo: dict[str, Any] | None = None
        melhor_peso = 0
        melhores_cobertas: list[str] = []

        for mod in modulos_candidatos:
            if any(
                t["curso"] == mod["curso"] and t["modulo"] == mod["modulo"]
                for t in trilha
            ):
                continue

            cobertas = [
                c
                for c in mod["competencias"]
                if c in lacunas_abertas and c not in comps_atendidas
            ]
            peso = sum(lacunas_abertas[c] for c in cobertas)
            if peso <= 0:
                continue

            if melhor_modulo is None:
                melhor_modulo = mod
                melhor_peso = peso
                melhores_cobertas = cobertas
            else:
                ch_melhor = melhor_modulo["carga_horaria"]
                ch_atual = mod["carga_horaria"]

                if peso > melhor_peso:
                    melhor_modulo = mod
                    melhor_peso = peso
                    melhores_cobertas = cobertas
                elif peso == melhor_peso:
                    if ch_atual < ch_melhor:
                        melhor_modulo = mod
                        melhor_peso = peso
                        melhores_cobertas = cobertas
                    elif ch_atual == ch_melhor:
                        chave_atual = (mod["curso"], mod["modulo"])
                        chave_melhor = (
                            melhor_modulo["curso"],
                            melhor_modulo["modulo"],
                        )
                        if chave_atual < chave_melhor:
                            melhor_modulo = mod
                            melhor_peso = peso
                            melhores_cobertas = cobertas

        if melhor_modulo is None or melhor_peso == 0:
            break

        trilha.append(
            {
                "curso": melhor_modulo["curso"],
                "modulo": melhor_modulo["modulo"],
                "carga_horaria": melhor_modulo["carga_horaria"],
                "competencias_cobertas": sorted(melhores_cobertas),
                "peso": melhor_peso,
            }
        )
        for c in melhores_cobertas:
            comps_atendidas.add(c)

    # Identificar lacunas que nenhum módulo da base ensina
    todas_comps_base = {m["competencia"] for m in modulos_base}
    sem_modulo = sorted(
        [c for c in lacunas_abertas if c not in todas_comps_base],
        key=lambda x: normalizar_texto(x),
    )

    return trilha, sem_modulo


def calcular_salario_mediano(vagas_escopo: Sequence[dict[str, Any]]) -> tuple[int | None, int]:
    """Calcula a mediana dos salários médios das vagas que possuem faixa salarial completa."""
    pontos_medios: list[float] = []
    for v in vagas_escopo:
        s_min = str(v.get("salario_min", "")).strip()
        s_max = str(v.get("salario_max", "")).strip()
        if s_min and s_max:
            try:
                v_min = float(s_min)
                v_max = float(s_max)
                pontos_medios.append((v_min + v_max) / 2.0)
            except ValueError:
                continue

    n = len(pontos_medios)
    if n == 0:
        return None, 0

    pontos_medios.sort()
    if n % 2 == 1:
        mediana = pontos_medios[n // 2]
    else:
        mediana = (pontos_medios[n // 2 - 1] + pontos_medios[n // 2]) / 2.0

    return int(round(mediana)), n


def calcular_salario_por_area(vagas: Sequence[dict[str, Any]]) -> dict[str, list[float]]:
    """Agrupa os pontos médios salariais por área para o box plot global."""
    agrupado: dict[str, list[float]] = {}
    for v in vagas:
        area = v.get("area", "")
        s_min = str(v.get("salario_min", "")).strip()
        s_max = str(v.get("salario_max", "")).strip()
        if area and s_min and s_max:
            try:
                pm = (float(s_min) + float(s_max)) / 2.0
                agrupado.setdefault(area, []).append(round(pm, 2))
            except ValueError:
                continue
    return agrupado


def calcular_variacao_semana(
    vagas: Sequence[dict[str, Any]],
    data_referencia: datetime | str | None = None,
) -> dict[str, int]:
    """Calcula a variação semanal por competência: vagas [hoje-6, hoje] menos [hoje-13, hoje-7]."""
    datas_validas: list[datetime] = []
    vagas_com_data: list[tuple[datetime, list[str]]] = []

    for v in vagas:
        d_str = str(v.get("data", "")).strip()
        if d_str:
            try:
                dt = datetime.strptime(d_str, "%Y-%m-%d")
                datas_validas.append(dt)
                comps_val = v.get("competencias", [])
                if isinstance(comps_val, list):
                    comps = [str(c).strip() for c in comps_val if str(c).strip()]
                else:
                    comps = [
                        c.strip()
                        for c in str(comps_val).split("|")
                        if c.strip()
                    ]
                vagas_com_data.append((dt, comps))
            except ValueError:
                continue

    if not datas_validas:
        return {}

    ref_dt = (
        datetime.strptime(data_referencia, "%Y-%m-%d")
        if isinstance(data_referencia, str)
        else data_referencia
    )
    hoje = ref_dt if ref_dt else max(datas_validas)
    fim_sem_atual = hoje
    ini_sem_atual = hoje - timedelta(days=6)
    fim_sem_anterior = hoje - timedelta(days=7)
    ini_sem_anterior = hoje - timedelta(days=13)

    cont_atual = Counter()
    cont_anterior = Counter()

    for dt, comps in vagas_com_data:
        comps_unicas = set(comps)
        if ini_sem_atual <= dt <= fim_sem_atual:
            for c in comps_unicas:
                cont_atual[c] += 1
        elif ini_sem_anterior <= dt <= fim_sem_anterior:
            for c in comps_unicas:
                cont_anterior[c] += 1

    todas_comps = set(cont_atual.keys()) | set(cont_anterior.keys())
    return {c: cont_atual[c] - cont_anterior[c] for c in todas_comps}


def gerar_estruturas_grafico(
    curso: str,
    amostra_n: int,
    demanda: Counter[str],
    comps_curso: set[str],
    lacunas: list[dict[str, Any]],
    vagas_escopo: Sequence[dict[str, Any]],
    modulos_do_curso: list[dict[str, Any]],
) -> dict[str, Any]:
    """Gera os dicionários formatados exatamente como o front-end espera (agentes.md §5)."""
    # 1. Gráfico Radar: 3 mais pedidas ensinadas + 3 maiores lacunas
    ensinadas_demandadas = [
        (c, demanda[c]) for c in demanda if c in comps_curso
    ]
    ensinadas_demandadas.sort(key=lambda x: (-x[1], normalizar_texto(x[0])))
    top3_ensinadas = [c for c, _ in ensinadas_demandadas[:3]]

    top3_lacunas = [l["competencia"] for l in lacunas[:3]]
    eixos = top3_ensinadas + top3_lacunas

    mercado_radar: list[float] = []
    curso_radar: list[float] = []

    for eixo in eixos:
        pct = round((demanda[eixo] / amostra_n * 100), 1) if amostra_n > 0 else 0.0
        mercado_radar.append(pct)
        if eixo in comps_curso:
            curso_radar.append(pct)
        else:
            curso_radar.append(0.0)

    radar = {
        "eixos": eixos,
        "mercado": mercado_radar,
        "curso": curso_radar,
    }

    # 2. Top Tecnologias: até 10 mais pedidas
    todas_ordenadas = sorted(
        demanda.items(), key=lambda x: (-x[1], normalizar_texto(x[0]))
    )
    top10 = todas_ordenadas[:10]
    top_tecnologias = {
        "competencias": [c for c, _ in top10],
        "pct": [
            round((qtd / amostra_n * 100), 1) if amostra_n > 0 else 0.0
            for _, qtd in top10
        ],
        "cobertas": [c in comps_curso for c, _ in top10],
    }

    # 3. Vagas por semana ISO
    contagem_semanas = Counter()
    for v in vagas_escopo:
        d_str = str(v.get("data", "")).strip()
        if d_str:
            try:
                dt = datetime.strptime(d_str, "%Y-%m-%d")
                ano, sem, _ = dt.isocalendar()
                contagem_semanas[f"{ano}-W{sem:02d}"] += 1
            except ValueError:
                continue

    semanas_ordenadas = sorted(contagem_semanas.keys())
    vagas_semana = {
        "semanas": semanas_ordenadas,
        "total": [contagem_semanas[s] for s in semanas_ordenadas],
    }

    # 4. Matriz: colunas = competências demandadas (até 15); linhas = módulos do curso
    comps_matriz = [c for c, _ in todas_ordenadas[:15]]

    # Módulos distintos do curso preservando ordem
    modulos_vistos: list[str] = []
    modulo_para_comps: dict[str, set[str]] = {}
    for m in modulos_do_curso:
        nome_mod = m["modulo"]
        if nome_mod not in modulos_vistos:
            modulos_vistos.append(nome_mod)
            modulo_para_comps[nome_mod] = set()
        modulo_para_comps[nome_mod].add(m["competencia"])

    linhas_matriz = []
    for nome_mod in modulos_vistos:
        comps_mod = modulo_para_comps[nome_mod]
        valores = [1 if c in comps_mod else 0 for c in comps_matriz]
        linhas_matriz.append({"modulo": nome_mod, "valores": valores})

    matriz = {
        "competencias": comps_matriz,
        "linhas": linhas_matriz,
    }

    return {
        "radar": radar,
        "top_tecnologias": top_tecnologias,
        "vagas_semana": vagas_semana,
        "matriz": matriz,
    }


def executar_matching_curso(
    curso: str,
    df_cursos: pd.DataFrame,
    df_taxonomia: pd.DataFrame,
    df_cursos_areas: pd.DataFrame,
    vagas_com_area: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    """Executa a análise completa de matching determinístico para um curso específico."""
    # 1. Identificar áreas de foco do curso
    areas_foco = set(
        df_cursos_areas[df_cursos_areas["curso"] == curso]["area_foco"].str.strip()
    )

    # 2. Filtrar vagas no escopo do curso
    vagas_escopo = [v for v in vagas_com_area if v.get("area") in areas_foco]
    amostra_n = len(vagas_escopo)

    # 3. Mapear competências do curso
    sub_curso = df_cursos[df_cursos["curso"] == curso]
    comps_curso = set(sub_curso["competencia"].str.strip())
    modulos_do_curso = sub_curso.to_dict(orient="records")

    # Módulos de toda a base (de qualquer curso) para a trilha
    todos_modulos_base = df_cursos.to_dict(orient="records")

    # Mapeamento de taxonomia (competência -> área)
    comp_area_map = dict(
        zip(
            df_taxonomia["competencia_padrao"].str.strip(),
            df_taxonomia["area"].str.strip(),
        )
    )

    # 4. Apurar demanda no escopo
    demanda = Counter()
    vagas_formatadas_aderencia: list[dict[str, Any]] = []

    for v in vagas_escopo:
        raw_comps = v.get("competencias", [])
        if isinstance(raw_comps, str):
            comps = [c.strip() for c in raw_comps.split("|") if c.strip()]
        else:
            comps = [str(c).strip() for c in raw_comps if str(c).strip()]

        # Cada vaga conta uma única vez por competência
        for c in set(comps):
            demanda[c] += 1

        # Aderência individual da vaga
        ad_vaga = calcular_aderencia_vaga(comps, comps_curso)
        cobertas_vaga = [c for c in comps if c in comps_curso]
        faltantes_vaga = [c for c in comps if c not in comps_curso]

        vagas_formatadas_aderencia.append(
            {
                "vaga_id": v.get("vaga_id", ""),
                "titulo": v.get("titulo", ""),
                "empresa": v.get("empresa", ""),
                "cidade": v.get("cidade", ""),
                "salario_min": v.get("salario_min", ""),
                "salario_max": v.get("salario_max", ""),
                "fonte_url": v.get("fonte_url", ""),
                "senioridade": v.get("senioridade", "nao_informado"),
                "area": v.get("area", ""),
                "competencias": comps,
                "aderencia_pct": ad_vaga,
                "competencias_cobertas": cobertas_vaga,
                "competencias_faltantes": faltantes_vaga,
            }
        )

    # 5. Coberturas
    total_comps_distintas = len(demanda)
    distintas_ensinadas = len([c for c in demanda if c in comps_curso])
    cobertura_pct = (
        round((distintas_ensinadas / total_comps_distintas * 100), 1)
        if total_comps_distintas > 0
        else None
    )

    total_mencoes = sum(demanda.values())
    mencoes_ensinadas = sum(qtd for c, qtd in demanda.items() if c in comps_curso)
    cobertura_ponderada_pct = (
        round((mencoes_ensinadas / total_mencoes * 100), 1)
        if total_mencoes > 0
        else None
    )

    # 6. Lacunas ordenadas (frequência decrescente, depois nome normalizado crescente)
    lacunas_brutas = [
        (c, qtd) for c, qtd in demanda.items() if c not in comps_curso
    ]
    lacunas_brutas.sort(key=lambda item: (-item[1], normalizar_texto(item[0])))

    lacunas = [
        {
            "competencia": c,
            "area": comp_area_map.get(c, "geral"),
            "frequencia": qtd,
            "pct_vagas": round((qtd / amostra_n * 100), 1) if amostra_n > 0 else 0.0,
        }
        for c, qtd in lacunas_brutas
    ]

    lacunas_map = {item["competencia"]: item["frequencia"] for item in lacunas}

    # 7. Trilha-base gulosa
    trilha_base, sem_modulo = calcular_trilha_base(
        lacunas_map, todos_modulos_base, limite_modulos=3
    )

    # 8. Aderência média antes e depois da trilha
    comps_trilha = set()
    for t in trilha_base:
        for c in t["competencias_cobertas"]:
            comps_trilha.add(c)

    comps_pos_trilha = comps_curso | comps_trilha

    ads_antes = [
        v["aderencia_pct"]
        for v in vagas_formatadas_aderencia
        if v["aderencia_pct"] is not None
    ]
    ads_depois: list[float] = []

    for v in vagas_formatadas_aderencia:
        c_vaga = v["competencias"]
        if c_vaga:
            cob = [c for c in c_vaga if c in comps_pos_trilha]
            ads_depois.append(round((len(cob) / len(c_vaga) * 100), 1))

    aderencia_antes_pct = (
        round((sum(ads_antes) / len(ads_antes)), 1) if ads_antes else None
    )
    aderencia_depois_pct = (
        round((sum(ads_depois) / len(ads_depois)), 1) if ads_depois else None
    )

    # 9. Salário mediano
    salario_mediano, salario_n = calcular_salario_mediano(vagas_escopo)

    # 10. Estruturas de gráficos
    graficos = gerar_estruturas_grafico(
        curso=curso,
        amostra_n=amostra_n,
        demanda=demanda,
        comps_curso=comps_curso,
        lacunas=lacunas,
        vagas_escopo=vagas_escopo,
        modulos_do_curso=modulos_do_curso,
    )

    return {
        "curso": curso,
        "amostra_n": amostra_n,
        "cobertura_pct": cobertura_pct,
        "cobertura_ponderada_pct": cobertura_ponderada_pct,
        "lacunas": lacunas,
        "sem_modulo": sem_modulo,
        "trilha_base": trilha_base,
        "aderencia_antes_pct": aderencia_antes_pct,
        "aderencia_depois_pct": aderencia_depois_pct,
        "salario_mediano": salario_mediano,
        "salario_n": salario_n,
        "graficos": graficos,
        "vagas_aderencia": vagas_formatadas_aderencia,
    }
