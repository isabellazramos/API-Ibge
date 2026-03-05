"""
Repositório para operações com a tabela de resultados.
"""

import logging
import ast
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session as SQLAlchemySession

from .connection import DatabaseConnection


logger = logging.getLogger(__name__)


class ResultadoRepository:
    """
    Repositório para manipular dados de resultados no banco de dados.
    
    Implementa padrão repository para abstrair lógica de acesso a dados.
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        Inicializa o repositório.
        
        Args:
            db_connection: Instância de DatabaseConnection
        """
        self.db = db_connection
        self.session = None
    
    def __enter__(self):
        """Suporte para context manager."""
        self.session = self.db.get_session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Suporte para context manager."""
        if self.session:
            self.session.close()
    
    def insert_batch(self, table_name: str, records: List[Dict[str, Any]]) -> int:
        """
        Insere um lote de registros no banco.
        
        Args:
            table_name: Nome da tabela
            records: Lista de dicionários com dados
            
        Returns:
            Número de registros inseridos
        """
        if not records:
            logger.warning("Nenhum registro para inserir")
            return 0
        
        try:
            if self.session is None:
                self.session = self.db.get_session()
            
            # Usar bulk insert para melhor performance
            self.session.execute(
                self.db.get_table(table_name).insert(),
                records
            )
            self.session.commit()
            
            logger.info(f"Inseridos {len(records)} registros na tabela '{table_name}'")
            return len(records)
        except Exception as e:
            if self.session:
                self.session.rollback()
            logger.error(f"Erro ao inserir registros: {e}")
            raise
    
    def parse_resultado_dict(self, dict_str: str) -> Optional[Dict[str, Any]]:
        """
        Parseia string de dicionário em Python.
        
        Args:
            dict_str: String representando um dicionário
            
        Returns:
            Dicionário parseado ou None se falhar
        """
        try:
            return ast.literal_eval(dict_str)
        except (ValueError, SyntaxError) as e:
            logger.error(f"Erro ao parsear dicionário: {e}")
            return None
