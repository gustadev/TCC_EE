import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np
import pywt

from classes.dataset.hmisali import Hmisali
from classes.dataset.normal import Normal


def plot_dwt_scalogram(axis, signal, title, n_escalas, wl_tipe = "db1"):
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

    scalogram = np.vstack(details)
    image = axis.imshow(np.abs(scalogram), aspect="auto", origin="lower", interpolation="nearest", resample=False, cmap="turbo")
    axis.set_title(title)
    axis.set_xlabel("Amostra")
    axis.set_ylabel("Nivel DWT")
    axis.set_yticks(range(n_escalas), [f"D{escala}" for escala in range(1, n_escalas + 1)])

    print(f"\n{title}")
    for escala, detail in enumerate(details, start=1):
        print(f"  D{escala}: {np.sum(detail ** 2):.6e}")

    return image


def share_color_scale(*images):
    values = [np.asarray(image.get_array()) for image in images]
    shared_norm = Normalize(
        vmin=min(np.nanmin(value) for value in values),
        vmax=max(np.nanmax(value) for value in values),
    )

    for image in images:
        image.set_norm(shared_norm)


if __name__ == "__main__":
    n_esc = 15
    print(pywt.wavelist(kind='discrete'))
    wt_tipe = "db4"
    normal = Normal()
    h_misali = Hmisali().set_lvl("0.5mm")

    normal_file = normal.list_files()[3]
    h_misali_file = h_misali.list_files()[3]

    normal_data = normal.set_file(normal_file)
    normal_x = normal_data.read_acel(2, "x")[0:25000].ravel().copy()
    normal_y = normal_data.read_acel(2, "y")[0:25000].ravel().copy()
    normal_z = normal_data.read_acel(2, "z")[0:25000].ravel().copy()
    normal_sound = normal_data.read_sound()[0:25000].copy()

    h_misali_data = h_misali.set_file(h_misali_file)
    h_misali_x = h_misali_data.read_acel(2, "x")[0:25000].ravel().copy()
    h_misali_y = h_misali_data.read_acel(2, "y")[0:25000].ravel().copy()
    h_misali_z = h_misali_data.read_acel(2, "z")[0:25000].ravel().copy()
    h_misali_sound = h_misali_data.read_sound()[0:25000].copy()

    figure_acceleration, axes_acceleration = plt.subplots(
        6, 1, figsize=(14, 18), layout="constrained"
    )
    image_x_normal = plot_dwt_scalogram(
        axes_acceleration[0], normal_x, "Normal - eixo X", n_esc, wt_tipe
    )
    image_x_h_misali = plot_dwt_scalogram(
        axes_acceleration[1],
        h_misali_x,
        "Desalinhamento Horizontal - eixo X",
        n_esc,
        wt_tipe,
    )
    share_color_scale(image_x_normal, image_x_h_misali)
    figure_acceleration.colorbar(
        image_x_normal, ax=axes_acceleration[0:2], label="Magnitude"
    )

    image_y_normal = plot_dwt_scalogram(
        axes_acceleration[2], normal_y, "Normal - eixo Y", n_esc, wt_tipe
    )
    image_y_h_misali = plot_dwt_scalogram(
        axes_acceleration[3],
        h_misali_y,
        "Desalinhamento Horizontal - eixo Y",
        n_esc,
        wt_tipe,
    )
    share_color_scale(image_y_normal, image_y_h_misali)
    figure_acceleration.colorbar(
        image_y_normal, ax=axes_acceleration[2:4], label="Magnitude"
    )

    image_z_normal = plot_dwt_scalogram(
        axes_acceleration[4], normal_z, "Normal - eixo Z", n_esc, wt_tipe
    )
    image_z_h_misali = plot_dwt_scalogram(
        axes_acceleration[5],
        h_misali_z,
        "Desalinhamento Horizontal - eixo Z",
        n_esc,
        wt_tipe,
    )
    share_color_scale(image_z_normal, image_z_h_misali)
    figure_acceleration.colorbar(
        image_z_normal, ax=axes_acceleration[4:6], label="Magnitude"
    )

    figure_sound, axes_sound = plt.subplots(2, 1, figsize=(14, 8), layout="constrained")
    image_sound_normal = plot_dwt_scalogram(axes_sound[0], normal_sound, "Normal - som", n_esc, wt_tipe)
    image_sound_h_misali = plot_dwt_scalogram(axes_sound[1], h_misali_sound, "Desalinhamento Horizontal - som", n_esc, wt_tipe)
    share_color_scale(image_sound_normal, image_sound_h_misali)
    figure_sound.colorbar(image_sound_normal, ax=axes_sound, label="Magnitude")

    plt.show()