import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, f1_score
from sklearn.preprocessing import MinMaxScaler


DEFAULT_INPUT_MAT_PATH = Path("Dados_Processados/normal_vs_horiz_misali.mat")
parser = argparse.ArgumentParser(
    description="Executa KMeans em dados de um arquivo .mat e gera a matriz de confusão."
)
parser.add_argument(
    "mat_file",
    nargs="?",
    default=DEFAULT_INPUT_MAT_PATH,
    type=Path,
    help=f"Arquivo .mat de entrada (padrão: {DEFAULT_INPUT_MAT_PATH})",
)
INPUT_MAT_PATH = parser.parse_args().mat_file
OUTPUT_PLOT_PATH = INPUT_MAT_PATH.with_name(
    f"{INPUT_MAT_PATH.stem}_matriz_confusao.png"
)


mat_data = loadmat(INPUT_MAT_PATH)
data = np.asarray(mat_data["data"], dtype=float)

if data.ndim != 2 or data.shape[1] < 3:
    raise ValueError(
        "O campo 'data' precisa conter treino, condicao e ao menos uma feature."
    )

# Colunas: treino (1 = treino, 0 = teste), condicao e features.
train_flag = data[:, 0]
condition = data[:, 1]
features = data[:, 2:]

# Remove linhas com valores ausentes ou infinitos.
valid_rows = (
    np.isfinite(train_flag)
    & np.isfinite(condition)
    & np.isfinite(features).all(axis=1)
)
removed_rows = np.count_nonzero(~valid_rows)
train_flag = train_flag[valid_rows]
condition = condition[valid_rows]
features = features[valid_rows]

if not np.isin(train_flag, (0, 1)).all():
    raise ValueError("A primeira coluna deve conter somente 0 (teste) ou 1 (treino).")

train_mask = train_flag == 1
test_mask = train_flag == 0
features_train = features[train_mask]
features_test = features[test_mask]
labels_train = condition[train_mask]
labels_test = condition[test_mask]
classes = np.unique(labels_train)

if features_train.shape[0] == 0 or features_test.shape[0] == 0:
    raise ValueError("O arquivo precisa conter dados de treino e de teste.")
if len(classes) < 2:
    raise ValueError("O treino precisa conter pelo menos duas categorias.")
if not np.isin(labels_test, classes).all():
    raise ValueError("Há categorias no teste que não aparecem nos dados de treino.")

# Ajusta a escala somente no treino e aplica os mesmos parâmetros ao teste.
scaler = MinMaxScaler()
features_train = scaler.fit_transform(features_train)
features_test = scaler.transform(features_test)
preprocessing_description =  f"MinMaxScaler, NaN/Inf removidas: {removed_rows}"

kmeans_model = KMeans(
    n_clusters=len(classes),
    n_init=20,
    random_state=42,
).fit(features_train)

# Associa os IDs arbitrários dos clusters às categorias usando somente o treino.
train_cluster_counts = np.zeros(
    (len(classes), kmeans_model.n_clusters),
    dtype=int,
)
for class_index, class_value in enumerate(classes):
    for cluster_index in range(kmeans_model.n_clusters):
        train_cluster_counts[class_index, cluster_index] = np.count_nonzero(
            (labels_train == class_value)
            & (kmeans_model.labels_ == cluster_index)
        )
class_indices, cluster_indices = linear_sum_assignment(-train_cluster_counts)
cluster_to_condition = {
    cluster_index: classes[class_index]
    for class_index, cluster_index in zip(class_indices, cluster_indices)
}

test_clusters = kmeans_model.predict(features_test)
predicted_labels = np.asarray(
    [cluster_to_condition[cluster] for cluster in test_clusters]
)

matrix = confusion_matrix(labels_test, predicted_labels, labels=classes)
f1 = f1_score(
    labels_test,
    predicted_labels,
    labels=classes,
    average="macro",
    zero_division=0,
)

print("Categorias (ordem da matriz):", classes)
print("Matriz de confusão (linhas = real, colunas = previsto):")
print(matrix)
print("F1-score (macro):", f1)
print("Pré-processamento:", preprocessing_description)
print(f"KMeans: n_clusters={len(classes)}, n_init=20, random_state=42")

display = ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=classes)
display.plot(cmap="Blues", values_format="d", xticks_rotation="vertical")
figure = display.figure_
figure.suptitle(f"Matriz de confusão — {INPUT_MAT_PATH.name}")
figure.text(
    0.5,
    0.01,
    f"F1 macro: {f1:.4f}" # | KMeans: n_clusters={len(classes)}, n_init=20, "
    f"random_state=42\nPré-processamento: {preprocessing_description}",
    ha="center",
    va="bottom",
    wrap=True,
)
figure.tight_layout(rect=(0, 0.12, 1, 0.93))
figure.savefig(OUTPUT_PLOT_PATH, dpi=150, bbox_inches="tight")
print("Gráfico salvo em:", OUTPUT_PLOT_PATH)
plt.show()
