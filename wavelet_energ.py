import matplotlib.pyplot as plt
import numpy as np
import pywt

from classes.dataset.datafile import DataFile
from classes.dataset.hmisali import Hmisali
from classes.dataset.imbalance import Imbalance
from classes.dataset.normal import Normal
from classes.dataset.overhang import Overhang
from classes.dataset.underhang import Underhang
from classes.dataset.vmisali import Vmisali


def calculate_detail_energies(
    signal: np.ndarray, n_levels: int, wavelet: str = "db1"
) -> np.ndarray:
    """Calcula a energia de D1 ate Dn da DWT de um sinal."""
    if not isinstance(n_levels, int) or n_levels <= 0:
        raise ValueError("n_levels deve ser um inteiro positivo.")

    coefficients = pywt.wavedec(np.asarray(signal).ravel(), wavelet, level=n_levels)
    detail_coefficients = coefficients[:0:-1]
    return np.asarray(
        [np.sum(np.abs(detail) ** 2) for detail in detail_coefficients], dtype=float
    )


def calculate_dataset_energies(
    dataset: DataFile,
    accelerator: int,
    n_levels: int,
    wavelet: str,
    sample_limit: int | None = None,
) -> tuple[list[str], np.ndarray]:
    """Calcula as energias dos detalhes DWT de todos os arquivos do dataset."""
    files = dataset.list_files()
    if not files:
        raise ValueError("Nenhum arquivo foi encontrado para a condicao selecionada.")

    energies_by_file = []
    for filename in files:
        acceleration = dataset.set_file(filename).read_acel(accelerator, ["x", "y", "z"])
        if sample_limit is not None:
            acceleration = acceleration[:sample_limit]

        energies_by_file.append(
            np.column_stack(
                [
                    calculate_detail_energies(acceleration[:, axis], n_levels, wavelet)
                    for axis in range(3)
                ]
            )
        )

    return files, np.asarray(energies_by_file)


def plot_energy_projections(
    energies_by_condition: dict[str, tuple[list[str], np.ndarray, str]],
    accelerator: int,
) -> list[plt.Figure]:
    """Plota as projeções XY, XZ e YZ para cada detalhe da wavelet."""
    first_energies = next(iter(energies_by_condition.values()))[1]
    n_levels = first_energies.shape[1]
    projections = ((0, 1, "XY"), (0, 2, "XZ"), (1, 2, "YZ"))
    figures = []

    for detail_index in range(n_levels):
        figure, axes = plt.subplots(1, 3, figsize=(18, 5), layout="constrained")
        figure.suptitle(
            f"Energia do detalhe D{detail_index + 1} - Acelerometro {accelerator}"
        )

        for axis, (first_axis, second_axis, projection) in zip(axes, projections):
            for condition, (_, energies, color) in energies_by_condition.items():
                values = energies[:, detail_index, :]
                axis.scatter(
                    values[:, first_axis],
                    values[:, second_axis],
                    label=condition,
                    color=color,
                    alpha=0.8,
                )

            axis.set_title(projection)
            axis.set_xlabel(f"Energia D{detail_index + 1} - eixo {'XYZ'[first_axis]}")
            axis.set_ylabel(f"Energia D{detail_index + 1} - eixo {'XYZ'[second_axis]}")
            axis.grid(True, alpha=0.3)
            axis.legend()

        figures.append(figure)

    return figures


if __name__ == "__main__":
    n_levels = 15
    wavelet = "dmey"
    accelerator = 2
    sample_limit = 5_000

    datasets = {
        "Normal": (Normal(), "tab:blue"),
        "Desalinhamento horizontal (0.5 mm)": (
            Hmisali().set_lvl("0.5mm"),
            "tab:orange",
        ),
        "Desalinhamento vertical (0.51 mm)": (
            Vmisali().set_lvl("0.51mm"),
            "tab:green",
        ),
        "Desbalanceamento (6g)": (Imbalance().set_lvl("6g"), "tab:red"),
        "Overhang - falha na esfera (6g)": (
            Overhang().set_lvl("6g").type("ball_fault"),
            "tab:purple",
        ),
        "Overhang - falha na gaiola (6g)": (
            Overhang().set_lvl("6g").type("cage_fault"),
            "tab:brown",
        ),
        "Overhang - falha na pista externa (6g)": (
            Overhang().set_lvl("6g").type("outer_race"),
            "tab:pink",
        ),
        "Underhang - falha na esfera (6g)": (
            Underhang().set_lvl("6g").tipe("ball_fault"),
            "tab:gray",
        ),
        "Underhang - falha na gaiola (6g)": (
            Underhang().set_lvl("6g").tipe("cage_fault"),
            "tab:olive",
        ),
        "Underhang - falha na pista externa (6g)": (
            Underhang().set_lvl("6g").tipe("outer_race"),
            "tab:cyan",
        ),
    }

    energies_by_condition = {}
    for condition, (dataset, color) in datasets.items():
        files, energies = calculate_dataset_energies(
            dataset,
            accelerator=accelerator,
            n_levels=n_levels,
            wavelet=wavelet,
            sample_limit=sample_limit,
        )
        energies_by_condition[condition] = (files, energies, color)
        print(f"{condition}: {len(files)} arquivos processados.")

    plot_energy_projections(energies_by_condition, accelerator)
    plt.show()