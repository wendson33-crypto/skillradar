# Execution/scrapers/fonte_vagas_1.py
# Implementação de scraper de fonte de vagas com seletores isolados.

import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup

try:
    from zoneinfo import ZoneInfo
    TZ_SP = ZoneInfo("America/Sao_Paulo")
except Exception:
    TZ_SP = None

from Execution.scrapers.base import BaseScraper


class FonteVagasPortalRegional(BaseScraper):
    """
    Scraper para portal regional de vagas (Ourinhos e região).
    Centraliza todos os seletores HTML em um único dicionário para fácil manutenção.
    """

    # Centralização dos seletores HTML
    SELETORES = {
        "container_vagas": ".card-vaga, .job-item, article.vaga",
        "titulo": ".titulo-vaga, .job-title, h2.cargo",
        "empresa": ".empresa, .company-name, .nome-empresa",
        "cidade": ".cidade, .job-location, .localidade",
        "data": ".data-publicacao, .job-date, time",
        "salario": ".salario, .job-salary, .faixa-salarial",
        "requisitos": ".requisitos, .job-description, .descricao-vaga",
        "link": "a.link-vaga, a.job-link",
    }

    def __init__(self, url_base: str = "https://vagas.ourinhoseregiao.com.br/vagas", **kwargs):
        super().__init__(**kwargs)
        self.url_base = url_base

    @staticmethod
    def _extrair_salario(texto_salario: Optional[str]) -> tuple[Optional[int], Optional[int]]:
        """
        Extrai salário mínimo e máximo em inteiros de uma string salarial.
        Retorna (None, None) se ausente, 'A combinar' ou não numérico.
        NUNCA retorna 0 (diretiva §5 e §9).
        """
        if not texto_salario:
            return None, None

        texto_limpo = texto_salario.lower().strip()
        if "combinar" in texto_limpo or "confidencial" in texto_limpo or not texto_limpo:
            return None, None

        # Encontra valores numéricos como 3500, 3.500, 3500,00 etc.
        # Remove R$, espaços e converte pontuações brasileiras
        padrao = r"(?:r\$\s*)?([\d\.]+)(?:,\d{2})?"
        valores = []
        for match in re.finditer(padrao, texto_limpo):
            val_str = match.group(1).replace(".", "")
            if val_str.isdigit():
                val_int = int(val_str)
                if val_int > 0:  # Salário 0 é inválido conforme diretiva
                    valores.append(val_int)

        if not valores:
            return None, None
        if len(valores) == 1:
            return valores[0], valores[0]
        return min(valores), max(valores)

    @staticmethod
    def _extrair_data(texto_data: Optional[str], data_referencia: Optional[datetime] = None) -> str:
        """
        Converte representações de data em string para o formato ISO AAAA-MM-DD.
        Suporta 'há X dias', 'hoje', 'ontem' ou formato direto DD/MM/AAAA.
        """
        agora = data_referencia or (datetime.now(TZ_SP) if TZ_SP else datetime.now())
        if not texto_data:
            return agora.strftime("%Y-%m-%d")

        texto_limpo = texto_data.lower().strip()

        if "hoje" in texto_limpo:
            return agora.strftime("%Y-%m-%d")
        if "ontem" in texto_limpo:
            return (agora - timedelta(days=1)).strftime("%Y-%m-%d")

        match_dias = re.search(r"h[aá]\s+(\d+)\s+dias?", texto_limpo)
        if match_dias:
            dias = int(match_dias.group(1))
            return (agora - timedelta(days=dias)).strftime("%Y-%m-%d")

        # Procura formato DD/MM/AAAA ou AAAA-MM-DD
        match_iso = re.search(r"(\d{4})-(\d{2})-(\d{2})", texto_limpo)
        if match_iso:
            return f"{match_iso.group(1)}-{match_iso.group(2)}-{match_iso.group(3)}"

        match_br = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", texto_limpo)
        if match_br:
            dia, mes, ano = match_br.groups()
            return f"{ano}-{int(mes):02d}-{int(dia):02d}"

        return agora.strftime("%Y-%m-%d")

    def extrair(self, html: str) -> List[Dict[str, Any]]:
        """
        Faz o parse do HTML e retorna a lista de registros brutos de vagas.
        """
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(self.SELETORES["container_vagas"])
        agora_iso = (datetime.now(TZ_SP) if TZ_SP else datetime.now()).isoformat()

        registros: List[Dict[str, Any]] = []

        for card in cards:
            el_titulo = card.select_one(self.SELETORES["titulo"])
            el_empresa = card.select_one(self.SELETORES["empresa"])
            el_cidade = card.select_one(self.SELETORES["cidade"])
            el_data = card.select_one(self.SELETORES["data"])
            el_salario = card.select_one(self.SELETORES["salario"])
            el_req = card.select_one(self.SELETORES["requisitos"])
            el_link = card.select_one(self.SELETORES["link"])

            titulo = el_titulo.get_text(strip=True) if el_titulo else "Vaga sem título"
            empresa = el_empresa.get_text(strip=True) if el_empresa else "Empresa Confidencial"
            cidade = el_cidade.get_text(strip=True) if el_cidade else "Ourinhos/SP"
            texto_data = el_data.get_text(strip=True) if el_data else None
            texto_salario = el_salario.get_text(strip=True) if el_salario else None
            texto_req = el_req.get_text(separator=" ", strip=True) if el_req else ""

            link_href = el_link.get("href", "") if el_link else ""
            if link_href.startswith("/"):
                fonte_url = self.url_base.rstrip("/") + link_href
            elif link_href.startswith("http"):
                fonte_url = link_href
            else:
                fonte_url = self.url_base

            sal_min, sal_max = self._extrair_salario(texto_salario)
            data_iso = self._extrair_data(texto_data)

            registro = {
                "titulo": titulo,
                "empresa": empresa,
                "cidade": cidade,
                "data": data_iso,
                "salario_min": sal_min,
                "salario_max": sal_max,
                "fonte_url": fonte_url,
                "requisitos_texto": texto_req,
                "coletado_em": agora_iso,
            }
            registros.append(registro)

        return registros
