import pandas as pd
import numpy as np
from typing import Literal
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

ACEL_NUM = Literal[1,2,"all"]
ACEL_AXIS = Literal["x","y","z","all"]

class DataFile:

    def __init__(self):
        self._dir_   =  "Datasets/mafaulda"
        self.path = [self._dir_,]
        self._tac_ = 0
        self._acel_ = {
             1 : {"x":1,"y":2,"z":3},
             2 : {"x":4,"y":5,"z":6},
        }
        self._sound_ = 7

    def get_path(self):
        path = ""
        for p in self.path:
            path += p
        return path

    def read_all(self):
        return pd.read_csv(self.get_path(), header=None).to_numpy()

    def read_tacometro(self):
        return pd.read_csv(self.get_path(), header=None).iloc[:,self._tac_].to_numpy()

    def read_acel(self, acel : list[ACEL_NUM] | ACEL_NUM | "all" = "all", axis : list[ACEL_AXIS] | ACEL_AXIS | "all"  = "all"):
        data = pd.read_csv(self.get_path(), header=None)
        colunas = [
            self._acel_[acelerometro][eixo]
            for acelerometro    in ((1, 2) if acel == "all" else (acel if isinstance(acel,list) else [acel]))
            for eixo            in (("x", "y", "z") if axis == "all" else (axis if isinstance(axis,list) else [axis]))
        ]
        return data.iloc[:, colunas].to_numpy()

    def read_sound(self):
        return pd.read_csv(self.get_path(), header=None).iloc[:,self._sound_].to_numpy()

    def plot_signals(self, show: bool = True):
        """Plota os sinais do arquivo com controles para ocultar ou exibir cada canal."""
        data = pd.read_csv(self.get_path(), header=None)
        signal_names = [
            "Tacometro",
            "Acelerometro 1 - eixo X",
            "Acelerometro 1 - eixo Y",
            "Acelerometro 1 - eixo Z",
            "Acelerometro 2 - eixo X",
            "Acelerometro 2 - eixo Y",
            "Acelerometro 2 - eixo Z",
            "Som",
        ]
        labels = [
            signal_names[column] if column < len(signal_names) else f"Sinal {column}"
            for column in data.columns
        ]

        figure, axis = plt.subplots(figsize=(16, 8))
        lines = [
            axis.plot(data.index, data[column], label=label)[0]
            for column, label in zip(data.columns, labels)
        ]

        axis.set_title(f"Sinais de {os.path.basename(self.get_path())}")
        axis.set_xlabel("Amostra")
        axis.set_ylabel("Amplitude")
        axis.grid(True, alpha=0.3)
        axis.legend(loc="upper left")

        figure.subplots_adjust(right=0.72)
        controls_axis = figure.add_axes((0.75, 0.2, 0.22, 0.6))
        check_buttons = CheckButtons(controls_axis, labels, [True] * len(labels))
        controls_axis.set_title("Sinais")

        def toggle_signal(label: str):
            line = lines[labels.index(label)]
            line.set_visible(not line.get_visible())
            figure.canvas.draw_idle()

        check_buttons.on_clicked(toggle_signal)
        figure._signal_check_buttons = check_buttons

        if show:
            plt.show()

        return figure, axis

    def plot_statistics_3d(self, tag: str = "mean", acel: int = 1, show: bool = True):
        """Plota a estatistica selecionada dos eixos X, Y e Z de cada arquivo."""
        if acel not in self._acel_:
            raise ValueError("O acelerometro deve ser 1 ou 2.")

        statistics = {
            "mean": ("Media", lambda data: data.mean(axis=0)),
            "variance": ("Variancia", lambda data: data.var(axis=0)),
            "std": ("Desvio padrao", lambda data: data.std(axis=0)),
            "skewness": ("Assimetria", lambda data: pd.DataFrame(data).skew().to_numpy()),
            "kurtosis": ("Curtose", lambda data: pd.DataFrame(data).kurt().to_numpy()),
        }
        if tag not in statistics:
            raise ValueError("Use uma destas tags: mean, variance, std, skewness ou kurtosis.")

        files = self.list_files()
        if not files:
            raise ValueError("Nenhum arquivo foi encontrado para o nivel selecionado.")

        values_by_file = []
        statistic_name, calculate = statistics[tag]
        for file in files:
            acceleration = self.set_file(file).read_acel(acel, ["x", "y", "z"])
            values_by_file.append(calculate(acceleration))

        values = np.asarray(values_by_file)
        figure = plt.figure(figsize=(10, 8))
        axis = figure.add_subplot(projection="3d")
        axis.scatter(values[:, 0], values[:, 1], values[:, 2])
        axis.set_title(f"{statistic_name} dos sinais - Acelerometro {acel}")
        axis.set_xlabel(f"{statistic_name} do eixo X")
        axis.set_ylabel(f"{statistic_name} do eixo Y")
        axis.set_zlabel(f"{statistic_name} do eixo Z")

        if show:
            plt.show()

        return figure, axis