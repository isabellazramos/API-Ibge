"""
Script para buscar indicadores das pesquisas do IBGE.

Faz requisições à API IBGE e salva os dados em formato JSON.
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import json
from typing import Optional

import config
from src.api import IBGEClient
from src.utils import setup_logging, ensure_directory_exists


logger = setup_logging(__name__)
DATA_DIR = ensure_directory_exists(config.DATA_DIR)


def fetch_indicadores(client: IBGEClient, research_ids: list[int]) -> int:
    """
    Busca indicadores para pesquisas específicas.
    
    Args:
        client: Cliente IBGE configurado
        research_ids: Lista de IDs de pesquisas
        
    Returns:
        Número de arquivos salvos
    """
    saved_count = 0
    
    for research_id in research_ids:
        logger.info(f"Processando pesquisa {research_id}...")
        
        indicadores = client.get_indicadores(research_id)
        if indicadores is None:
            logger.warning(f"Não foi possível buscar indicadores para pesquisa {research_id}")
            continue
        
        # Salvar em JSON
        output_file = DATA_DIR / f"indicadores-pesquisa-{research_id}.json"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(indicadores, f, ensure_ascii=False, indent=2)
            logger.info(f"Indicadores salvos em {output_file}")
            saved_count += 1
        except IOError as e:
            logger.error(f"Erro ao salvar arquivo {output_file}: {e}")
    
    return saved_count


def main() -> None:
    """Função principal."""
    logger.info("=== Iniciando busca de indicadores ===")
    
    try:
        with IBGEClient() as client:
            count = fetch_indicadores(client, config.RESEARCH_IDS)
            logger.info(f"=== Processo concluído: {count} arquivo(s) salvo(s) ===")
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
