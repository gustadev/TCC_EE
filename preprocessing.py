from dataclasses import dataclass

import numpy as np
from sklearn.decomposition import FastICA, PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler


@dataclass
class TrainTestSets:
    features_train: np.ndarray
    labels_train: np.ndarray
    features_test: np.ndarray
    labels_test: np.ndarray
    classes: np.ndarray
    removed_rows: int


def create_balanced_train_test_sets(data: np.ndarray) -> TrainTestSets:
    """Separa os dados do MAT e balanceia o conjunto de treino por categoria.

    O formato da matriz é: indicador de treino (1=treino, 0=teste), categoria
    e features. Linhas com NaN ou infinito são descartadas. O teste mantém todas
    as linhas válidas; o treino fica com a quantidade da menor categoria.
    """
    data = np.asarray(data, dtype=float)
    if data.ndim != 2 or data.shape[1] < 3:
        raise ValueError(
            "O campo 'data' precisa conter treino, condicao e ao menos uma feature."
        )

    train_flag = data[:, 0]
    condition = data[:, 1]
    features = data[:, 2:]
    valid_rows = (
        np.isfinite(train_flag)
        & np.isfinite(condition)
        & np.isfinite(features).all(axis=1)
    )
    removed_rows = int(np.count_nonzero(~valid_rows))
    train_flag = train_flag[valid_rows]
    condition = condition[valid_rows]
    features = features[valid_rows]

    if not np.isin(train_flag, (0, 1)).all():
        raise ValueError(
            "A primeira coluna deve conter somente 0 (teste) ou 1 (treino)."
        )

    train_mask = train_flag == 1
    test_mask = train_flag == 0
    features_train = features[train_mask]
    labels_train = condition[train_mask]
    features_test = features[test_mask]
    labels_test = condition[test_mask]

    if features_train.shape[0] == 0 or features_test.shape[0] == 0:
        raise ValueError("O arquivo precisa conter dados de treino e de teste.")

    classes = np.unique(labels_train)
    if len(classes) < 2:
        raise ValueError("O treino precisa conter pelo menos duas categorias.")
    if not np.isin(labels_test, classes).all():
        raise ValueError("Há categorias no teste que não aparecem nos dados de treino.")

    features_by_class = [
        features_train[labels_train == value] for value in classes
    ]
    labels_by_class = [labels_train[labels_train == value] for value in classes]
    balanced_class_size = min(labels.size for labels in labels_by_class)

    features_train = np.concatenate(
        [values[:balanced_class_size] for values in features_by_class], axis=0
    )
    labels_train = np.concatenate(
        [values[:balanced_class_size] for values in labels_by_class], axis=0
    )

    return TrainTestSets(
        features_train=features_train,
        labels_train=labels_train,
        features_test=features_test,
        labels_test=labels_test,
        classes=np.unique(labels_train),
        removed_rows=removed_rows,
    )


def normalize_features(
    features_train: np.ndarray,
    features_test: np.ndarray,
    method: str = "minmax",
) -> tuple[np.ndarray, np.ndarray, str]:
    """Ajusta a normalização no treino e aplica a transformação ao teste."""
    if method == "minmax":
        scaler = MinMaxScaler()
        description = "MinMaxScaler"
    elif method == "standard":
        scaler = StandardScaler()
        description = "StandardScaler (média zero, desvio padrão um)"
    elif method == "none":
        return features_train, features_test, "sem normalização"
    else:
        raise ValueError("A normalização deve ser 'minmax', 'standard' ou 'none'.")

    features_train = scaler.fit_transform(features_train)
    features_test = scaler.transform(features_test)
    return features_train, features_test, description


def reduce_dimensions(
    features_train: np.ndarray,
    features_test: np.ndarray,
    method: str | None = None,
    n_components: int = 3,
) -> tuple[np.ndarray, np.ndarray, str]:
    """Ajusta PCA ou ICA no treino e transforma os conjuntos de treino e teste."""
    if method is None:
        return features_train, features_test, "sem redução de dimensionalidade"
    if method not in ("pca", "ica"):
        raise ValueError("A redução deve ser 'pca', 'ica' ou None.")
    if n_components < 1:
        raise ValueError("--n-components deve ser um inteiro positivo.")

    max_components = min(features_train.shape)
    if n_components > max_components:
        raise ValueError(
            f"--n-components={n_components} excede o máximo permitido "
            f"({max_components}) para os dados de treino."
        )

    if method == "pca":
        reducer = PCA(n_components=n_components)
    else:
        reducer = FastICA(n_components=n_components, random_state=42)

    features_train = reducer.fit_transform(features_train)
    features_test = reducer.transform(features_test)
    return (
        features_train,
        features_test,
        f"{method.upper()} ({n_components} componentes)",
    )
