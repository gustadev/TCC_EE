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

    print("Aproximação:", cA4)
    print("Detalhes:", cD4, cD3, cD2, cD1)

    fig, sub = plt.subplots(4)
    sub[0].plot(cD1)
    sub[1].plot(signal[:,2])
    plt.show()