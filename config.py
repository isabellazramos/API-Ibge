"""
Arquivo de configuração centralizado para o projeto API-IBGE.

Este módulo contém todas as constantes e configurações utilizadas
no projeto, permitindo fácil gerenciamento de parâmetros.
"""

import os
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "resultados"
LOGS_DIR = BASE_DIR / "logs"

# Criar diretórios se não existirem
for directory in [DATA_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Banco de Dados
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "usuario"),
    "password": os.getenv("DB_PASSWORD", "senha"),
    "database": os.getenv("DB_NAME", "banco"),
}

DB_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# API IBGE
IBGE_API_BASE_URL = "https://servicodados.ibge.gov.br/api/v1"
IBGE_ENDPOINTS = {
    "pesquisas": f"{IBGE_API_BASE_URL}/pesquisas",
    "municipios": f"{IBGE_API_BASE_URL}/localidades/municipios",
    "indicadores": "{base_url}/pesquisas/{pesquisa_id}/indicadores/",
    "resultados": "{base_url}/pesquisas/{pesquisa_id}/resultados/{municipio_id}",
}

# IDs de Pesquisas
RESEARCH_IDS = [
    11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 231, 233, 234, 235, 232,
    29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43,
    10075, 10077, 10078, 10084, 10087
]

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "api_ibge.log"

# Request
REQUEST_TIMEOUT = 30
REQUEST_RETRIES = 3
REQUEST_RETRY_DELAY = 5
