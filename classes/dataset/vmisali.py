from . import datafile as df
from pathlib import Path
from typing import Literal

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
        return self

    def list_files(self):
        pasta = Path(self.get_path())
        return sorted(arquivo.name for arquivo in pasta.iterdir() if arquivo.is_file())

    def set_file(self,file):
        if Path(self.get_path() + "/" + file):
            self.path[3] = "/" + file
            return self
        self.path[3] = ""
        raise FileNotFoundError(f"Arquivo não encontrado no local {self.get_path() + file}")


if __name__ == "__main__":
    v_misali = Vmisali().set_lvl("0.51mm")
    arquivo = v_misali.list_files()[0]
    v_misali.set_file(arquivo).plot_signals()

