"""
Utilitários e funções auxiliares reutilizáveis.
"""

import logging
from typing import Optional
from pathlib import Path
import sys

import config


def setup_logging(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Configura logging para um módulo.
    
    Args:
        name: Nome do logger (geralmente __name__)
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Logger configurado
    """
    log_level = getattr(logging, level or config.LOG_LEVEL)
    
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(config.LOG_FORMAT))
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(config.LOG_FORMAT))
    
    # Evitar handlers duplicados
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def ensure_directory_exists(path: Path) -> Path:
    """
    Garante que um diretório existe.
    
    Args:
        path: Caminho do diretório
        
    Returns:
        Caminho confirmado
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
