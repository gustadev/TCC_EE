from . import datafile as df
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Literal

IM_LVL = Literal["6g", "10g", "15g", "20g", "25g", "30g", "35g"]

class Imbalance(df.DataFile):

    def __init__(self):
        super().__init__()
        self.path = [self._dir_,"/imbalance","",""]
        self.lvl = ""
        self.file = ""

    def set_lvl(self, lvl : IM_LVL):
        self.path[2] = "/" + lvl
        return self

    def set_file(self,file):
        if Path(self.get_path() + "/" + file):
            self.path[3] = "/" + file
            return self
        self.path[3] = ""
        raise FileNotFoundError(f"Arquivo não encontrado no local {self.get_path() + file}")


if __name__ == "__main__":
    imbalance = Imbalance().set_lvl("6g")
    arquivo = imbalance.list_files()[0]
    aceleracoes = imbalance.set_file(arquivo).read_acel(1, ["x", "y", "z"])

    plt.figure(figsize=(18, 9))
    plt.plot(aceleracoes[:, 0], label="Acelerometro 1 - eixo X")
    plt.plot(aceleracoes[:, 1], label="Acelerometro 1 - eixo Y")
    plt.plot(aceleracoes[:, 2], label="Acelerometro 1 - eixo Z")
    plt.title(f"Desbalanceamento (6g) - {arquivo}")
    plt.xlabel("Amostra")
    plt.ylabel("Aceleracao")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()