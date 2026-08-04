from . import datafile as df
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Literal

OH_LVL = Literal["0g","6g","20g","35g"]
OH_TIPE = Literal["ball_fault", "cage_fault", "outer_race"]

class Overhang(df.DataFile):

    def __init__(self):
        super().__init__()
        self.path = [self._dir_,"/overhang","","",""]
        self.lvl = ""
        self.file = ""

    def set_lvl(self, lvl : OH_LVL):
        self.path[3] = "/" + lvl
        return self

    def tipe(self, tipe : OH_TIPE):
        self.path[2] = "/" + tipe
        return self

    def list_files(self):
        pasta = Path(self.get_path())
        return sorted(arquivo.name for arquivo in pasta.iterdir() if arquivo.is_file())

    def set_file(self,file):
        if Path(self.get_path() + "/" + file):
            self.path[4] = "/" + file
            return self
        self.path[4] = ""
        raise FileNotFoundError(f"Arquivo não encontrado no local {self.get_path() + file}")


if __name__ == "__main__":
    overhang = Overhang().tipe("ball_fault").set_lvl("0g")
    arquivo = overhang.list_files()[0]
    aceleracoes = overhang.set_file(arquivo).read_acel(1, ["x", "y", "z"])

    plt.figure(figsize=(18, 9))
    plt.plot(aceleracoes[:, 0], label="Acelerometro 1 - eixo X")
    plt.plot(aceleracoes[:, 1], label="Acelerometro 1 - eixo Y")
    plt.plot(aceleracoes[:, 2], label="Acelerometro 1 - eixo Z")
    plt.title(f"Overhang - falha na esfera (0g) - {arquivo}")
    plt.xlabel("Amostra")
    plt.ylabel("Aceleracao")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

