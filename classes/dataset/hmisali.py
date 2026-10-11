from . import datafile as df
from pathlib import Path
from typing import Literal

HM_LVL = Literal["0.5mm","1.0mm","1.5mm","2.0mm"]

class Hmisali(df.DataFile):

    def __init__(self):
        super().__init__()
        self.path = [self._dir_,"/horizontal-misalignment","",""]
        self.lvl = ""
        self.file = ""

    def set_lvl(self, lvl : HM_LVL):
        self.path[2] = "/" + lvl
        return self

    def set_file(self,file):
        if Path(self.get_path() + "/" + file):
            self.path[3] = "/" + file
            return self
        self.path[3] = ""
        raise FileNotFoundError(f"Arquivo não encontrado no local {self.get_path() + file}")

if __name__ == "__main__":
    h_misali = Hmisali().set_lvl("0.5mm")
    h_misali.plot_statistics_3d(tag="variance", acel=2)


