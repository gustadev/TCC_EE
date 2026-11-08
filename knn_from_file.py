import argparse
from pathlib import Path

from scipy.io import loadmat
from sklearn.neighbors import KNeighborsClassifier

from plot_results import plot_confusion_matrix, show_plots
from preprocessing import (
    create_balanced_train_test_sets,
    normalize_features,
    reduce_dimensions,
)


DEFAULT_INPUT_MAT_PATH = Path("Dados_Processados/normal_vs_horiz_misali.mat")
parser = argparse.ArgumentParser(
    description="Executa KNN em dados de um arquivo .mat e gera a matriz de confusão."
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
    help="Redução de dimensionalidade antes do KNN: PCA ou ICA (padrão: nenhuma).",
)
parser.add_argument(
    "--n-components",
    type=int,
    default=3,
    help="Número de componentes para PCA/ICA (padrão: 3).",
)
parser.add_argument(
    "--n-neighbors",
    type=int,
    default=5,
    help="Número de vizinhos usados pelo KNN (padrão: 5).",
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

if args.n_neighbors < 1:
    raise ValueError("--n-neighbors deve ser um inteiro positivo.")
if args.n_neighbors > prepared.features_train.shape[0]:
    raise ValueError(
        f"--n-neighbors={args.n_neighbors} excede o número de exemplos de treino "
        f"({prepared.features_train.shape[0]})."
    )

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

knn_model = KNeighborsClassifier(n_neighbors=args.n_neighbors)
knn_model.fit(features_train, prepared.labels_train)
predicted_test_labels = knn_model.predict(features_test)

model_description = (
    f"KNN: n_neighbors={args.n_neighbors}, weights='uniform', distância euclidiana"
)
print("Categorias (ordem da matriz):", prepared.classes)
print("Pré-processamento:", preprocessing_description)
print(model_description)

plot_confusion_matrix(
    prepared.labels_test,
    predicted_test_labels,
    prepared.classes,
    input_mat_path,
    "KNN",
    "teste",
    model_description,
    preprocessing_description,
)
if args.plot_training:
    predicted_train_labels = knn_model.predict(features_train)
    plot_confusion_matrix(
        prepared.labels_train,
        predicted_train_labels,
        prepared.classes,
        input_mat_path,
        "KNN",
        "treino",
        model_description,
        preprocessing_description,
    )

show_plots()
