from db_utils import query_data
import pywt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# Constantes
fs = 50000 # samp/s
tempo = 5 # segundos
series_fatias = query_data("SELECT DISTINCT serie, fatia from amostras where fatia is not null limit 1")

for s,f in series_fatias:
    signal = query_data(f"SELECT seq, acel_x1, acel_y1, acel_z1, acel_x2, acel_y2, acel_z2, mic from amostras where serie = {s} and fatia={f} order by seq")

    wt = pywt.wavedec(signal[:,2].flatten(), wavelet="db4", level=15, axis=0)

    for w in wt:
        print(pd.DataFrame(w).kurt())
    