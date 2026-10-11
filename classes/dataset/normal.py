from . import datafile as df
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Literal

class Normal(df.DataFile):

    def __init__(self):
        super().__init__()
        self.path = [self._dir_,"/normal","",""]
        self.lvl = ""
        self.file = ""

    def set_file(self,file,mat=True):
        file = str.replace(file,".csv",".mat")
        if Path(self.get_path() + "/" + file):
            self.path[3] = "/" + file
            return self
        self.path[3] = ""
        raise FileNotFoundError(f"Arquivo não encontrado no local {self.get_path() + file}")


if __name__ == "__main__":
    normal = Normal()
    arquivo = normal.list_files()[0]
    aceleracoes = normal.set_file(arquivo).read_acel(1, ["x", "y", "z"])

    plt.figure(figsize=(18, 9))
    plt.plot(aceleracoes[:, 0], label="Acelerometro 1 - eixo X")
    plt.plot(aceleracoes[:, 2], label="Acelerometro 1 - eixo Z")
    plt.plot(aceleracoes[:, 1], label="Acelerometro 1 - eixo Y")
    plt.title(f"Condicao normal - {arquivo}")
    plt.xlabel("Amostra")
    plt.ylabel("Aceleracao")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    