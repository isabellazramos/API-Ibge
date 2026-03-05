"""
Cliente para comunicação com a API do IBGE.

Fornece métodos para buscar dados de pesquisas, indicadores e resultados.
"""

import time
from typing import Any, Dict, List, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

import config


logger = logging.getLogger(__name__)


class IBGEClient:
    """
    Cliente para interagir com a API IBGE.
    
    Implementa estratégias de retry, timeout e tratamento de erros.
    """
    
    def __init__(self, timeout: int = config.REQUEST_TIMEOUT):
        """
        Inicializa o cliente IBGE.
        
        Args:
            timeout: Timeout em segundos para requisições
        """
        self.session = self._create_session()
        self.timeout = timeout
    
    @staticmethod
    def _create_session() -> requests.Session:
        """
        Cria uma sessão com estratégia de retry automático.
        
        Returns:
            Sessão configurada
        """
        session = requests.Session()
        
        retry_strategy = Retry(
            total=config.REQUEST_RETRIES,
            backoff_factor=config.REQUEST_RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _get(self, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Realiza uma requisição GET com tratamento de erros.
        
        Args:
            url: URL da requisição
            **kwargs: Argumentos adicionais para requests.get()
            
        Returns:
            Resposta JSON ou None se falhar
        """
        try:
            logger.debug(f"GET {url}")
            response = self.session.get(url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao fazer requisição para {url}: {e}")
            return None
    
    def get_pesquisas(self) -> Optional[List[Dict[str, Any]]]:
        """
        Obtém lista de todas as pesquisas.
        
        Returns:
            Lista de pesquisas ou None se falhar
        """
        logger.info("Buscando pesquisas...")
        return self._get(config.IBGE_ENDPOINTS["pesquisas"])
    
    def get_municipios(self) -> Optional[List[Dict[str, Any]]]:
        """
        Obtém lista de todos os municípios.
        
        Returns:
            Lista de municípios ou None se falhar
        """
        logger.info("Buscando municípios...")
        return self._get(config.IBGE_ENDPOINTS["municipios"])
    
    def get_indicadores(self, pesquisa_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Obtém indicadores de uma pesquisa específica.
        
        Args:
            pesquisa_id: ID da pesquisa
            
        Returns:
            Lista de indicadores ou None se falhar
        """
        url = config.IBGE_ENDPOINTS["indicadores"].format(
            base_url=config.IBGE_API_BASE_URL,
            pesquisa_id=pesquisa_id
        )
        logger.info(f"Buscando indicadores para pesquisa {pesquisa_id}...")
        return self._get(url)
    
    def get_resultado(self, pesquisa_id: int, municipio_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtém resultado de uma pesquisa para um município.
        
        Args:
            pesquisa_id: ID da pesquisa
            municipio_id: ID do município
            
        Returns:
            Resultado ou None se falhar
        """
        url = config.IBGE_ENDPOINTS["resultados"].format(
            base_url=config.IBGE_API_BASE_URL,
            pesquisa_id=pesquisa_id,
            municipio_id=municipio_id
        )
        return self._get(url)
    
    def close(self) -> None:
        """Fecha a sessão."""
        self.session.close()
    
    def __enter__(self):
        """Suporte para context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Suporte para context manager."""
        self.close()
