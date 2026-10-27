from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from os import getenv
from pathlib import Path
from typing import Any, get_args

import psycopg

from classes.dataset.hmisali import HM_LVL, Hmisali
from classes.dataset.imbalance import IM_LVL, Imbalance
from classes.dataset.normal import Normal
from classes.dataset.overhang import OH_LVL, OH_TIPE, Overhang
from classes.dataset.underhang import UN_LVL, UN_TIPE, Underhang
from classes.dataset.vmisali import VM_LVL, Vmisali


DEFAULT_DATABASE_URL = "postgresql://admin:1234@localhost:5432/database"


class DatabasePostgres:
    def __init__(self, database_url: str | None = None) -> None:
        self.database_url = database_url or getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
        self.file_count = 0
        self.schema = Path(__file__).with_name("database.sql").read_text(encoding="utf-8")

    def insert_normal(self, *, initialize_schema: bool = True) -> None:
        normal = Normal()
        with self._connect() as connection:
            if initialize_schema:
                self._initialize_schema(connection)
            self._insert_files(connection, normal, [("normal", 0, "normal")])

    def insert_hmisali(self, *, initialize_schema: bool = True) -> None:
        with self._connect() as connection:
            if initialize_schema:
                self._initialize_schema(connection)
            for level in get_args(HM_LVL):
                dataset = Hmisali().set_lvl(level)
                self._insert_files(
                    connection,
                    dataset,
                    [("horizontal misalignment", 0, "horizontal misalignment")],
                )

    def insert_imbalance(self, *, initialize_schema: bool = True) -> None:
        with self._connect() as connection:
            if initialize_schema:
                self._initialize_schema(connection)
            for level in get_args(IM_LVL):
                dataset = Imbalance().set_lvl(level)
                self._insert_files(
                    connection,
                    dataset,
                    [("imbalance", 0, "imbalance")],
                )

    def insert_vmisali(self, *, initialize_schema: bool = True) -> None:
        with self._connect() as connection:
            if initialize_schema:
                self._initialize_schema(connection)
            for level in get_args(VM_LVL):
                dataset = Vmisali().set_lvl(level)
                self._insert_files(
                    connection,
                    dataset,
                    [("vertical misalignment", 0, "vertical misalignment")],
                )

    def insert_overhang(self, *, initialize_schema: bool = True) -> None:
        with self._connect() as connection:
            if initialize_schema:
                self._initialize_schema(connection)
            for condition_type in get_args(OH_TIPE):
                condition_name = f"overhang {condition_type.replace('_', ' ')}"
                for level in get_args(OH_LVL):
                    dataset = Overhang().type(condition_type).set_lvl(level)
                    self._insert_files(
                        connection,
                        dataset,
                        [(condition_name, float(level.removesuffix("g")), condition_name)],
                    )

    def insert_underhang(self, *, initialize_schema: bool = True) -> None:
        with self._connect() as connection:
            if initialize_schema:
                self._initialize_schema(connection)
            for condition_type in get_args(UN_TIPE):
                condition_name = f"underhang {condition_type.replace('_', ' ')}"
                for level in get_args(UN_LVL):
                    dataset = Underhang().type(condition_type).set_lvl(level)
                    self._insert_files(
                        connection,
                        dataset,
                        [(condition_name, float(level.removesuffix("g")), condition_name)],
                    )

    def insert_all(self) -> None:
        with self._connect() as connection:
            self._initialize_schema(connection)

        inserters = (
            self.insert_normal,
            self.insert_hmisali,
            self.insert_imbalance,
            self.insert_vmisali,
            self.insert_overhang,
            self.insert_underhang,
        )
        with ThreadPoolExecutor(max_workers=len(inserters)) as executor:
            futures = [
                executor.submit(inserter, initialize_schema=False) for inserter in inserters
            ]
            for future in futures:
                future.result()

        # with self._connect() as connection:
        #     connection.execute(
        #         "REFRESH MATERIALIZED VIEW public.caracteristicas_limpo"
        #     )

    def _connect(self) -> psycopg.Connection[Any]:
        return psycopg.connect(self.database_url)

    def _initialize_schema(self, connection: psycopg.Connection[Any]) -> None:
        connection.execute(self.schema)

    def _insert_files(
        self,
        connection: psycopg.Connection[Any],
        dataset: Any,
        conditions: list[tuple[str, float, str]],
    ) -> None:
        files = dataset.list_files(mat=True)
        for filename in files:
            dataset.set_file(filename)
            file_path = dataset.get_path()

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT EXISTS (SELECT 1 FROM serie WHERE description = %s)",
                    (file_path,),
                )
                already_exists = cursor.fetchone()[0]

            self.file_count += 1
            current_time = datetime.now().strftime("%H:%M:%S")
            if already_exists:
                print(
                    f"[{current_time}] skip file ({file_path}): already in database. "
                    f"{self.file_count}/{len(files)}"
                )
                continue

            print(
                f"[{current_time}] add file ({file_path}) to database. "
                f"{self.file_count}/{len(files)}"
            )
            self._insert_series(
                connection,
                filename,
                file_path,
                conditions,
                self._read_signals(dataset),
                dataset.borda_de_subida(),
            )

    def _insert_series(
        self,
        connection: psycopg.Connection[Any],
        filename: str,
        file_path: str,
        conditions: list[tuple[str, float, str]],
        signals: list[Any],
        splits: list[tuple[int, int]],
    ) -> None:
        with connection.cursor() as cursor:
            frequency = float(Path(filename).stem)
            cursor.execute(
                "INSERT INTO serie (name, freq, description) VALUES (%s, %s, %s) RETURNING id",
                (str(filename), frequency, file_path),
            )
            result = cursor.fetchone()
            if result is None:
                raise RuntimeError("Could not create series record.")
            series_id = result[0]

            condition_names = {name for name, _, _ in conditions}
            cursor.execute(
                "SELECT name FROM condicao WHERE name = ANY(%s)",
                (list(condition_names),),
            )
            existing_conditions = {row[0] for row in cursor.fetchall()}
            missing_conditions = condition_names - existing_conditions
            if missing_conditions:
                raise ValueError(
                    "Conditions are missing from the condicao table: "
                    + ", ".join(sorted(missing_conditions))
                )

            cursor.executemany(
                """
                INSERT INTO serie_condicao (serie, condicao, graduacao, description)
                SELECT %s, id, %s, %s
                FROM condicao
                WHERE name = %s
                """,
                [(series_id, grade, description, name) for name, grade, description in conditions],
            )
            sample_count = len(signals[0])
            if any(len(signal) != sample_count for signal in signals):
                raise ValueError("All sensor signals in a series must have the same length.")

            fatia_indices: list[int | None] = [None] * sample_count
            for split_index, (sample_start, sample_end) in enumerate(splits):
                if sample_start < 0 or sample_end > sample_count or sample_end <= sample_start:
                    raise ValueError(
                        f"Invalid slice bounds ({sample_start}, {sample_end}) "
                        f"for a series with {sample_count} samples."
                    )
                for sample_index in range(sample_start, sample_end):
                    fatia_indices[sample_index] = split_index

            with cursor.copy(
                'COPY amostras (serie, seq, fatia, acel_x1, acel_y1, acel_z1, '
                'acel_x2, acel_y2, acel_z2, mic) FROM STDIN'
            ) as copy:
                for sequence, sample_values in enumerate(zip(*signals), start=1):
                    copy.write_row(
                        (
                            series_id,
                            sequence,
                            fatia_indices[sequence - 1],
                            *(float(value) for value in sample_values),
                        )
                    )
    @staticmethod
    def _read_signals(dataset: Any) -> list[Any]:
        return [
            dataset.read_acel(1, "x").ravel(),
            dataset.read_acel(1, "y").ravel(),
            dataset.read_acel(1, "z").ravel(),
            dataset.read_acel(2, "x").ravel(),
            dataset.read_acel(2, "y").ravel(),
            dataset.read_acel(2, "z").ravel(),
            dataset.read_sound(),
        ]


if __name__ == "__main__":
    database = DatabasePostgres()
    database.insert_all()
