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


if __name__ == "__main__":

    # Dados MaFaulDa
    h_misali    =   Hmisali().set_lvl('0.5mm')
    v_misali    =   Vmisali().set_lvl('0.51mm')
    imbalan     =   Imbalance().set_lvl('6g')
    normal      =   Normal()
    overhang    =   Overhang().set_lvl('0g')
    underhang   =   Underhang().set_lvl('0g')
    


    normal_stats = {
        "mean" : [],
        "variance" : [],
        "kurtosis" : [],
        "skewness" : []
    }

    h_misali_stats = {
        "mean" : [],
        "variance" : [],
        "kurtosis" : [],
        "skewness" : []
    }

    v_misali_stats = {
            "mean" : [],
            "variance" : [],
            "kurtosis" : [],
            "skewness" : []
        }

    
    for f in normal.list_files():
        data = normal.set_file(f).read_acel(1,"all")
        normal_stats["mean"].append(data.mean(axis=0))
        normal_stats["variance"].append(np.var(data,axis=0))
        normal_stats["kurtosis"].append(stats.kurtosis(data,axis=0))
        normal_stats["skewness"].append(stats.skew(data,axis=0))

    for f in h_misali.list_files():
        data = h_misali.set_file(f).read_acel(1,"all")
        h_misali_stats["mean"].append(data.mean(axis=0))
        h_misali_stats["variance"].append(np.var(data,axis=0))
        h_misali_stats["kurtosis"].append(stats.kurtosis(data,axis=0))
        h_misali_stats["skewness"].append(stats.skew(data,axis=0))

    for f in v_misali.list_files():
        data = v_misali.set_file(f).read_acel(1,"all")
        v_misali_stats["mean"].append(data.mean(axis=0))
        v_misali_stats["variance"].append(np.var(data,axis=0))
        v_misali_stats["kurtosis"].append(stats.kurtosis(data,axis=0))
        v_misali_stats["skewness"].append(stats.skew(data,axis=0))

    mean_values = np.asarray(normal_stats["mean"])
    h_misali_mean_values = np.asarray(h_misali_stats["mean"])
    v_misali_mean_values = np.asarray(v_misali_stats["mean"])
    figure = plt.figure(num=1,figsize=(8, 8),)
    axis = figure.add_subplot(projection="3d")
    axis.scatter(mean_values[:, 0], mean_values[:, 1], mean_values[:, 2], color="blue", label="Normal")
    axis.scatter(h_misali_mean_values[:, 0], h_misali_mean_values[:, 1], h_misali_mean_values[:, 2], color="red", label="Desalinhamento horizontal")
    axis.scatter(v_misali_mean_values[:, 0], v_misali_mean_values[:, 1], v_misali_mean_values[:, 2], color="green", label="Desalinhamento vertical")
    axis.set_xlabel("Media do eixo X")
    axis.set_ylabel("Media do eixo Y")
    axis.set_zlabel("Media do eixo Z")
    axis.set_title("Media dos dados")
    axis.legend()

    variance_values = np.asarray(normal_stats["variance"])
    h_misali_variance_values = np.asarray(h_misali_stats["variance"])
    v_misali_variance_values = np.asarray(v_misali_stats["variance"])
    figure = plt.figure(num=2,figsize=(8, 8))
    axis = figure.add_subplot(projection="3d")
    axis.scatter(variance_values[:, 0], variance_values[:, 1], variance_values[:, 2], color="blue", label="Normal")
    axis.scatter(h_misali_variance_values[:, 0], h_misali_variance_values[:, 1], h_misali_variance_values[:, 2], color="red", label="Desalinhamento horizontal")
    axis.scatter(v_misali_variance_values[:, 0], v_misali_variance_values[:, 1], v_misali_variance_values[:, 2], color="green", label="Desalinhamento vertical")
    axis.set_xlabel("Variancia do eixo X")
    axis.set_ylabel("Variancia do eixo Y")
    axis.set_zlabel("Variancia do eixo Z")
    axis.set_title("Variancia dos dados")
    axis.legend()

    kurtosis_values = np.asarray(normal_stats["kurtosis"])
    h_misali_kurtosis_values = np.asarray(h_misali_stats["kurtosis"])
    v_misali_kurtosis_values = np.asarray(v_misali_stats["kurtosis"])
    figure = plt.figure(num=3,figsize=(8, 8))
    axis = figure.add_subplot(projection="3d")
    axis.scatter(kurtosis_values[:, 0], kurtosis_values[:, 1], kurtosis_values[:, 2], color="blue", label="Normal")
    axis.scatter(h_misali_kurtosis_values[:, 0], h_misali_kurtosis_values[:, 1], h_misali_kurtosis_values[:, 2], color="red", label="Desalinhamento horizontal")
    axis.scatter(v_misali_kurtosis_values[:, 0], v_misali_kurtosis_values[:, 1], v_misali_kurtosis_values[:, 2], color="green", label="Desalinhamento vertical")
    axis.set_xlabel("Kurtosis do eixo X")
    axis.set_ylabel("Kurtosis do eixo Y")
    axis.set_zlabel("Kurtosis do eixo Z")
    axis.set_title("Kurtosis dos dados")
    axis.legend()

    skewness_values = np.asarray(normal_stats["skewness"])
    h_misali_skewness_values = np.asarray(h_misali_stats["skewness"])
    v_misali_skewness_values = np.asarray(v_misali_stats["skewness"])
    figure = plt.figure(num=4,figsize=(8, 8))
    axis = figure.add_subplot(projection="3d")
    axis.scatter(skewness_values[:, 0], skewness_values[:, 1], skewness_values[:, 2], color="blue", label="Normal")
    axis.scatter(h_misali_skewness_values[:, 0], h_misali_skewness_values[:, 1], h_misali_skewness_values[:, 2], color="red", label="Desalinhamento horizontal")
    axis.scatter(v_misali_skewness_values[:, 0], v_misali_skewness_values[:, 1], v_misali_skewness_values[:, 2], color="green", label="Desalinhamento vertical")
    axis.set_xlabel("Obliquidade do eixo X")
    axis.set_ylabel("Obliquidade do eixo Y")
    axis.set_zlabel("Obliquidade do eixo Z")
    axis.set_title("Obliquidade dos dados")
    axis.legend()


    plt.show()
