"""
Script para buscar pesquisas e municípios do IBGE.

Faz requisições à API IBGE e salva os dados em formato JSON.
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import json

import config
from src.api import IBGEClient
from src.utils import setup_logging, ensure_directory_exists


logger = setup_logging(__name__)
DATA_DIR = ensure_directory_exists(config.DATA_DIR)


def fetch_pesquisas_e_municipios() -> bool:
    """
    Busca pesquisas e municípios da API IBGE.
    
    Returns:
        True se bem-sucedido, False caso contrário
    """
    logger.info("Buscando pesquisas e municípios...")
    
    try:
        with IBGEClient() as client:
            # Buscar pesquisas
            pesquisas = client.get_pesquisas()
            if pesquisas is None:
                logger.error("Não foi possível buscar pesquisas")
                return False
            
            # Buscar municípios
            municipios = client.get_municipios()
            if municipios is None:
                logger.error("Não foi possível buscar municípios")
                return False
            
            # Salvar em JSON
            pesquisas_file = DATA_DIR / "pesquisas.json"
            municipios_file = DATA_DIR / "municipios.json"
            
            with open(pesquisas_file, 'w', encoding='utf-8') as f:
                json.dump(pesquisas, f, ensure_ascii=False, indent=2)
            logger.info(f"Pesquisas salvas em {pesquisas_file}")
            
            with open(municipios_file, 'w', encoding='utf-8') as f:
                json.dump(municipios, f, ensure_ascii=False, indent=2)
            logger.info(f"Municípios salvo em {municipios_file}")
            
            return True
    except Exception as e:
        logger.error(f"Erro ao buscar pesquisas e municípios: {e}", exc_info=True)
        return False


def main() -> None:
    """Função principal."""
    logger.info("=== Iniciando busca de pesquisas e municípios ===")
    
    if fetch_pesquisas_e_municipios():
        logger.info("=== Processo concluído com sucesso ===")
    else:
        logger.error("=== Processo falhou ===")
        raise RuntimeError("Não foi possível buscar dados")


if __name__ == '__main__':
    main()
