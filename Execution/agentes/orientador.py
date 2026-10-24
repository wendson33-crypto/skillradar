# Execution/agentes/orientador.py
# Agente Orientador: geração de insights pedagógicos e recomendação de trilha de formação
# com validação estrita anti-alucinação e Plano B determinístico por templates.

import json
import os
import re
from typing import List, Dict, Any, Optional, Literal, Set
from pydantic import BaseModel, Field


class Insight(BaseModel):
    """
    Insight pedagógico e de mercado gerado para a coordenação ou aluno.
    """
    titulo: str = Field(max_length=100)
    texto: str = Field(max_length=280)
    severidade: Literal["info", "aviso", "critico"] = "info"
    origem: Literal["gemini", "template"] = "gemini"


class ItemTrilha(BaseModel):
    """
    Módulo recomendado para compor a trilha formativa.
    """
    curso: str
    modulo: str
    motivo: str = Field(max_length=280)
    carga_horaria: Optional[int] = None
    competencias_cobertas: Optional[List[str]] = None
    peso: Optional[int] = None


class OrientadorSaida(BaseModel):
    """
    Estrutura validada de saída do Agente Orientador (§6).
    """
    insights: List[Insight] = Field(max_length=3)
    trilha: List[ItemTrilha]


def extrair_numeros_de_texto(texto: str) -> Set[float]:
    """
    Extrai todos os números reais ou inteiros presentes no texto,
    suportando vírgula ou ponto como separador decimal.
    """
    encontrados = set()
    padrao = r"\b\d+(?:[.,]\d+)?\b"
    for m in re.finditer(padrao, texto):
        val_str = m.group(0).replace(",", ".")
        try:
            encontrados.add(float(val_str))
        except ValueError:
            pass
    return encontrados


def coletar_numeros_dos_fatos(fatos: Dict[str, Any]) -> Set[float]:
    """
    Varre recursivamente o dicionário de fatos para mapear todos os
    números legítimos permitidos no texto gerado pelo Gemini.
    """
    permitidos = set()

    def _varrer(obj: Any):
        if isinstance(obj, (int, float)):
            permitidos.add(float(obj))
        elif isinstance(obj, dict):
            for v in obj.values():
                _varrer(v)
        elif isinstance(obj, list):
            for item in obj:
                _varrer(item)

    _varrer(fatos)
    # Adiciona também quantidades de itens das coleções (ex: tamanho da trilha)
    if "trilha_base" in fatos and isinstance(fatos["trilha_base"], list):
        permitidos.add(float(len(fatos["trilha_base"])))
    if "lacunas" in fatos and isinstance(fatos["lacunas"], list):
        permitidos.add(float(len(fatos["lacunas"])))

    return permitidos


def validar_anti_alucinacao_numerica(texto: str, numeros_permitidos: Set[float]) -> bool:
    """
    Garante que nenhum número mencionado no texto foi alucinado ou inventado.
    Todo número deve coincidir com um número presente nos fatos de entrada.
    """
    nums_texto = extrair_numeros_de_texto(texto)
    for num in nums_texto:
        # Permite tolerância de 0.05 para pequenas variações de arredondamento
        casou = any(abs(num - perm) < 0.05 for perm in numeros_permitidos)
        if not casou:
            return False
    return True


def gerar_plano_b_templates(fatos: Dict[str, Any]) -> OrientadorSaida:
    """
    Plano B determinístico com templates (§6.180).
    Utilizado em modo offline, sem Gemini ou se a validação do modelo falhar.
    """
    curso = fatos.get("curso", "Curso Técnico")
    amostra_n = fatos.get("amostra_n", 0)
    lacunas = fatos.get("lacunas", [])
    sem_modulo = fatos.get("sem_modulo", [])
    trilha_base = fatos.get("trilha_base", [])
    antes_pct = fatos.get("aderencia_antes_pct", 0.0)
    depois_pct = fatos.get("aderencia_depois_pct", 0.0)

    insights: List[Insight] = []

    # 1. Insight sobre a maior lacuna identificada
    if lacunas:
        top_lacuna = lacunas[0]
        comp_nome = top_lacuna.get("competencia", "")
        freq = top_lacuna.get("frequencia", 0)

        if comp_nome in sem_modulo:
            insights.append(
                Insight(
                    titulo="Demanda Externa Não Coberta",
                    texto=f"{comp_nome} aparece em {freq} de {amostra_n} vagas e não é ensinada em nenhum módulo da base.",
                    severidade="aviso",
                    origem="template",
                )
            )
        else:
            # Encontra módulo que cobre a lacuna na trilha
            modulo_cobriu = None
            for item in trilha_base:
                if comp_nome in item.get("competencias_cobertas", []):
                    modulo_cobriu = item.get("modulo")
                    break

            if modulo_cobriu:
                insights.append(
                    Insight(
                        titulo="Oportunidade de Atualização",
                        texto=f"{comp_nome} é a maior lacuna da área, presente em {freq} de {amostra_n} vagas, e é ensinada em {modulo_cobriu}.",
                        severidade="info",
                        origem="template",
                    )
                )
            else:
                insights.append(
                    Insight(
                        titulo="Tecnologia em Alta",
                        texto=f"{comp_nome} é a maior lacuna da área, demandada em {freq} de {amostra_n} vagas avaliadas.",
                        severidade="info",
                        origem="template",
                    )
                )

    # 2. Insight sobre a evolução da aderência após a trilha recomendada
    k_modulos = len(trilha_base)
    if k_modulos > 0:
        insights.append(
            Insight(
                titulo="Impacto da Trilha Recomendada",
                texto=f"Os {k_modulos} módulos da trilha elevam a aderência média de {antes_pct}% para {depois_pct}%.",
                severidade="info",
                origem="template",
            )
        )
    else:
        insights.append(
            Insight(
                titulo="Currículo Alinhado",
                texto=f"O currículo do curso atende plenamente o escopo avaliado de {amostra_n} vagas.",
                severidade="info",
                origem="template",
            )
        )

    # 3. Insight de contexto de mercado
    insights.append(
        Insight(
            titulo="Amostra de Mercado Regional",
            texto=f"Métricas calculadas a partir de {amostra_n} vagas do setor tecnológico de Ourinhos e região.",
            severidade="info",
            origem="template",
        )
    )

    # Constrói itens da trilha copiando deterministamente da trilha_base
    itens_trilha: List[ItemTrilha] = []
    for item in trilha_base:
        mod_nome = item.get("modulo", "")
        cur_nome = item.get("curso", "")
        ch = item.get("carga_horaria", 0)
        cobertas = item.get("competencias_cobertas", [])
        peso = item.get("peso", 0)

        itens_trilha.append(
            ItemTrilha(
                curso=cur_nome,
                modulo=mod_nome,
                motivo=f"Módulo com {ch}h práticas cobrindo as lacunas: {', '.join(cobertas)}.",
                carga_horaria=ch,
                competencias_cobertas=cobertas,
                peso=peso,
            )
        )

    return OrientadorSaida(
        insights=insights[:3],
        trilha=itens_trilha,
    )


def executar_orientador_curso(
    fatos: Dict[str, Any],
    sem_gemini: bool = False,
) -> OrientadorSaida:
    """
    Orquestra o Agente Orientador para um curso específico:
    1. Se sem_gemini=True ou ausência de chaves, aciona Plano B em templates.
    2. Envia fatos enxutos ao Gemini via google-genai com schema Pydantic.
    3. Pós-validação anti-alucinação:
       - Todos os módulos devem existir na trilha-base.
       - Nenhum número alucinado fora dos fatos.
       - Textos até 280 caracteres.
       - Se falhar, recorre de forma transparente ao Plano B.
    4. Python anexa deterministicamente carga_horaria, peso e competencias_cobertas.
    """
    trilha_base = fatos.get("trilha_base", [])
    modulos_base_map = {
        (item.get("curso"), item.get("modulo")): item
        for item in trilha_base
    }

    api_key = os.environ.get("GEMINI_API_KEY")
    modelo = os.environ.get("GEMINI_MODEL")

    if sem_gemini or not api_key or not modelo:
        return gerar_plano_b_templates(fatos)

    numeros_permitidos = coletar_numeros_dos_fatos(fatos)
    fatos_json = json.dumps(fatos, ensure_ascii=False, indent=2)

    prompt = (
        "Você é um orientador de carreira de uma escola técnica. Escreva em português do Brasil, em linguagem simples.\n"
        "Regras:\n"
        "1. Use SOMENTE os fatos e números do JSON abaixo. Não invente números, vagas, empresas nem módulos.\n"
        "2. Em 'trilha', use apenas módulos que estão em 'trilha_base' (copie curso e módulo exatamente).\n"
        "3. Insights: no máximo 3, com título curto e 1 ou 2 frases.\n"
        "4. Não prometa emprego nem aumento de salário.\n\n"
        f"Fatos:\n{fatos_json}\n"
    )

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        resposta = client.models.generate_content(
            model=modelo,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=OrientadorSaida,
                temperature=0.0,
            ),
        )

        dados = OrientadorSaida.model_validate_json(resposta.text)

        # 1. Pós-validação da trilha: módulos DEVEM existir na trilha-base
        trilha_validada: List[ItemTrilha] = []
        for item in dados.trilha:
            chave = (item.curso, item.modulo)
            if chave not in modulos_base_map:
                # Módulo inventado pelo modelo: descarta a resposta inteira e usa Plano B
                return gerar_plano_b_templates(fatos)

            base_info = modulos_base_map[chave]
            # Validação numérica no motivo
            if not validar_anti_alucinacao_numerica(item.motivo, numeros_permitidos):
                item.motivo = f"Módulo cobrindo lacunas do mercado com foco prático."

            item.carga_horaria = base_info.get("carga_horaria")
            item.competencias_cobertas = base_info.get("competencias_cobertas")
            item.peso = base_info.get("peso")
            trilha_validada.append(item)

        # 2. Pós-validação dos insights: valida números e tamanho
        insights_validados: List[Insight] = []
        for ins in dados.insights[:3]:
            if len(ins.texto) > 280:
                continue
            # Verifica números em título e texto
            if not validar_anti_alucinacao_numerica(f"{ins.titulo} {ins.texto}", numeros_permitidos):
                continue
            ins.origem = "gemini"
            insights_validados.append(ins)

        if not insights_validados:
            # Se todos os insights forem descartados por números inválidos, usa Plano B
            return gerar_plano_b_templates(fatos)

        return OrientadorSaida(
            insights=insights_validados,
            trilha=trilha_validada if trilha_validada else [
                ItemTrilha(
                    curso=b["curso"],
                    modulo=b["modulo"],
                    motivo="Módulo recomendado pela cobertura de lacunas de mercado.",
                    carga_horaria=b.get("carga_horaria"),
                    competencias_cobertas=b.get("competencias_cobertas"),
                    peso=b.get("peso"),
                )
                for b in trilha_base
            ],
        )

    except Exception:
        # Fallback determinístico seguro
        return gerar_plano_b_templates(fatos)
