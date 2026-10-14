import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np
from pathlib import Path
import scipy.io

from classes.dataset.hmisali import Hmisali
from classes.dataset.vmisali import Vmisali
from classes.dataset.normal import Normal
from classes.dataset.overhang import Overhang
from classes.dataset.underhang import Underhang

nf = 1
ns = 0 # 0 - Todos; > 0 - Indice da fatia
SPLIT_DATA = True
GENERATE_ANALYSIS_FILE = True
SAVE_SPLIT_COMBINED = True
SAVE_SPLIT_SEPARATE = True

datasets = {
	"Normal": Normal(),
	"Desalinhamento horizontal": Hmisali().set_lvl("2.0mm"),
	"Desalinhamento vertical": Vmisali().set_lvl("1.90mm"),
	"Overhang - esfera (35g)": Overhang().type("ball_fault").set_lvl("35g"),
	"Overhang - gaiola (35g)": Overhang().type("cage_fault").set_lvl("35g"),
	"Overhang - pista externa (35g)": Overhang().type("outer_race").set_lvl("35g"),
	"Underhang - esfera (35g)": Underhang().type("ball_fault").set_lvl("35g"),
	"Underhang - gaiola (35g)": Underhang().type("cage_fault").set_lvl("35g"),
	"Underhang - pista externa (35g)": Underhang().type("outer_race").set_lvl("35g"),
}

for dataset in datasets.values():
	dataset.set_file(dataset.list_files(True)[nf])


def calculate_variance(dataset):
	if SPLIT_DATA:
		segments = dataset.read_all(split=True)
		data = np.concatenate(segments) if ns == 0 else segments[ns]
	else:
		data = dataset.read_all()
	return np.var(data[:, 1:], axis=0)


def calculate_split_variances(dataset):
	return np.asarray([
		np.var(segment[:, 1:], axis=0)
		for segment in dataset.read_all(split=True)
	])


variances = {
	condition: calculate_variance(dataset)
	for condition, dataset in datasets.items()
}
channel_names = [
	"Acelerometro 1 - X",
	"Acelerometro 1 - Y",
	"Acelerometro 1 - Z",
	"Acelerometro 2 - X",
	"Acelerometro 2 - Y",
	"Acelerometro 2 - Z",
	"Som",
]

if GENERATE_ANALYSIS_FILE:
	analysis_directory = Path("Analises")
	analysis_directory.mkdir(exist_ok=True)
	if not SPLIT_DATA or SAVE_SPLIT_COMBINED:
		analysis_scope = (
			f"split_fatia_{ns}" if SPLIT_DATA and ns > 0
			else "split_junta" if SPLIT_DATA
			else "completo"
		)
		analysis_path = analysis_directory / f"variancia_{analysis_scope}.mat"
		scipy.io.savemat(
			analysis_path,
			{
				"variancia": np.vstack(list(variances.values())),
				"condition_labels": np.asarray(list(variances), dtype=object),
				"channel_labels": np.asarray(channel_names, dtype=object),
				"split_enabled": SPLIT_DATA,
				"segment_index": ns if SPLIT_DATA else -1,
			},
		)
		print(f"Analise conjunta salva em: {analysis_path}")

	if SPLIT_DATA and SAVE_SPLIT_SEPARATE:
		variances_by_segment = {
			condition: calculate_split_variances(dataset)
			for condition, dataset in datasets.items()
		}
		segment_counts = np.asarray([
			condition_variances.shape[0]
			for condition_variances in variances_by_segment.values()
		])
		separate_variances = np.full(
			(len(variances_by_segment), segment_counts.max(), len(channel_names)),
			np.nan,
		)
		for condition_index, condition_variances in enumerate(variances_by_segment.values()):
			separate_variances[condition_index, :condition_variances.shape[0], :] = condition_variances

		analysis_path = analysis_directory / "variancia_split_separada.mat"
		scipy.io.savemat(
			analysis_path,
			{
				"variancia_por_fatia": separate_variances,
				"segment_counts": segment_counts,
				"condition_labels": np.asarray(list(variances_by_segment), dtype=object),
				"channel_labels": np.asarray(channel_names, dtype=object),
				"split_enabled": True,
			},
		)
		print(f"Analise por fatia salva em: {analysis_path}")

conditions = list(variances)
condition_positions = np.arange(len(conditions))
columns = 2
rows = int(np.ceil(len(channel_names) / columns))
figure, axes = plt.subplots(rows, columns, figsize=(18, 4 * rows), layout="constrained")
figure.suptitle("Variancia por canal")

for channel, axis in enumerate(axes.flat):
	if channel >= len(channel_names):
		axis.set_visible(False)
		continue

	channel_variances = [values[channel] for values in variances.values()]
	axis.bar(condition_positions, channel_variances)
	axis.set_title(channel_names[channel])
	axis.set_ylabel("Variancia")
	axis.set_xticks(condition_positions, conditions, rotation=35, ha="right")
	axis.grid(axis="y", alpha=0.3)

plt.show()



