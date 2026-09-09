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

h_misali    =   Hmisali().set_lvl('1.5mm')
v_misali    =   Vmisali().set_lvl('1.90mm')
imbalan     =   Imbalance().set_lvl('6g')
normal      =   Normal()
overhang    =   Overhang().set_lvl('6g')
underhang   =   Underhang().set_lvl('6g')


for f in h_misali.list_files():
    h_misali.set_file(f)
    h_misali.save_mat()