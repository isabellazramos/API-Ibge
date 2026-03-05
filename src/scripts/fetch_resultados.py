"""
Script para buscar resultados de pesquisas por município do IBGE.

Faz requisições à API IBGE para cada combinação de pesquisa e município
e salva os dados em formato JSON.
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


def fetch_resultados(
    client: IBGEClient,
    research_ids: list[int],
    municipio_ids: list[int],
    max_retries: int = 3
) -> dict[int, int]:
    """
    Busca resultados para todas as combinações de pesquisas e municípios.
    
    Args:
        client: Cliente IBGE configurado
        research_ids: Lista de IDs de pesquisas
        municipio_ids: Lista de IDs de municípios
        max_retries: Número máximo de tentativas por requisição
        
    Returns:
        Dicionário com pesquisa_id e número de municípios processados
    """
    resultados_por_pesquisa = {}
    
    for research_id in research_ids:
        logger.info(f"Processando pesquisa {research_id}...")
        resultados = []
        municipios_processados = 0
        
        for municipio_id in municipio_ids:
            resultado = client.get_resultado(research_id, municipio_id)
            
            if resultado is None:
                # Se falhar, provavelmente essa pesquisa não tem dados para este município
                continue
            
            resultados.append({municipio_id: resultado})
            municipios_processados += 1
            
            # Log de progresso a cada 100 municípios
            if municipios_processados % 100 == 0:
                logger.debug(f"Pesquisa {research_id}: {municipios_processados} municípios processados")
        
        # Salvar em JSON
        if resultados:
            output_file = DATA_DIR / f"resultado-pesquisa-{research_id}.json"
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(resultados, f, ensure_ascii=False, indent=2)
                logger.info(f"Salvos {municipios_processados} resultados para pesquisa {research_id}")
                resultados_por_pesquisa[research_id] = municipios_processados
            except IOError as e:
                logger.error(f"Erro ao salvar arquivo {output_file}: {e}")
        else:
            logger.warning(f"Nenhum resultado encontrado para pesquisa {research_id}")
    
    return resultados_por_pesquisa


def main() -> None:
    """Função principal."""
    logger.info("=== Iniciando busca de resultados ===")
    
    try:
        with IBGEClient() as client:
            # Primeiro, buscar lista de municípios
            municipios = client.get_municipios()
            if not municipios:
                logger.error("Não foi possível buscar lista de municípios")
                raise RuntimeError("Dados de municípios não obtidos")
            
            municipio_ids = [m['id'] for m in municipios]
            logger.info(f"Total de municípios: {len(municipio_ids)}")
            
            # Buscar resultados
            resultados = fetch_resultados(
                client,
                config.RESEARCH_IDS,
                municipio_ids
            )
            
            total_processados = sum(resultados.values())
            logger.info(f"=== Processo concluído: {total_processados} registros salvos ===")
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
