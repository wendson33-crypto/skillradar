# Execution/orquestrador.py
# Orquestrador central do SkillRadar: pipeline completo de 3 camadas determinístico e IA.

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Garante compatibilidade de saída em consoles Windows (cp1252/utf-8)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Garante que a raiz do projeto esteja no sys.path para execução direta da CLI
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

try:
    from zoneinfo import ZoneInfo
    TZ_SP = ZoneInfo("America/Sao_Paulo")
except Exception:
    TZ_SP = None

# Camada de Dados
from Execution.dados import (
    carregar_competencias_cursos,
    carregar_taxonomia,
    carregar_cursos_areas,
    calcular_area_principal_vaga,
    calcular_contagens_demanda,
    normalizar_texto,
)

# Camada de Agentes
from Execution.agentes.coletor import (
    executar_coleta,
    carregar_vagas_demo_brutas,
)
from Execution.scrapers.fonte_vagas_1 import FonteVagasPortalRegional
from Execution.agentes.extrator import executar_extracao_vaga
from Execution.agentes.matcher import (
    executar_matching_curso,
    calcular_salario_por_area,
    calcular_variacao_semana,
)
from Execution.agentes.orientador import executar_orientador_curso


def gerar_slug(texto: str) -> str:
    """
    Gera slug padronizado sem acentos, em minúsculas e separado por hífens.
    Exemplo: 'Técnico em Desenvolvimento de Sistemas' -> 'tecnico-em-desenvolvimento-de-sistemas'
    """
    if not texto:
        return ""
    norm = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in norm if not unicodedata.combining(c))
    slug = re.sub(r"[^\w\s-]", "", sem_acento.lower()).strip()
    return re.sub(r"[-\s]+", "-", slug)


def sanitizar_para_firestore(obj: Any) -> Any:
    """
    Remove recursivamente valores incompatíveis com Firestore (NaN, Infinity),
    substituindo-os por None.
    """
    if isinstance(obj, float):
        import math
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif isinstance(obj, dict):
        return {k: sanitizar_para_firestore(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitizar_para_firestore(item) for item in obj]
    return obj


def executar_pipeline(
    modo: str = "demo",
    sem_gemini: bool = True,
    dry_run: bool = True,
    caminho_dados: Optional[str] = None,
    pasta_temp: str = ".temp",
) -> Dict[str, Any]:
    """
    Executa o fluxo completo do SkillRadar de ponta a ponta:
    1. Coleta ou leitura de vagas de demonstração
    2. Extração de competências via Extrator (Gemini ou Plano B)
    3. Identificação de macroárea por vaga e cálculo de tendências globais
    4. Matcher determinístico para todos os cursos da base
    5. Orientador para geração de insights e trilhas validadas
    6. Consolidação dos documentos do Firestore
    7. Saída em .temp/dry_run_*.json (se dry_run=True) ou persistência no Firestore
    """
    agora = datetime.now(TZ_SP) if TZ_SP else datetime.now()
    timestamp_iso = agora.isoformat()
    data_hoje_iso = agora.strftime("%Y-%m-%d")

    print(f"\n{'='*70}")
    print(f"[INICIO] PIPELINE SKILLRADAR -- MODO: {modo.upper()} | SEM-GEMINI: {sem_gemini} | DRY-RUN: {dry_run}")
    print(f"{'='*70}\n")

    # --------------------------------------------------------------------------
    # ETAPA 1: Carregamento de Bases Canônicas
    # --------------------------------------------------------------------------
    print("[1/5] Carregando bases de dados RAG (cursos, taxonomia, áreas)...")
    base_dir = caminho_dados or "data"
    df_cursos = carregar_competencias_cursos(os.path.join(base_dir, "competencias_cursos.csv"))
    df_taxonomia = carregar_taxonomia(os.path.join(base_dir, "taxonomia_competencias.csv"))
    df_cursos_areas = carregar_cursos_areas(os.path.join(base_dir, "cursos_areas.csv"))

    comp_area_map = dict(
        zip(
            df_taxonomia["competencia_padrao"].str.strip(),
            df_taxonomia["area"].str.strip(),
        )
    )

    # --------------------------------------------------------------------------
    # ETAPA 2: Coleta de Vagas (Web Scraping ou Modo Demo)
    # --------------------------------------------------------------------------
    print(f"[2/5] Coletando registros de vagas (Modo: {modo})...")
    if modo == "real":
        scraper = FonteVagasPortalRegional()
        resultado_coleta = executar_coleta(
            scraper=scraper,
            modo_demo=False,
            caminho_demo=os.path.join(base_dir, "vagas_demo.csv"),
            pasta_temp=pasta_temp,
        )
    else:
        resultado_coleta = executar_coleta(
            scraper=None,
            modo_demo=True,
            caminho_demo=os.path.join(base_dir, "vagas_demo.csv"),
            pasta_temp=pasta_temp,
        )

    vagas_brutas = resultado_coleta["vagas"]
    usou_modo_demo = resultado_coleta["modo_demo"]
    print(f"   [OK] {len(vagas_brutas)} vagas prontas (Modo Demo: {usou_modo_demo}).")

    # --------------------------------------------------------------------------
    # ETAPA 3: Extração de Competências e Classificação de Área
    # --------------------------------------------------------------------------
    print(f"[3/5] Extraindo competências técnicas e classificando áreas...")
    vagas_processadas: List[Dict[str, Any]] = []

    for v in vagas_brutas:
        saida_extrator = executar_extracao_vaga(
            vaga=v,
            mapa_taxonomia=df_taxonomia,
            sem_gemini=sem_gemini,
            caminho_cache=os.path.join(pasta_temp, "cache_extrator.json"),
        )

        comps = saida_extrator.competencias
        area_principal = calcular_area_principal_vaga(comps, comp_area_map=comp_area_map)

        v_proc = dict(v)
        v_proc["competencias"] = comps
        v_proc["nao_mapeadas"] = saida_extrator.nao_mapeadas
        v_proc["senioridade"] = saida_extrator.senioridade
        v_proc["area"] = area_principal
        vagas_processadas.append(v_proc)

    # Métricas globais de demanda
    demanda_global = calcular_contagens_demanda(vagas_processadas)
    variacao_global = calcular_variacao_semana(vagas_processadas, data_referencia=data_hoje_iso)
    salarios_por_area = calcular_salario_por_area(vagas_processadas)
    print(f"   [OK] Extracao concluida. {len(demanda_global)} competencias distintas demandadas.")

    # --------------------------------------------------------------------------
    # ETAPA 4: Análise por Curso (Matcher + Orientador)
    # --------------------------------------------------------------------------
    print(f"[4/5] Executando Matching e Orientacao Pedagogica por Curso...")
    cursos_disponiveis = sorted(df_cursos_areas["curso"].unique())

    documentos_lacunas: Dict[str, Dict[str, Any]] = {}
    documentos_trilhas: Dict[str, Dict[str, Any]] = {}
    documentos_insights: Dict[str, Dict[str, Any]] = {}

    for curso_nome in cursos_disponiveis:
        curso_slug = gerar_slug(curso_nome)

        # 4.1 Executa Matcher determinístico
        resultado_matcher = executar_matching_curso(
            curso=curso_nome,
            df_cursos=df_cursos,
            df_taxonomia=df_taxonomia,
            df_cursos_areas=df_cursos_areas,
            vagas_com_area=vagas_processadas,
        )

        areas_curso = df_cursos_areas[df_cursos_areas["curso"] == curso_nome]["area_foco"].tolist()

        # Documento da coleção lacunas_cursos/{cursoSlug}
        documentos_lacunas[curso_slug] = {
            "curso": curso_nome,
            "areas_foco": areas_curso,
            "amostra_n": resultado_matcher["amostra_n"],
            "total_coletadas": len(vagas_processadas),
            "cobertura_pct": resultado_matcher["cobertura_pct"],
            "cobertura_ponderada_pct": resultado_matcher["cobertura_ponderada_pct"],
            "lacunas": resultado_matcher["lacunas"],
            "kpis": {
                "salario_mediano": resultado_matcher["salario_mediano"],
                "salario_n": resultado_matcher["salario_n"],
            },
            "graficos": resultado_matcher["graficos"],
            "atualizado_em": timestamp_iso,
        }

        # 4.2 Executa Orientador
        fatos_orientador = {
            "curso": curso_nome,
            "amostra_n": resultado_matcher["amostra_n"],
            "lacunas": resultado_matcher["lacunas"][:5],
            "sem_modulo": resultado_matcher["sem_modulo"],
            "trilha_base": resultado_matcher["trilha_base"],
            "aderencia_antes_pct": resultado_matcher["aderencia_antes_pct"],
            "aderencia_depois_pct": resultado_matcher["aderencia_depois_pct"],
        }

        saida_orientador = executar_orientador_curso(
            fatos=fatos_orientador,
            sem_gemini=sem_gemini,
        )

        # Documento da coleção trilhas_sugeridas/{cursoSlug}
        documentos_trilhas[curso_slug] = {
            "curso": curso_nome,
            "modulos": [item.model_dump() for item in saida_orientador.trilha],
            "sem_modulo": resultado_matcher["sem_modulo"],
            "aderencia_antes_pct": resultado_matcher["aderencia_antes_pct"],
            "aderencia_depois_pct": resultado_matcher["aderencia_depois_pct"],
            "atualizado_em": timestamp_iso,
        }

        # Documentos da coleção insights/{id}
        for idx, ins in enumerate(saida_orientador.insights, start=1):
            doc_id = f"coordenacao-{curso_slug}-{idx}"
            documentos_insights[doc_id] = {
                "id": doc_id,
                "escopo": "coordenacao",
                "curso": curso_slug,
                "titulo": ins.titulo,
                "texto": ins.texto,
                "severidade": ins.severidade,
                "origem": ins.origem,
                "criado_em": timestamp_iso,
            }

        print(f"   [OK] Curso '{curso_nome}': amostra {resultado_matcher['amostra_n']} | cob {resultado_matcher['cobertura_pct']}% | trilha com {len(saida_orientador.trilha)} modulos.")

    # --------------------------------------------------------------------------
    # ETAPA 5: Estruturação das Coleções Globais do Firestore
    # --------------------------------------------------------------------------
    print("[5/5] Consolidando documentos para o Firestore...")

    # 5.1 Coleção vagas_ativas/{vaga_id}
    documentos_vagas: Dict[str, Dict[str, Any]] = {}
    for v in vagas_processadas:
        v_id = v["vaga_id"]
        documentos_vagas[v_id] = {
            "vaga_id": v_id,
            "titulo": v["titulo"],
            "empresa": v["empresa"],
            "cidade": v["cidade"],
            "data": v["data"],
            "salario_min": v["salario_min"],
            "salario_max": v["salario_max"],
            "fonte_url": v["fonte_url"],
            "competencias": v["competencias"],
            "senioridade": v["senioridade"],
            "area": v["area"],
            "modo_demo": v.get("modo_demo", usou_modo_demo),
            "coletado_em": v["coletado_em"],
        }

    # 5.2 Coleção competencias_demandadas/{competenciaSlug}
    documentos_competencias: Dict[str, Dict[str, Any]] = {}
    total_vagas_n = len(vagas_processadas)
    for comp, freq in demanda_global.items():
        comp_slug = gerar_slug(comp)
        pct = round((freq / total_vagas_n * 100), 1) if total_vagas_n > 0 else 0.0
        var_semana = variacao_global.get(comp, 0)
        area_comp = comp_area_map.get(comp, "geral")

        documentos_competencias[comp_slug] = {
            "competencia": comp,
            "area": area_comp,
            "frequencia": freq,
            "pct_vagas": pct,
            "variacao_semana": var_semana,
            "atualizado_em": timestamp_iso,
        }

    # 5.3 Coleção contexto/atual
    documento_contexto = {
        "total_vagas": total_vagas_n,
        "ultima_coleta": timestamp_iso,
        "modo_demo": usou_modo_demo,
        "fonte": "vagas_demo.csv" if usou_modo_demo else "portal_regional",
        "graficos": {
            "salario_por_area": salarios_por_area,
        },
        "atualizado_em": timestamp_iso,
    }

    # Payload Consolidado Sanitizado
    payload_firestore = sanitizar_para_firestore({
        "contexto": {
            "atual": documento_contexto,
        },
        "vagas_ativas": documentos_vagas,
        "lacunas_cursos": documentos_lacunas,
        "trilhas_sugeridas": documentos_trilhas,
        "insights": documentos_insights,
        "competencias_demandadas": documentos_competencias,
    })

    # Gravação no Firestore ou em .temp/ quando em modo dry-run
    caminho_arquivo_dry_run = None
    resultado_firestore = None

    if dry_run:
        os.makedirs(pasta_temp, exist_ok=True)
        nome_arquivo = f"dry_run_{agora.strftime('%Y%m%d_%H%M%S')}.json"
        caminho_arquivo_dry_run = os.path.join(pasta_temp, nome_arquivo)
        caminho_latest = os.path.join(pasta_temp, "dry_run_latest.json")

        with open(caminho_arquivo_dry_run, "w", encoding="utf-8") as f:
            json.dump(payload_firestore, f, ensure_ascii=False, indent=2)

        with open(caminho_latest, "w", encoding="utf-8") as f:
            json.dump(payload_firestore, f, ensure_ascii=False, indent=2)

        print(f"\n[DRY-RUN] Lote consolidado salvo com sucesso em:")
        print(f"   -> {caminho_arquivo_dry_run}")
        print(f"   -> {caminho_latest}")
    else:
        print(f"\n[FIRESTORE] Gravando coleções no Cloud Firestore...")
        from Execution.firestore_cliente import gravar_payload_firestore
        resultado_firestore = gravar_payload_firestore(payload_firestore)
        if resultado_firestore.get("sucesso"):
            print(f"   [OK] {resultado_firestore['total_gravados']} documentos persistidos no Firestore com sucesso!")
        else:
            print(f"   [AVISO] Nao foi possivel persistir no Firestore: {resultado_firestore.get('motivo')}")
            os.makedirs(pasta_temp, exist_ok=True)
            caminho_backup = os.path.join(pasta_temp, f"backup_firestore_{agora.strftime('%Y%m%d_%H%M%S')}.json")
            with open(caminho_backup, "w", encoding="utf-8") as f:
                json.dump(payload_firestore, f, ensure_ascii=False, indent=2)
            print(f"   [BACKUP] Copia de contingencia salva em: {caminho_backup}")

    print(f"\n{'='*70}")
    print("[SUCESSO] PIPELINE CONCLUIDO COM SUCESSO!")
    print(f"   - Vagas processadas: {len(documentos_vagas)}")
    print(f"   - Cursos mapeados: {len(documentos_lacunas)}")
    print(f"   - Competências demandadas: {len(documentos_competencias)}")
    print(f"   - Insights pedagógicos: {len(documentos_insights)}")
    print(f"   - Trilhas sugeridas: {len(documentos_trilhas)}")
    print(f"{'='*70}\n")

    return {
        "sucesso": True,
        "modo_demo": usou_modo_demo,
        "arquivo_dry_run": caminho_arquivo_dry_run,
        "payload": payload_firestore,
    }


def main():
    parser = argparse.ArgumentParser(
        description="SkillRadar — Orquestrador central de extração, análise de lacunas e recomendação pedagógica."
    )
    parser.add_argument(
        "--modo",
        choices=["demo", "real"],
        default="demo",
        help="Modo de execução: 'demo' (vagas_demo.csv offline) ou 'real' (web scraping regional)",
    )
    parser.add_argument(
        "--sem-gemini",
        action="store_true",
        help="Executa pipeline sem chamadas à API Gemini (utiliza extrator e orientador determinísticos)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Executa o pipeline completo sem conectar ao Firestore, salvando o lote em .temp/dry_run_*.json",
    )

    args = parser.parse_args()

    # Se a chave da API do Gemini não existir no ambiente, força --sem-gemini com aviso amigável
    sem_gemini = args.sem_gemini or (not os.environ.get("GEMINI_API_KEY"))

    try:
        resultado = executar_pipeline(
            modo=args.modo,
            sem_gemini=sem_gemini,
            dry_run=args.dry_run,
        )
        sys.exit(0 if resultado["sucesso"] else 1)
    except Exception as e:
        print(f"\n[ERRO CRITICO] NA EXECUCAO DO PIPELINE: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
