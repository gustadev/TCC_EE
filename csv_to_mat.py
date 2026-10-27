from typing import get_args

from classes.dataset.hmisali import HM_LVL, Hmisali
from classes.dataset.imbalance import IM_LVL, Imbalance
from classes.dataset.normal import Normal
from classes.dataset.overhang import OH_LVL, OH_TIPE, Overhang
from classes.dataset.underhang import UN_LVL, UN_TIPE, Underhang
from classes.dataset.vmisali import VM_LVL, Vmisali

datasets = []
# datasets += [Normal()]
datasets += [Hmisali().set_lvl(level) for level in get_args(HM_LVL)]
# datasets += [Imbalance().set_lvl(level) for level in get_args(IM_LVL)]
# datasets += [Vmisali().set_lvl(level) for level in get_args(VM_LVL)]
# datasets += [
#     Overhang().type(condition_type).set_lvl(level)
#     for condition_type in get_args(OH_TIPE)
#     for level in get_args(OH_LVL)
# ]
# datasets += [
#     Underhang().type(condition_type).set_lvl(level)
#     for condition_type in get_args(UN_TIPE)
#     for level in get_args(UN_LVL)
# ]

for dataset in datasets:
    for filename in dataset.list_files(mat=False):
        print(f"Processando {filename}")
        dataset.set_file(filename)
        dataset.save_mat()