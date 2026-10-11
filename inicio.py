import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np

from classes.dataset.hmisali import Hmisali
from classes.dataset.normal import Normal

normal = Normal()
hmisali = Hmisali().set_lvl("0.5mm")

normal.set_file(normal.list_files(True)[1])

d = normal.read_acel(1,'all',True)
print(d)
plt.plot(d[1][:,1])
plt.show()
# bu_taco = hmisali.borda_de_subida()

# print(bu_taco)

# plt.plot(hmisali.read_acel(1,'y')[bu_taco[1][0]:bu_taco[1][1]])
# plt.show()
