# 🇧🇷 API-IBGE - Sistema de Importação de Dados

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-ativo-brightgreen.svg)

Sistema automatizado e robusto para coleta, processamento e importação de dados da **API do IBGE** (Instituto Brasileiro de Geografia e Estatística) em banco de dados MySQL.

## 📋 O que este projeto faz

- ✅ **Coleta de dados** automatizada da API IBGE (pesquisas, indicadores, municípios)
- ✅ **Processamento inteligente** com retry automático e tratamento de erros
- ✅ **Importação em massa** otimizada para MySQL
- ✅ **Logging detalhado** para auditoria e debugging
- ✅ **Arquitetura modular** e fácil de extends

### Dados coletados
- **35+ pesquisas** diferentes (POF, PNAD, Censo, etc.)
- **~5.500 municípios** brasileiros
- **Séries temporais** com vários períodos e indicadores

---

## 🏗️ Estrutura do Projeto

```
API-Ibge/
├── src/                           # Código-fonte principal
│   ├── api/
│   │   └── client.py              # Cliente HTTP com retry automático
│   ├── database/
│   │   ├── connection.py          # Gerenciador de conexão (Singleton)
│   │   └── repository.py          # Operações em batch
│   ├── scripts/
│   │   ├── fetch_pesquisas_municipios.py  # Baixa lista de pesquisas e municípios
│   │   ├── fetch_indicadores.py           # Baixa indicadores por pesquisa
│   │   ├── fetch_resultados.py            # Baixa resultados por munícipio
│   │   └── import_to_database.py          # Importa CSV para MySQL
│   └── utils.py                   # Funções utilitárias
├── data/                          # JSONs baixados da API
├── resultados/                    # Arquivos CSV para importação
├── logs/                          # Logs de execução
├── config.py                      # Configuração centralizada
├── requirements.txt               # Dependências Python
├── .env.example                   # Template de variáveis de ambiente
├── database_schema.sql            # Schema do banco de dados
└── README.md
```

---

## 🔧 Requisitos

- **Python 3.11+**
- **MySQL 5.7+** ou **MariaDB 10.3+**
- **pip** (gerenciador de pacotes Python)

Verifique sua versão Python:
```bash
python --version
```

---

## 🚀 Instalação e Configuração

### 1️⃣ Clonar/Preparar o projeto
```bash
cd API-Ibge
```

### 2️⃣ Instalar dependências Python
```bash
pip install -r requirements.txt
```

**Dependências instaladas:**
- `requests` - cliente HTTP
- `sqlalchemy` - ORM de banco de dados
- `pymysql` - driver MySQL
- `pandas` - processamento de dados
- `numpy` - operações numéricas
- `python-dotenv` - variáveis de ambiente

### 3️⃣ Configurar variáveis de ambiente
```bash
# Criar arquivo .env a partir do template
cp .env.example .env
```

Edite ``.env`` com suas credenciais:
```env
DB_HOST=localhost        # Host do MySQL
DB_PORT=3306            # Porta do MySQL
DB_USER=seu_usuario     # Usuário do MySQL
DB_PASSWORD=sua_senha   # Senha do MySQL
DB_NAME=seu_banco       # Nome do banco
LOG_LEVEL=INFO          # Nível de log (DEBUG, INFO, WARNING, ERROR)
```

### 4️⃣ Criar banco de dados
```bash
# Abra o arquivo database_schema.sql
# Customize com suas credenciais
# Execute no MySQL:

mysql -u seu_usuario -p < database_schema.sql
```

---

## 📡 Como usar

### Método 1: Scripts individuais (passo a passo)

**Passo 1:** Baixar pesquisas e municípios
```bash
python src/scripts/fetch_pesquisas_municipios.py
```
✅ Cria: `data/pesquisas.json`, `data/municipios.json`

**Passo 2:** Baixar indicadores
```bash
python src/scripts/fetch_indicadores.py
```
✅ Cria: `data/indicadores-pesquisa-{id}.json` (um por pesquisa)

**Passo 3:** Baixar resultados por município
```bash
python src/scripts/fetch_resultados.py
```
⚠️ Atenção: Este script é longo! Pode levar horas (~5.500 municípios × 35 pesquisas)

**Passo 4:** Importar para o banco de dados
```bash
python src/scripts/import_to_database.py
```
✅ Popula as tabelas MySQL com os dados

---

## 📊 Entender os dados

### Arquivos gerados

| Arquivo | Descrição | Tamanho esperado |
|---------|-----------|-----------------|
| `pesquisas.json` | Lista de pesquisas disponíveis | ~50 KB |
| `municipios.json` | Lista de ~5.500 municípios | ~200 KB |
| `indicadores-pesquisa-*.json` | Indicadores por pesquisa | Varia |
| `resultado-pesquisa-*.json` | Resultados por pesquisa/município | Centenas MB |
| `pesquisa*.csv` | CSVs processados do `resultados/` | Varia |

### Estrutura de dados no MySQL

**Tabela:** `resultadov2`

```sql
CREATE TABLE resultadov2 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pesquisa_id INT NOT NULL,
    municipio_id INT NOT NULL,
    indicador_id INT,
    valor DECIMAL(12, 2),
    periodo INT,
    FOREIGN KEY (pesquisa_id) REFERENCES pesquisas(id),
    FOREIGN KEY (municipio_id) REFERENCES municipios(id)
);
```

---

## 🔍 Monitoramento e Logs

### Ver logs em tempo real

**Linux/Mac:**
```bash
tail -f logs/api_ibge.log
```

**Windows (PowerShell):**
```powershell
Get-Content logs/api_ibge.log -Wait
```

### Estrutura dos logs
```
2026-03-04 22:00:10,999 - __main__ - INFO - === Iniciando busca de indicadores ===
2026-03-04 22:00:12,010 - __main__ - INFO - Indicadores salvos em ./data/indicadores-pesquisa-11.json
2026-03-04 22:00:15,050 - __main__ - WARNING - Pesquisa 19 indisponível (HTTP 400)
```

### Configurar nível de log
Edite `.env`:
```env
LOG_LEVEL=DEBUG      # Mostrar tudo
LOG_LEVEL=INFO       # Informações gerais
LOG_LEVEL=WARNING    # Apenas alertas
LOG_LEVEL=ERROR      # Apenas erros
```



## 📚 Exemplos de uso avançado

### Usar o cliente IBGE em seu próprio código
```python
from src.api.client import IBGEClient

client = IBGEClient()

# Baixar pesquisas
pesquisas = client.get_pesquisas()

# Baixar municipios
municipios = client.get_municipios()

# Baixar indicadores específicos
indicadores = client.get_indicadores(pesquisa_id=11)

# Baixar resultado específico
resultado = client.get_resultado(pesquisa_id=11, municipio_id=3550308)
```


