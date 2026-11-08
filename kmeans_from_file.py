import argparse
from pathlib import Path

import numpy as np
from scipy.io import loadmat
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans

from plot_results import plot_confusion_matrix, show_plots
from preprocessing import (
    create_balanced_train_test_sets,
    normalize_features,
    reduce_dimensions,
)


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
parser.add_argument(
    "--scaling",
    choices=("minmax", "standard", "none"),
    default="none",
    help=(
        "Normalização das features: 'minmax' (padrão), 'standard' "
        "(média zero e desvio padrão um) ou 'none' (sem normalização)."
    ),
)
parser.add_argument(
    "--reduction",
    choices=("pca", "ica"),
    default=None,
    help="Redução de dimensionalidade antes do KMeans: PCA ou ICA (padrão: nenhuma).",
)
parser.add_argument(
    "--n-components",
    type=int,
    default=3,
    help="Número de componentes para PCA/ICA (padrão: 3).",
)
parser.add_argument(
    "--plot-training",
    "--plot-training-confusion-matrix",
    dest="plot_training",
    action="store_true",
    help="Também gera a matriz de confusão para os dados de treino.",
)
args, unknown_args = parser.parse_known_args()
unexpected_args = [arg for arg in unknown_args if not arg.startswith("--f=")]
if unexpected_args:
    parser.error(f"unrecognized arguments: {' '.join(unexpected_args)}")

input_mat_path = args.mat_file
mat_data = loadmat(input_mat_path)
prepared = create_balanced_train_test_sets(mat_data["data"])

features_train, features_test, scaling_description = normalize_features(
    prepared.features_train,
    prepared.features_test,
    args.scaling,
)
features_train, features_test, reduction_description = reduce_dimensions(
    features_train,
    features_test,
    args.reduction,
    args.n_components,
)
preprocessing_description = (
    f"{scaling_description}; {reduction_description}; "
    f"NaN/Inf removidas: {prepared.removed_rows}"
)

kmeans_model = KMeans(
    n_clusters=len(prepared.classes),
    n_init=20,
    random_state=42,
).fit(features_train)

# Associa os IDs arbitrários dos clusters às categorias usando somente o treino.
train_cluster_counts = np.zeros(
    (len(prepared.classes), kmeans_model.n_clusters),
    dtype=int,
)
for class_index, class_value in enumerate(prepared.classes):
    for cluster_index in range(kmeans_model.n_clusters):
        train_cluster_counts[class_index, cluster_index] = np.count_nonzero(
            (prepared.labels_train == class_value)
            & (kmeans_model.labels_ == cluster_index)
        )
class_indices, cluster_indices = linear_sum_assignment(-train_cluster_counts)
cluster_to_condition = {
    cluster_index: prepared.classes[class_index]
    for class_index, cluster_index in zip(class_indices, cluster_indices)
}

train_clusters = kmeans_model.labels_
test_clusters = kmeans_model.predict(features_test)
predicted_train_labels = np.asarray(
    [cluster_to_condition[cluster] for cluster in train_clusters]
)
predicted_test_labels = np.asarray(
    [cluster_to_condition[cluster] for cluster in test_clusters]
)

model_description = (
    f"KMeans: n_clusters={len(prepared.classes)}, n_init=20, random_state=42"
)
print("Categorias (ordem da matriz):", prepared.classes)
print("Pré-processamento:", preprocessing_description)
print(model_description)

plot_confusion_matrix(
    prepared.labels_test,
    predicted_test_labels,
    prepared.classes,
    input_mat_path,
    "KMeans",
    "teste",
    model_description,
    preprocessing_description,
)
if args.plot_training:
    plot_confusion_matrix(
        prepared.labels_train,
        predicted_train_labels,
        prepared.classes,
        input_mat_path,
        "KMeans",
        "treino",
        model_description,
        preprocessing_description,
    )

show_plots()
