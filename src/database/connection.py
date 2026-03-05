"""
Gerenciamento de conexão com banco de dados.
"""

import logging
from typing import Any, List, Optional
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession

import config


logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Gerenciador de conexão com banco de dados MySQL.
    
    Implementa padrão singleton e context manager.
    """
    
    _instance = None
    
    def __new__(cls, url: Optional[str] = None):
        """Implementa singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, url: Optional[str] = None):
        """
        Inicializa a conexão com o banco.
        
        Args:
            url: URL de conexão (usa config.DB_URL por padrão)
        """
        if self._initialized:
            return
        
        self.url = url or config.DB_URL
        
        try:
            logger.info(f"Conectando ao banco de dados: {self.url.split('@')[1]}")
            self.engine = create_engine(self.url, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine)
            self.metadata = MetaData()
            self.metadata.reflect(bind=self.engine)
            
            # Testar conexão
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            
            logger.info("Conexão com banco de dados estabelecida com sucesso")
            self._initialized = True
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            self._initialized = False
            raise
    
    def get_session(self) -> SQLAlchemySession:
        """
        Retorna uma nova sessão.
        
        Returns:
            Sessão SQLAlchemy
        """
        return self.SessionLocal()
    
    def get_table(self, table_name: str) -> Table:
        """
        Obtém uma tabela do banco.
        
        Args:
            table_name: Nome da tabela
            
        Returns:
            Objeto Table
        """
        if table_name not in self.metadata.tables:
            self.metadata.reflect(bind=self.engine)
        
        return self.metadata.tables.get(table_name)
    
    def get_table_names(self) -> List[str]:
        """
        Retorna nomes de todas as tabelas.
        
        Returns:
            Lista de nomes de tabelas
        """
        return self.engine.table_names()
    
    def close(self) -> None:
        """Fecha a conexão."""
        if hasattr(self, 'engine'):
            self.engine.dispose()
            logger.info("Conexão com banco de dados fechada")
    
    def __enter__(self):
        """Suporte para context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Suporte para context manager."""
        self.close()
