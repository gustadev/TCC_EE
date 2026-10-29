from db_utils import query_data
import pywt
import matplotlib.pyplot as plt

# Constantes
fs = 50000 # samp/s
tempo = 5 # segundos
series_fatias = query_data("SELECT DISTINCT serie, fatia from amostras where fatia is not null limit 1")

for s,f in series_fatias:
    signal = query_data(f"SELECT seq, acel_x1, acel_y1, acel_z1, acel_x2, acel_y2, acel_z2, mic from amostras where serie = {s} and fatia={f} order by seq")

    # Calcula a transformada usando a wavelet Daubechies 4
    cA4, cD4, cD3, cD2, cD1 = pywt.wavedec(signal[:,2], wavelet="db4", level=4)

    # A consulta retorna: seq, acel_x1, acel_y1, acel_z1, ...
    # Portanto, signal[:, 2] é acel_y1.
    tempo_sinal = (signal[:, 0] - signal[0, 0]) / fs

    # wavedec retorna a aproximação final seguida dos detalhes do nível mais
    # alto ao mais baixo: cA4, cD4, cD3, cD2, cD1.
    coeficientes = [
        (cA4, "Aproximação cA4 (nível 4)"),
        (cD4, "Detalhe cD4 (nível 4)"),
        (cD3, "Detalhe cD3 (nível 3)"),
        (cD2, "Detalhe cD2 (nível 2)"),
        (cD1, "Detalhe cD1 (nível 1)"),
    ]

    fig, axes = plt.subplots(6, 1, figsize=(13, 14))

    axes[0].plot(tempo_sinal, signal[:, 2], color="steelblue", linewidth=0.8)
    axes[0].set_title("Sinal original — acel_y1")
    axes[0].set_xlabel("Tempo (s)")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True, alpha=0.3)

    for ax, (coef, titulo) in zip(axes[1:], coeficientes):
        ax.plot(coef, linewidth=0.8)
        ax.set_title(titulo)
        ax.set_xlabel("Índice do coeficiente")
        ax.set_ylabel("Amplitude")
        ax.grid(True, alpha=0.3)

    fig.suptitle(f"Decomposição wavelet db4 — série {s}, fatia {f}")
    fig.tight_layout()
    plt.show()
