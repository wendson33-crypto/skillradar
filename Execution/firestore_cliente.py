# Execution/firestore_cliente.py
# Cliente Firebase Admin SDK para gravação de lotes no Cloud Firestore.

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env local se existir
load_dotenv()

# Injeção da raiz no sys.path para importações consistentes
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

# Import condicional do firebase_admin para resiliência offline
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_ADMIN_DISPONIVEL = True
except ImportError:
    FIREBASE_ADMIN_DISPONIVEL = False


def verificar_configuracao_firebase() -> Dict[str, Any]:
    """
    Verifica se os parâmetros necessários para o Firebase Firestore estão configurados.
    NUNCA expõe chaves ou conteúdo de arquivos (apenas confirmação booleana).
    """
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.environ.get("FIREBASE_PROJECT_ID")

    tem_cred_var = bool(cred_path and cred_path.strip())
    arquivo_cred_existe = False
    if tem_cred_var:
        arquivo_cred_existe = os.path.isfile(cred_path)

    tem_project_id = bool(project_id and project_id.strip())

    pronto = FIREBASE_ADMIN_DISPONIVEL and tem_cred_var and arquivo_cred_existe

    return {
        "sdk_instalado": FIREBASE_ADMIN_DISPONIVEL,
        "variavel_credenciais_definida": tem_cred_var,
        "arquivo_credenciais_existe": arquivo_cred_existe,
        "variavel_project_id_definida": tem_project_id,
        "pronto_para_gravar": pronto,
    }


def tem_arrays_aninhados(obj: Any) -> bool:
    """
    Verifica recursivamente se há arrays dentro de arrays (rejeitado pelo Firestore).
    Retorna True se encontrar qualquer lista como elemento direto de outra lista.
    """
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, list):
                return True
            if tem_arrays_aninhados(item):
                return True
    elif isinstance(obj, dict):
        for val in obj.values():
            if tem_arrays_aninhados(val):
                return True
    return False


def obter_db():
    """
    Retorna a instância do cliente Firestore usando Firebase Admin SDK.
    Inicializa o app padrão se ainda não tiver sido inicializado.
    """
    if not FIREBASE_ADMIN_DISPONIVEL:
        raise RuntimeError("O pacote 'firebase-admin' não está instalado no ambiente.")

    if not firebase_admin._apps:
        cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not cred_path or not os.path.isfile(cred_path):
            raise FileNotFoundError(
                "Arquivo de conta de serviço referenciado em GOOGLE_APPLICATION_CREDENTIALS não encontrado."
            )

        cred = credentials.Certificate(cred_path)
        project_id = os.environ.get("FIREBASE_PROJECT_ID")
        options = {"projectId": project_id} if project_id else None
        firebase_admin.initialize_app(cred, options=options)

    return firestore.client()


def converter_payload_para_operacoes(payload: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Converte o payload consolidado do orquestrador em uma lista plana de operações:
    [(caminho_documento, dados_documento), ...]
    Valida ausência de arrays aninhados antes de gerar a operação.
    """
    operacoes: List[Tuple[str, Dict[str, Any]]] = []

    # 1. Coleção contexto/atual
    if "contexto" in payload and "atual" in payload["contexto"]:
        doc_atual = payload["contexto"]["atual"]
        if tem_arrays_aninhados(doc_atual):
            raise ValueError("Documento 'contexto/atual' contém arrays aninhados.")
        operacoes.append(("contexto/atual", doc_atual))

    # 2. Coleção vagas_ativas/{vaga_id}
    if "vagas_ativas" in payload:
        for vaga_id, dados in payload["vagas_ativas"].items():
            if tem_arrays_aninhados(dados):
                raise ValueError(f"Vaga '{vaga_id}' contém arrays aninhados.")
            operacoes.append((f"vagas_ativas/{vaga_id}", dados))

    # 3. Coleção lacunas_cursos/{cursoSlug}
    if "lacunas_cursos" in payload:
        for curso_slug, dados in payload["lacunas_cursos"].items():
            if tem_arrays_aninhados(dados):
                raise ValueError(f"Curso '{curso_slug}' em lacunas_cursos contém arrays aninhados.")
            operacoes.append((f"lacunas_cursos/{curso_slug}", dados))

    # 4. Coleção trilhas_sugeridas/{cursoSlug}
    if "trilhas_sugeridas" in payload:
        for curso_slug, dados in payload["trilhas_sugeridas"].items():
            if tem_arrays_aninhados(dados):
                raise ValueError(f"Trilha '{curso_slug}' contém arrays aninhados.")
            operacoes.append((f"trilhas_sugeridas/{curso_slug}", dados))

    # 5. Coleção insights/{id}
    if "insights" in payload:
        for doc_id, dados in payload["insights"].items():
            if tem_arrays_aninhados(dados):
                raise ValueError(f"Insight '{doc_id}' contém arrays aninhados.")
            operacoes.append((f"insights/{doc_id}", dados))

    # 6. Coleção competencias_demandadas/{competenciaSlug}
    if "competencias_demandadas" in payload:
        for comp_slug, dados in payload["competencias_demandadas"].items():
            if tem_arrays_aninhados(dados):
                raise ValueError(f"Competência '{comp_slug}' contém arrays aninhados.")
            operacoes.append((f"competencias_demandadas/{comp_slug}", dados))

    return operacoes


def gravar_lote(db, operacoes: List[Tuple[str, Dict[str, Any]]], tamanho_lote: int = 500) -> int:
    """
    Grava a lista de operações no Firestore em batches de no máximo 500 operações.
    Utiliza db.batch().set() garantindo idempotência e atualização atômica.
    Retorna o total de documentos gravados.
    """
    total = len(operacoes)
    gravados = 0

    for i in range(0, total, tamanho_lote):
        bloco = operacoes[i : i + tamanho_lote]
        lote = db.batch()

        for caminho, dados in bloco:
            doc_ref = db.document(caminho)
            lote.set(doc_ref, dados)

        lote.commit()
        gravados += len(bloco)

    return gravados


def gravar_payload_firestore(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Orquestra a conversão e gravação de todo o payload do SkillRadar no Firestore.
    """
    config = verificar_configuracao_firebase()
    if not config["pronto_para_gravar"]:
        return {
            "sucesso": False,
            "motivo": "Configuração de conta de serviço ou variáveis do Firebase ausentes.",
            "total_gravados": 0,
            "detalhes": config,
        }

    try:
        db = obter_db()
        operacoes = converter_payload_para_operacoes(payload)
        total_gravados = gravar_lote(db, operacoes)

        return {
            "sucesso": True,
            "total_gravados": total_gravados,
            "total_operacoes": len(operacoes),
        }
    except Exception as e:
        return {
            "sucesso": False,
            "motivo": f"Erro durante a gravação no Firestore: {str(e)}",
            "total_gravados": 0,
        }
