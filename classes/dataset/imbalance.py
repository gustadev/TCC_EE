from . import datafile as df
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Literal, get_args
import pandas as pd

IM_LVL = Literal["6g", "10g", "15g", "20g", "25g", "30g", "35g"]

class Imbalance(df.DataFile):

    def __init__(self):
        super().__init__()
        self.path = [self._dir_,"/imbalance","",""]
        self.lvl = ""
        self.file = ""

    def set_lvl(self, lvl : IM_LVL):
        self.path[2] = "/" + lvl
        self.path[3] = ""
        return self

    def set_file(self,file):
        if Path(self.get_path() + "/" + file):
            self.path[3] = "/" + file
            return self
        self.path[3] = ""
        raise FileNotFoundError(f"Arquivo não encontrado no local {self.get_path() + file}")

    def make_big_file(self,mat=False):
        last_lvl = self.lvl
        last_file = self.file
        frames = []
        for lvl in get_args(IM_LVL):
            self.set_lvl(lvl)
            for file_name in self.list_files(mat):
                self.set_file(file_name)
                for split_index, split in enumerate(self.split_data(self.read_all())):
                    frame = pd.DataFrame(split)
                    frame["lvl"] = lvl
                    frame["file_name"] = float(Path(file_name).stem)
                    frame["tipo_falha"] = "i"
                    frame["split_index"] = split_index
                    frames.append(frame)

        self.lvl = last_lvl
        self.file = last_file
        self.path[2] = "/" + last_lvl if last_lvl else ""
        self.path[3] = "/" + last_file if last_file else ""
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


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