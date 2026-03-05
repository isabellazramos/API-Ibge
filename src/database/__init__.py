"""Módulo para operações com banco de dados."""

from .connection import DatabaseConnection
from .repository import ResultadoRepository

__all__ = ["DatabaseConnection", "ResultadoRepository"]
