# Execution/agentes/coletor.py
# Agente Coletor: sanitização de PII (e-mails/telefones), normalização, deduplicação e fallback.

import hashlib
import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    from zoneinfo import ZoneInfo
    TZ_SP = ZoneInfo("America/Sao_Paulo")
except Exception:
    TZ_SP = None

from Execution.dados import normalizar_texto, carregar_vagas_demo
from Execution.scrapers.base import BaseScraper

# Regex de sanitização de PII (LGPD e Diretiva §2.7)
RE_EMAIL = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", re.IGNORECASE)

# Padrão amplo de telefones brasileiros:
# Suporta formatos como: (14) 99876-5432, 14 99876-5432, +55 14 3322-1100, (14) 33221100, 99876-5432
RE_TELEFONE = re.compile(
    r"(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?(?:9\s*)?\d{4}[-\s]?\d{4}\b"
)


def remover_pii(texto: str) -> str:
    """
    Remove endereços de e-mail e números de telefone do texto para conformidade com LGPD.
    Substitui os padrões identificados por vazio.
    """
    if not texto:
        return ""
    # Remove e-mails
    sem_email = RE_EMAIL.sub("", texto)
    # Remove telefones
    sem_telefone = RE_TELEFONE.sub("", sem_email)
    return sem_telefone


def limpar_texto_requisitos(texto: str) -> str:
    """
    Remove tags HTML residuais, expurga PII (e-mails e telefones) e
    normaliza múltiplos espaços em branco.
    """
    if not texto:
        return ""

    # Remove tags HTML simples
    texto_sem_html = re.sub(r"<[^>]+>", " ", texto)

    # Expurga dados de contato pessoais
    texto_limpo = remover_pii(texto_sem_html)

    # Normaliza espaçamentos e quebras de linha
    texto_normalizado = re.sub(r"\s+", " ", texto_limpo).strip()
    return texto_normalizado


def gerar_vaga_id(titulo: str, empresa: str, cidade: str) -> str:
    """
    Gera o identificador estável da vaga via hash SHA1 dos campos canônicos:
    sha1(normalizar(titulo) + "|" + normalizar(empresa) + "|" + normalizar(cidade))[:12]
    Garante que a mesma vaga mantenha o mesmo ID entre coletas.
    """
    t_norm = normalizar_texto(titulo or "")
    e_norm = normalizar_texto(empresa or "")
    c_norm = normalizar_texto(cidade or "")
    chave = f"{t_norm}|{e_norm}|{c_norm}".encode("utf-8")
    return hashlib.sha1(chave).hexdigest()[:12]


def sanitizar_registro_vaga(vaga: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida e normaliza um registro individual de vaga para o esquema padrão (§5).
    Garante que salários sejam inteiros positivos ou None (nunca 0).
    """
    titulo = str(vaga.get("titulo") or "").strip()
    empresa = str(vaga.get("empresa") or "").strip()
    cidade = str(vaga.get("cidade") or "").strip()

    # Identificador único determinístico conforme Diretiva §6
    vaga_id = gerar_vaga_id(titulo, empresa, cidade)

    # Salários: inteiro ou None (nunca 0)
    sal_min = vaga.get("salario_min")
    sal_max = vaga.get("salario_max")

    def _tratar_salario(val: Any) -> Optional[int]:
        if val is None or val == "" or str(val).lower() == "nan":
            return None
        try:
            val_int = int(float(val))
            return val_int if val_int > 0 else None
        except (ValueError, TypeError):
            return None

    sal_min_proc = _tratar_salario(sal_min)
    sal_max_proc = _tratar_salario(sal_max)

    req_texto = limpar_texto_requisitos(str(vaga.get("requisitos_texto") or ""))

    data_val = str(vaga.get("data") or "")
    if not data_val or data_val.lower() == "nan":
        agora = datetime.now(TZ_SP) if TZ_SP else datetime.now()
        data_val = agora.strftime("%Y-%m-%d")

    coletado_em = str(vaga.get("coletado_em") or "")
    if not coletado_em or coletado_em.lower() == "nan":
        agora = datetime.now(TZ_SP) if TZ_SP else datetime.now()
        coletado_em = agora.isoformat()

    return {
        "vaga_id": vaga_id,
        "titulo": titulo,
        "empresa": empresa,
        "cidade": cidade,
        "data": data_val,
        "salario_min": sal_min_proc,
        "salario_max": sal_max_proc,
        "fonte_url": str(vaga.get("fonte_url") or ""),
        "requisitos_texto": req_texto,
        "coletado_em": coletado_em,
        "senioridade": str(vaga.get("senioridade") or "nao_informado"),
        "modo_demo": bool(vaga.get("modo_demo", False)),
    }


def deduplicar_vagas(vagas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicatas utilizando o vaga_id estável como chave primária.
    Preserva a ocorrência com registro de data/coleta mais recente.
    """
    mapa_dedup: Dict[str, Dict[str, Any]] = {}

    for raw in vagas:
        v = sanitizar_registro_vaga(raw)
        v_id = v["vaga_id"]
        if v_id not in mapa_dedup:
            mapa_dedup[v_id] = v
        else:
            # Se já existir, sobrescreve se a nova tiver dados mais recentes
            if v["data"] >= mapa_dedup[v_id]["data"]:
                mapa_dedup[v_id] = v

    return list(mapa_dedup.values())


def salvar_vagas_brutas(vagas: List[Dict[str, Any]], pasta_temp: str = ".temp") -> str:
    """
    Salva o lote bruto em .temp/vagas_brutas_AAAAMMDD_HHMM.json.
    """
    os.makedirs(pasta_temp, exist_ok=True)
    agora = datetime.now(TZ_SP) if TZ_SP else datetime.now()
    nome_arquivo = f"vagas_brutas_{agora.strftime('%Y%m%d_%H%M')}.json"
    caminho = os.path.join(pasta_temp, nome_arquivo)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(vagas, f, ensure_ascii=False, indent=2)

    return caminho


def carregar_vagas_demo_brutas(caminho_csv: str = "data/vagas_demo.csv") -> List[Dict[str, Any]]:
    """
    Carrega o arquivo de demonstração data/vagas_demo.csv e converte
    para a estrutura padronizada de registros brutos, com modo_demo = True.
    """
    df = carregar_vagas_demo(caminho_csv)
    vagas_raw: List[Dict[str, Any]] = []

    for _, row in df.iterrows():
        reg = row.to_dict()
        reg["modo_demo"] = True
        vagas_raw.append(reg)

    return deduplicar_vagas(vagas_raw)


def executar_coleta(
    scraper: Optional[BaseScraper] = None,
    modo_demo: bool = True,
    caminho_demo: str = "data/vagas_demo.csv",
    pasta_temp: str = ".temp",
) -> Dict[str, Any]:
    """
    Orquestra a coleta de vagas de acordo com as regras:
    - Se modo_demo for True: utiliza dados locais de demonstração.
    - Se modo_demo for False: tenta executar o scraper configurado.
    - Se o scraper falhar ou for bloqueado: aciona fallback transparente para demo.
    - Salva sempre saída intermediária em .temp/.
    """
    erros = []
    vagas_coletadas: List[Dict[str, Any]] = []
    usou_demo = modo_demo

    if not modo_demo and scraper is not None:
        try:
            vagas_raw = scraper.coletar()
            vagas_coletadas = deduplicar_vagas(vagas_raw)
        except Exception as e:
            erros.append(str(e))
            usou_demo = True

    if usou_demo:
        vagas_coletadas = carregar_vagas_demo_brutas(caminho_demo)

    caminho_salvo = salvar_vagas_brutas(vagas_coletadas, pasta_temp=pasta_temp)

    return {
        "sucesso": len(vagas_coletadas) > 0,
        "modo_demo": usou_demo,
        "total": len(vagas_coletadas),
        "vagas": vagas_coletadas,
        "arquivo_intermediario": caminho_salvo,
        "erros": erros,
    }
