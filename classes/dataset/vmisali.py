from . import datafile as df
from pathlib import Path
from typing import Literal, get_args
import pandas as pd

VM_LVL = Literal["0.51mm","0.63mm","1.27mm","1.40mm","1.78mm","1.90mm"]

class Vmisali(df.DataFile):

    def __init__(self):
        super().__init__()
        self.path = [self._dir_,"/vertical-misalignment","",""]
        self.lvl = ""
        self.file = ""

    def set_lvl(self, lvl : VM_LVL):
    # Valores Possives: "0.51mm","0.63mm","1.27mm","1.40mm","1.78mm","1.90mm"
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
        for lvl in get_args(VM_LVL):
            self.set_lvl(lvl)
            for file_name in self.list_files(mat):
                self.set_file(file_name)
                for split_index, split in enumerate(self.split_data(self.read_all())):
                    frame = pd.DataFrame(split)
                    frame["lvl"] = lvl
                    frame["file_name"] = float(Path(file_name).stem)
                    frame["tipo_falha"] = "v"
                    frame["split_index"] = split_index
                    frames.append(frame)

        self.lvl = last_lvl
        self.file = last_file
        self.path[2] = "/" + last_lvl if last_lvl else ""
        self.path[3] = "/" + last_file if last_file else ""
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


if __name__ == "__main__":
    v_misali = Vmisali().set_lvl("0.51mm")
    arquivo = v_misali.list_files()[0]
    v_misali.set_file(arquivo).plot_signals()

