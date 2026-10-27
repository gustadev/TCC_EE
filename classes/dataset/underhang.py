from . import datafile as df
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Literal, get_args
import pandas as pd

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
        self.path[4] = ""
        return self

    def type(self, tipe : UN_TIPE):
        # Valor Possival: "ball_fault", "cage_fault", "outer_race"
        self.path[2] = "/" + tipe
        self.path[3] = ""
        self.path[4] = ""
        return self

    def set_file(self,file):
        if Path(self.get_path() + "/" + file):
            self.path[4] = "/" + file
            return self
        self.path[4] = ""
        raise FileNotFoundError(f"Arquivo não encontrado no local {self.get_path() + file}")

    def make_big_file(self,mat=False):
        last_type = self.path[2]
        last_lvl = self.lvl
        last_file = self.file
        frames = []
        for subtype in get_args(UN_TIPE):
            self.type(subtype)
            for lvl in get_args(UN_LVL):
                self.set_lvl(lvl)
                for file_name in self.list_files(mat):
                    self.set_file(file_name)
                    for split_index, split in enumerate(self.split_data(self.read_all())):
                        frame = pd.DataFrame(split)
                        frame["lvl"] = lvl
                        frame["file_name"] = float(Path(file_name).stem)
                        frame["tipo_falha"] = "u"
                        frame["subtipo_falha"] = subtype
                        frame["split_index"] = split_index
                        frames.append(frame)

        self.path[2] = last_type
        self.lvl = last_lvl
        self.file = last_file
        self.path[3] = "/" + last_lvl if last_lvl else ""
        self.path[4] = "/" + last_file if last_file else ""
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


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