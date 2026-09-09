-- Habilite chaves estrangeiras em cada conexão SQLite com:
-- PRAGMA foreign_keys = ON;

-- Uma sequência temporal de medições.
CREATE TABLE IF NOT EXISTS serie (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único da série.
    name TEXT NOT NULL,                   -- Nome ou código que identifica a série.
    description TEXT                      -- Descrição da série.
);

-- Uma condição de operação ou tipo de falha aplicável a uma série.
CREATE TABLE IF NOT EXISTS condicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único da condição.
    name TEXT NOT NULL UNIQUE,             -- Nome da condição ou tipo de falha.
    description TEXT                       -- Descrição da condição.
);

INSERT OR IGNORE INTO condicao (name, description) VALUES ('falha', ''),
('normal', ''),('bearing fault', ''),('ball fault', ''),('outer race', '')
,('cage fault', ''),('misalignment', ''),('horizontal misalignment', ''),
('vertical misalignment', ''),('imbalance', ''),('underhang',''),('overhang','');

-- Condições que caracterizam uma série.
CREATE TABLE IF NOT EXISTS serie_condicao (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único da associação.
    serie INTEGER NOT NULL,               -- Série à qual a condição se aplica.
    condicao INTEGER NOT NULL,            -- Condição ou tipo de falha associado.
    graduacao REAL,                       -- Intensidade ou grau da condição.
    description TEXT,                     -- Observações específicas desta condição na série.
    FOREIGN KEY (serie) REFERENCES serie (id) ON DELETE CASCADE,
    FOREIGN KEY (condicao) REFERENCES condicao (id) ON DELETE RESTRICT,
    UNIQUE (serie, condicao)
);



-- Tipo de sensor
CREATE TABLE IF NOT EXISTS sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único do sensor.
    name TEXT,                            -- Nome do sensor.
    description TEXT                      -- Descrição do sensor.
);

INSERT OR IGNORE INTO sensor (name, description) VALUES('tacometro', ''),('acelerometro 1 X', ''),
('acelerometro 1 Y', ''),('acelerometro 1 Z', ''),('acelerometro 2 X', ''),
('acelerometro 2 Y', ''),('acelerometro 2 Z', ''),('microfone', '');

-- Sequencias dos sensores
CREATE TABLE IF NOT EXISTS amostras (
    sensor INTEGER NOT NULL, -- Identificador do sensor associado à medição.
    serie INTEGER NOT NULL,  -- Identificador da série associada à medição.
    seq INTEGER NOT NULL,    -- Posição sequencial da medição na série.
    value REAL NOT NULL,     -- Instante da medição, em milissegundos.
    PRIMARY KEY (sensor, serie, seq),
    FOREIGN KEY (sensor) REFERENCES sensor (id) ON DELETE RESTRICT,
    FOREIGN KEY (serie) REFERENCES serie (id) ON DELETE CASCADE
) WITHOUT ROWID;

CREATE TABLE metrica (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	CONSTRAINT metricas_pk PRIMARY KEY (id)
);

CREATE TABLE estatistica (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL
);

INSERT INTO estatistica (name) VALUES
	 ('variancia'),
	 ('media'),
	 ('kurtosis');

CREATE TABLE estatistica_valor (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	value REAL NOT NULL,
	sample_start INTEGER,
	sample_end INTEGER,
	estatistica INTEGER NOT NULL
, serie INTEGER, sensor INTEGER);
-----------------------------------------------------------------
CREATE VIEW Variancia_Condicao AS 
SELECT avg(ev.value) as Valor, ss.name as Sensor, c.name as Condicao
FROM estatistica_valor ev 
INNER JOIN serie s ON s.id = ev.serie 
INNER JOIN serie_condicao sc ON sc.serie = ev.serie
INNER JOIN condicao c ON c.id = sc.condicao
INNER JOIN sensor ss ON ss.id = ev.sensor 
GROUP BY estatistica, sensor, sc.condicao , ss.id 
ORDER BY Sensor, Condicao;c
-----------------------------------------------------------------
CREATE VIEW Variancia_Serie AS
WITH valores AS (
    SELECT
        AVG(ev.value) AS Valor,
        ss.id AS Sensor,
        c.id AS CondicaoId,
        c.name AS Condicao,
        s.id AS Serie
    FROM estatistica_valor AS ev
    INNER JOIN serie AS s ON s.id = ev.serie
    INNER JOIN serie_condicao AS sc ON sc.serie = ev.serie
    INNER JOIN condicao AS c ON c.id = sc.condicao
    INNER JOIN sensor AS ss ON ss.id = ev.sensor
    INNER JOIN estatistica AS e ON e.id = ev.estatistica
    WHERE e.name = 'variancia'
    GROUP BY s.id, s.name, c.id, c.name, ss.id, ss.name
)
SELECT
    Serie,
    Condicao,
    MAX(CASE WHEN Sensor = 2 THEN Valor END) AS A1X,
    MAX(CASE WHEN Sensor = 3 THEN Valor END) AS A1Y,
    MAX(CASE WHEN Sensor = 4 THEN Valor END) AS A1Z,
    MAX(CASE WHEN Sensor = 5 THEN Valor END) AS A2X,
    MAX(CASE WHEN Sensor = 6 THEN Valor END) AS A2Y,
    MAX(CASE WHEN Sensor = 7 THEN Valor END) AS A2Z,
    MAX(CASE WHEN Sensor = 1 THEN Valor END) AS TAC,
    MAX(CASE WHEN Sensor = 8 THEN Valor END) AS MIC
FROM valores
GROUP BY Serie, CondicaoId, Condicao
ORDER BY Serie, Condicao;