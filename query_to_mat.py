from os import getenv
from pathlib import Path

import numpy as np
import psycopg
from scipy.io import savemat


DATABASE_URL = getenv(
    "DATABASE_URL", "postgresql://admin:1234@localhost:5432/database"
)
OUTPUT_PATH = Path("Dados_Processados/normal_vs_under_ballfault.mat")

# Edite esta consulta conforme os dados que deseja exportar.
# A ordem dos aliases define as colunas da matriz; os nomes são salvos em parameter_names.
QUERY = """
with series as (
	select distinct serie_id
	from caracteristicas_limpo cl
	INNER JOIN condicao c ON c.id = cl.condicao_id
	where c.name IN ('normal', 'underhang ball fault')
),
treino as (
	select serie_id, 1 as treino
	from series
	order by RANDOM()
	limit (select count(*) * 0.8 from series)
),
teste as (
	select serie_id, 0 as treino
	from series
	where serie_id not in (select serie_id from treino)
	order by RANDOM()
),
series_rotuladas as (
	select * from treino
	union all
	select * from teste
)
SELECT treino,condicao_id,acel_x1_energia, acel_y1_energia, acel_z1_energia, acel_x2_energia, acel_y2_energia, acel_z2_energia, mic_energia
FROM caracteristicas_limpo cl
INNER JOIN condicao c ON c.id = cl.condicao_id
inner join series_rotuladas sr on sr.serie_id = cl.serie_id
"""

with psycopg.connect(DATABASE_URL) as connection:
    with connection.cursor() as cursor:
        cursor.execute(QUERY)
        if cursor.description is None:
            raise ValueError("A consulta não retornou colunas para exportar.")

        column_names = [column.name for column in cursor.description]
        rows = cursor.fetchall()

data = np.asarray(
    [
        [
            np.nan if value is None else float(value)
            for value in row
        ]
        for row in rows
    ],
    dtype=float,
).reshape(len(rows), len(column_names))
parameter_names = np.asarray(column_names, dtype=object).reshape(1, -1)

savemat(
    file_name=str(OUTPUT_PATH),
    mdict={
        "data": data,
        "parameter_names": parameter_names,
    },
)
print(f"{len(rows)} linha(s) salva(s) em {OUTPUT_PATH}")

