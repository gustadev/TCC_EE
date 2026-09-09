import matplotlib.pyplot as plt
import numpy as np
import pywt

from classes.dataset.overhang import Overhang
from classes.dataset.hmisali import Hmisali
from classes.dataset.normal import Normal


def plot_dwt_details(axes, signal, title, n_escalas, wl_tipe = "db1"):
    if not isinstance(n_escalas, int) or n_escalas <= 0:
        raise ValueError("n_escalas deve ser um inteiro positivo.")
    
    coefficients = pywt.wavedec(signal, wl_tipe, level=n_escalas)
    details = []

    for escala in range(1, n_escalas + 1):
        detail = pywt.upcoef(
            "d",
            coefficients[n_escalas - escala + 1],
            wl_tipe,
            level=escala,
            take=len(signal),
        )
        details.append(detail)

    for escala, (axis, detail) in enumerate(zip(axes, details), start=1):
        axis.plot(detail, linewidth=0.8)
        axis.set_ylabel(f"D{escala}")
        axis.grid(True, alpha=0.3)

    axes[0].set_title(title)
    axes[-1].set_xlabel("Amostra")

    print(f"\n{title}")
    for escala, detail in enumerate(details, start=1):
        print(f"  D{escala}: {np.sum(detail ** 2):.6e}")

if __name__ == "__main__":
    n_esc = 10
    print(pywt.wavelist(kind='discrete'))
    wt_tipe = "dmey"
    normal = Normal()
    dataset = Overhang().set_lvl("35g").type("ball_fault")

    normal_file = normal.list_files()[1]
    dataset_file = dataset.list_files()[1]

    normal_data = normal.set_file(normal_file)
    normal_x = normal_data.read_acel(2, "x")[0:10000].ravel().copy()
    normal_y = normal_data.read_acel(2, "y")[0:10000].ravel().copy()
    normal_z = normal_data.read_acel(2, "z")[0:10000].ravel().copy()
    normal_sound = normal_data.read_sound()[0:10000].copy()

    dataset_data = dataset.set_file(dataset_file)
    dataset_x = dataset_data.read_acel(2, "x")[0:10000].ravel().copy()
    dataset_y = dataset_data.read_acel(2, "y")[0:10000].ravel().copy()
    dataset_z = dataset_data.read_acel(2, "z")[0:10000].ravel().copy()
    dataset_sound = dataset_data.read_sound()[0:10000].copy()

    figure_x, axes_x = plt.subplots(n_esc, 2, figsize=(16, 2 * n_esc), sharex="col")
    plot_dwt_details(axes_x[:, 0], normal_x, "Normal - eixo X", n_esc, wt_tipe)
    plot_dwt_details(axes_x[:, 1], dataset_x, "dataset - eixo X", n_esc, wt_tipe)
    figure_x.tight_layout()

    figure_y, axes_y = plt.subplots(n_esc, 2, figsize=(16, 2 * n_esc), sharex="col")
    plot_dwt_details(axes_y[:, 0], normal_y, "Normal - eixo Y", n_esc, wt_tipe)
    plot_dwt_details(axes_y[:, 1], dataset_y, "dataset - eixo Y", n_esc, wt_tipe)
    figure_y.tight_layout()

    figure_z, axes_z = plt.subplots(n_esc, 2, figsize=(16, 2 * n_esc), sharex="col")
    plot_dwt_details(axes_z[:, 0], normal_z, "Normal - eixo Z", n_esc, wt_tipe)
    plot_dwt_details(axes_z[:, 1], dataset_z, "dataset - eixo Z", n_esc, wt_tipe)
    figure_z.tight_layout()

    figure_sound, axes_sound = plt.subplots(n_esc, 2, figsize=(16, 2 * n_esc), sharex="col")
    plot_dwt_details(axes_sound[:, 0], normal_sound, "Normal - som", n_esc, wt_tipe)
    plot_dwt_details(axes_sound[:, 1], dataset_sound, "dataset - som", n_esc, wt_tipe)
    figure_sound.tight_layout()

    plt.show()