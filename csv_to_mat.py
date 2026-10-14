import numpy as np
import pandas as pd
import scipy.stats as stats
from classes.dataset.hmisali import Hmisali,HM_LVL
from classes.dataset.vmisali import Vmisali,VM_LVL
from classes.dataset.imbalance import Imbalance,IM_LVL
from classes.dataset.normal import Normal
from classes.dataset.overhang import Overhang,OH_LVL,OH_TIPE
from classes.dataset.underhang import Underhang,UN_LVL,UN_TIPE
import matplotlib.pyplot as plt

h_misali    =   Hmisali().set_lvl('2.0mm')
v_misali    =   Vmisali().set_lvl('1.90mm')
imbalan     =   Imbalance().set_lvl('35g')
normal      =   Normal()
overhang    =   Overhang().type("outer_race").set_lvl('35g')
underhang   =   Underhang().type("outer_race").set_lvl('35g')


for f in underhang.list_files(mat=False):
    underhang.set_file(f)
    underhang.save_mat()