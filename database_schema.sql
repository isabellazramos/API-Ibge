/**
 * Script de criação das tabelas do banco de dados.
 * Configure seu banco de dados em .env antes de executar.
 */

-- Criar banco de dados com seu nome
-- CREATE DATABASE IF NOT EXISTS seu_banco;
-- USE seu_banco;

-- Após criar o banco de dados, descomente a criação da primeira tabela
-- e execute este script no seu banco de dados:
CREATE TABLE IF NOT EXISTS periodo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ano INT NOT NULL UNIQUE,
    descricao VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ano (ano)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de pesquisas
CREATE TABLE IF NOT EXISTS pesquisa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pesquisa INT NOT NULL UNIQUE,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_id_pesquisa (id_pesquisa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de indicadores
CREATE TABLE IF NOT EXISTS indicador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_indicador INT NOT NULL UNIQUE,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_id_indicador (id_indicador)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de relacionamento pesquisa-indicador-período
CREATE TABLE IF NOT EXISTS indicador_pesquisa_periodo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pesquisa INT NOT NULL,
    id_indicador INT NOT NULL,
    id_periodo INT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_pesquisa_indicador_periodo 
        (id_pesquisa, id_indicador, id_periodo),
    FOREIGN KEY (id_pesquisa) REFERENCES pesquisa(id),
    FOREIGN KEY (id_indicador) REFERENCES indicador(id),
    FOREIGN KEY (id_periodo) REFERENCES periodo(id),
    INDEX idx_id_pesquisa (id_pesquisa),
    INDEX idx_id_indicador (id_indicador),
    INDEX idx_id_periodo (id_periodo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de municípios
CREATE TABLE IF NOT EXISTS municipio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_municipio INT NOT NULL UNIQUE,
    nome VARCHAR(255) NOT NULL,
    uf VARCHAR(2),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_id_municipio (id_municipio),
    INDEX idx_uf (uf)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela PRINCIPAL: Resultados (versão otimizada v2)
CREATE TABLE IF NOT EXISTS resultadov2 (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_cidade INT NOT NULL,
    id_pesquisa INT NOT NULL,
    periodo INT NOT NULL,
    id_indicador INT NOT NULL,
    resultado VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices para performance
    INDEX idx_cidade (id_cidade),
    INDEX idx_pesquisa (id_pesquisa),
    INDEX idx_periodo (periodo),
    INDEX idx_indicador (id_indicador),
    INDEX idx_pesquisa_periodo (id_pesquisa, periodo),
    INDEX idx_cidade_pesquisa_periodo (id_cidade, id_pesquisa, periodo),
    
    -- Foreign keys (opcional, pode impactar performance)
    -- FOREIGN KEY (id_cidade) REFERENCES municipio(id_municipio),
    -- FOREIGN KEY (id_pesquisa) REFERENCES pesquisa(id_pesquisa),
    -- FOREIGN KEY (id_indicador) REFERENCES indicador(id_indicador),
    -- FOREIGN KEY (periodo) REFERENCES periodo(ano)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela de resultados (versão original para compatibilidade)
CREATE TABLE IF NOT EXISTS resultado (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_cidade INT NOT NULL,
    id_indicador_pesquisa_periodo INT NOT NULL,
    resultado VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_cidade (id_cidade),
    INDEX idx_indicador_pesquisa_periodo (id_indicador_pesquisa_periodo),
    
    FOREIGN KEY (id_indicador_pesquisa_periodo) 
        REFERENCES indicador_pesquisa_periodo(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/**
 * ANÁLISES E QUERIES ÚTEIS
 */

-- Ver estatísticas de resultados
-- SELECT 
--     COUNT(*) as total_registros,
--     COUNT(DISTINCT id_cidade) as cidades_unicas,
--     COUNT(DISTINCT id_pesquisa) as pesquisas_unicas,
--     COUNT(DISTINCT id_indicador) as indicadores_unicos,
--     COUNT(DISTINCT periodo) as periodos_unicos
-- FROM resultadov2;

-- Ver distribuição por pesquisa
-- SELECT id_pesquisa, COUNT(*) as registros
-- FROM resultadov2
-- GROUP BY id_pesquisa
-- ORDER BY registros DESC;

-- Ver data de maior importação
-- SELECT DATE(criado_em) as data, COUNT(*) as registros
-- FROM resultadov2
-- GROUP BY DATE(criado_em)
-- ORDER BY data DESC
-- LIMIT 10;
