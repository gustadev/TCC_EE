from . import datafile as df
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Literal
import pandas as pd

class Normal(df.DataFile):

    def __init__(self):
        super().__init__()
        self.path = [self._dir_,"/normal","",""]
        self.lvl = ""
        self.file = ""

    def set_file(self,file,mat=True):
        if Path(self.get_path() + "/" + file):
            self.path[3] = "/" + file
            return self
        self.path[3] = ""
        raise FileNotFoundError(f"Arquivo não encontrado no local {self.get_path() + file}")

    def make_big_file(self,mat=True):
        last_file = self.file
        frames = []
        for file_name in self.list_files(mat):
            self.set_file(file_name)
            for split_index, split in enumerate(self.split_data(self.read_all())):
                frame = pd.DataFrame(split)
                frame["lvl"] = ""
                frame["file_name"] = float(Path(file_name).stem)
                frame["tipo_falha"] = "n"
                frame["subtipo_falha"] = "normal"
                frame["split_index"] = split_index
                frames.append(frame)

        self.file = last_file
        self.path[3] = "/" + last_file if last_file else ""
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


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

    