import numpy as np
import psycopg


def query_data(query):
    with psycopg.connect("postgresql://admin:1234@localhost:5432/database") as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description is None:
                raise ValueError("A consulta não retornou colunas para exportar.")
            column_names = [column.name for column in cursor.description]
            rows = cursor.fetchall()
    return np.array(rows)