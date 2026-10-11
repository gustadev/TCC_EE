from . import datafile as df
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Literal

UN_LVL = Literal["0g","6g","20g","35g"]
UN_TIPE = Literal["ball_fault", "cage_fault", "outer_race"]

class Underhang(df.DataFile):

    def __init__(self):
        super().__init__()
        self.path = [self._dir_,"/underhang","","",""]
        self.lvl = ""
        self.file = ""

    def set_lvl(self, lvl : UN_LVL):
        # Valores possiveis: "0g","6g","20g","35g"
        self.path[3] = "/" + lvl
        return self

    def tipe(self, tipe : UN_TIPE):
        # Valor Possival: "ball_fault", "cage_fault", "outer_race"
        self.path[2] = "/" + tipe
        return self

    def set_file(self,file):
        if Path(self.get_path() + "/" + file):
            self.path[4] = "/" + file
            return self
        self.path[4] = ""
        raise FileNotFoundError(f"Arquivo não encontrado no local {self.get_path() + file}")


if __name__ == "__main__":
    underhang = Underhang().tipe("ball_fault").set_lvl("0g")
    arquivo = underhang.list_files()[0]
    aceleracoes = underhang.set_file(arquivo).read_acel(1, ["x", "y", "z"])

    plt.figure(figsize=(18, 9))
    plt.plot(aceleracoes[:, 0], label="Acelerometro 1 - eixo X")
    plt.plot(aceleracoes[:, 1], label="Acelerometes 1 - eixo Y")
    plt.plot(aceleracoes[:, 2], label="Acelerometro 1 - eixo Z")
    plt.title(f"Underhang - falha na esfera (0g) - {arquivo}")
    plt.xlabel("Amostra")
    plt.ylabel("Aceleracao")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()