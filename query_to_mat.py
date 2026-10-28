import argparse
from os import getenv
from pathlib import Path

import numpy as np
import psycopg
from scipy.io import savemat


DATABASE_URL = getenv(
    "DATABASE_URL", "postgresql://admin:1234@localhost:5432/database"
)

parser = argparse.ArgumentParser(
    description="Executa uma consulta SQL e salva o resultado em um arquivo .mat."
)
parser.add_argument(
    "-q",
    "--query",
    dest="query_path",
    type=Path,
    default=Path(__file__).resolve().parent / "query.sql",
    help="Caminho do arquivo .sql (padrão: query.sql na pasta do script)",
)
parser.add_argument(
    "-o",
    "--output",
    dest="output_path",
    type=Path,
    required=True,
    help="Caminho/nome do arquivo .mat de saída",
)
args = parser.parse_args()

query = args.query_path.read_text(encoding="utf-8")

with psycopg.connect(DATABASE_URL) as connection:
    with connection.cursor() as cursor:
        cursor.execute(query)
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

args.output_path.parent.mkdir(parents=True, exist_ok=True)
savemat(
    file_name=str(args.output_path),
    mdict={
        "data": data,
        "parameter_names": parameter_names,
    },
)
print(f"{len(rows)} linha(s) salva(s) em {args.output_path}")

