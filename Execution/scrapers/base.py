# Execution/scrapers/base.py
# Classe BaseScraper com governança de scraping, robots.txt, retry e intervalo.

import time
import urllib.parse
import urllib.robotparser
from typing import Optional, List, Dict, Any
import requests

USER_AGENT_PADRAO = "SkillRadarBot/1.0 (projeto educacional SENAI Ourinhos)"


class BaseScraper:
    """
    Classe base para scrapers do SkillRadar.
    Implementa leitura de robots.txt, User-Agent identificado,
    intervalo mínimo de 2 segundos, timeouts e retries com backoff.
    """

    def __init__(
        self,
        user_agent: str = USER_AGENT_PADRAO,
        intervalo_segundos: float = 2.0,
        timeout: float = 15.0,
        max_retries: int = 3,
    ):
        self.user_agent = user_agent
        self.intervalo_segundos = intervalo_segundos
        self.timeout = timeout
        self.max_retries = max_retries

        # Cache de robots.txt indexado por netloc (domínio:porta)
        self._robots_cache: Dict[str, urllib.robotparser.RobotFileParser] = {}
        # Marcação do último timestamp de requisição por netloc
        self._ultimo_acesso: Dict[str, float] = {}

    def registrar_robots_em_memoria(self, netloc: str, robots_txt: str) -> None:
        """
        Registra conteúdo de robots.txt em memória para um domínio.
        Útil para testes offline e simulações sem acesso à rede.
        """
        rfp = urllib.robotparser.RobotFileParser()
        rfp.parse(robots_txt.splitlines())
        self._robots_cache[netloc] = rfp

    def obter_robot_parser(self, url: str) -> urllib.robotparser.RobotFileParser:
        """
        Retorna o RobotFileParser para o domínio da URL, utilizando cache.
        Faz download do robots.txt apenas se não estiver em cache.
        """
        parsed = urllib.parse.urlparse(url)
        netloc = parsed.netloc

        if netloc in self._robots_cache:
            return self._robots_cache[netloc]

        robots_url = f"{parsed.scheme}://{netloc}/robots.txt"
        rfp = urllib.robotparser.RobotFileParser()
        rfp.set_url(robots_url)

        try:
            # Aplica User-Agent na leitura do robots.txt
            resp = requests.get(
                robots_url,
                headers={"User-Agent": self.user_agent},
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                rfp.parse(resp.text.splitlines())
            elif resp.status_code in (401, 403):
                # Se robots.txt é proibido, por precaução ética desautoriza
                rfp.disallow_all = True
            else:
                # 404 indica ausência de restrições de robots.txt
                rfp.allow_all = True
        except Exception:
            # Em caso de falha de conexão com robots.txt, assume restritivo para segurança
            rfp.disallow_all = True

        self._robots_cache[netloc] = rfp
        return rfp

    def pode_coletar(self, url: str, robots_txt_content: Optional[str] = None) -> bool:
        """
        Verifica se a URL pode ser coletada segundo as regras do robots.txt.
        Aceita opcionalmente robots_txt_content para validação offline/teste.
        """
        parsed = urllib.parse.urlparse(url)
        netloc = parsed.netloc

        if robots_txt_content is not None:
            self.registrar_robots_em_memoria(netloc, robots_txt_content)

        rfp = self.obter_robot_parser(url)
        return rfp.can_fetch(self.user_agent, url)

    def _aguardar_intervalo(self, netloc: str) -> None:
        """
        Garante intervalo mínimo entre requisições ao mesmo domínio.
        """
        agora = time.time()
        ultimo = self._ultimo_acesso.get(netloc, 0.0)
        tempo_decorrido = agora - ultimo

        if tempo_decorrido < self.intervalo_segundos:
            tempo_espera = self.intervalo_segundos - tempo_decorrido
            time.sleep(tempo_espera)

    def baixar(self, url: str) -> str:
        """
        Baixa o conteúdo HTML da URL respeitando robots.txt, intervalo e retries.
        """
        if not self.pode_coletar(url):
            raise PermissionError(
                f"Acesso proibido pelas diretivas do robots.txt para a URL: {url}"
            )

        parsed = urllib.parse.urlparse(url)
        netloc = parsed.netloc

        for tentativa in range(1, self.max_retries + 1):
            self._aguardar_intervalo(netloc)
            try:
                self._ultimo_acesso[netloc] = time.time()
                resp = requests.get(
                    url,
                    headers={"User-Agent": self.user_agent},
                    timeout=self.timeout,
                )

                # Se o site responder 403 ou 429, não insiste (regra inegociável §2.5)
                if resp.status_code in (403, 429):
                    raise ConnectionRefusedError(
                        f"Site bloqueou requisição (Status HTTP {resp.status_code}). Interrompendo coleta."
                    )

                resp.raise_for_status()
                return resp.text

            except ConnectionRefusedError:
                raise
            except requests.RequestException as e:
                if tentativa == self.max_retries:
                    raise ConnectionError(
                        f"Falha ao baixar URL após {self.max_retries} tentativas: {url}. Erro: {e}"
                    )
                # Espera crescente (backoff linear) antes da próxima tentativa
                time.sleep(tentativa * 2.0)

        raise ConnectionError(f"Não foi possível obter resposta para: {url}")

    def extrair(self, html: str) -> List[Dict[str, Any]]:
        """
        Método abstrato de extração de vagas a partir do HTML.
        Deve ser implementado pelas subclasses de cada fonte.
        """
        raise NotImplementedError("Subclasses de BaseScraper devem implementar extrair().")

    def coletar(self, url: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Orquestra o download e a extração dos dados brutos de vagas.
        """
        alvo = url or getattr(self, "url_base", None)
        if not alvo:
            raise ValueError("URL não especificada para a coleta.")
        html = self.baixar(alvo)
        return self.extrair(html)
