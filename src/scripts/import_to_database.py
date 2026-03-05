"""
Script para importar resultados de CSV para o banco de dados.

Lê arquivos CSV processados e insere os dados no banco de dados.
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import gzip
import ast
from typing import Optional

import pandas as pd

import config
from src.database import DatabaseConnection, ResultadoRepository
from src.utils import setup_logging


logger = setup_logging(__name__)


def processar_resultado_csv(
    df_row: pd.Series,
    coluna: str,
    id_municipio: int,
    id_pesquisa: int
) -> Optional[dict]:
    """
    Processa um valor de resultado do dataframe.
    
    Args:
        df_row: Linha do dataframe
        coluna: Nome da coluna (indicador)
        id_municipio: ID do município
        id_pesquisa: ID da pesquisa
        
    Returns:
        Dicionário com dados formatados ou None se inválido
    """
    try:
        valor_str = df_row[coluna]
        if pd.isna(valor_str):
            return None
        
        # Parser do dicionário de resultados
        resultado_dict = ast.literal_eval(valor_str)
        
        records = []
        for ano, valor in resultado_dict.items():
            if valor is not None:
                records.append({
                    'id_cidade': int(id_municipio),
                    'id_pesquisa': int(id_pesquisa),
                    'periodo': int(ano),
                    'id_indicador': int(coluna),
                    'resultado': str(valor)
                })
        
        return records
    except (ValueError, SyntaxError, KeyError) as e:
        logger.error(f"Erro ao processar resultado: {e}")
        return None


def importar_pesquisa(
    db: DatabaseConnection,
    pesquisa_id: int,
    csv_file: Path
) -> int:
    """
    Importa dados de uma pesquisa específica.
    
    Args:
        db: Conexão com banco de dados
        pesquisa_id: ID da pesquisa
        csv_file: Caminho do arquivo CSV
        
    Returns:
        Número de registros importados
    """
    logger.info(f"Importando pesquisa {pesquisa_id} de {csv_file}...")
    
    try:
        # Carregar CSV (com compressão gzip se necessário)
        if csv_file.suffix == '.gz':
            with gzip.open(csv_file, 'rb') as f:
                df = pd.read_csv(f, index_col=0)
        else:
            df = pd.read_csv(csv_file, index_col=0)
        
        # Processar dados
        id_municipio = df['id']
        df = df.drop(columns=['id'])
        colunas = df.columns
        
        df = df.dropna()
        df = df.reset_index()
        
        # Preparar registros para inserção
        all_records = []
        
        for coluna in colunas:
            logger.debug(f"Processando indicador {coluna}...")
            
            for idx, row in df.iterrows():
                records = processar_resultado_csv(
                    row,
                    coluna,
                    id_municipio.iloc[idx],
                    pesquisa_id
                )
                
                if records:
                    all_records.extend(records)
        
        # Inserir no banco
        if all_records:
            with ResultadoRepository(db) as repo:
                inserted = repo.insert_batch('resultadov2', all_records)
                logger.info(f"Pesquisa {pesquisa_id}: {inserted} registros inseridos")
                return inserted
        else:
            logger.warning(f"Nenhum registro válido encontrado para pesquisa {pesquisa_id}")
            return 0
    
    except Exception as e:
        logger.error(f"Erro ao importar pesquisa {pesquisa_id}: {e}", exc_info=True)
        raise


def main() -> None:
    """Função principal."""
    logger.info("=== Iniciando importação para banco de dados ===")
    
    try:
        db = DatabaseConnection()
        
        # Procurar arquivos CSV
        csv_dir = config.RESULTS_DIR
        if not csv_dir.exists():
            logger.error(f"Diretório não encontrado: {csv_dir}")
            raise FileNotFoundError(f"Diretório {csv_dir} não existe")
        
        total_importados = 0
        
        for pesquisa_id in config.RESEARCH_IDS:
            csv_file = csv_dir / f"pesquisa{pesquisa_id}.csv"
            
            if not csv_file.exists():
                logger.warning(f"Arquivo não encontrado: {csv_file}")
                continue
            
            try:
                importados = importar_pesquisa(db, pesquisa_id, csv_file)
                total_importados += importados
            except Exception as e:
                logger.error(f"Falha ao importar pesquisa {pesquisa_id}: {e}")
                # Continuar com próximas pesquisas
                continue
        
        logger.info(f"=== Importação concluída: {total_importados} registros no banco ===")
    
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        raise
    finally:
        if 'db' in locals():
            db.close()


if __name__ == '__main__':
    main()
