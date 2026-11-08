from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    confusion_matrix,
    f1_score,
)


def _available_output_path(
    input_path: Path,
    classifier_name: str,
    data_split: str,
) -> Path:
    base_name = f"{input_path.stem}_{classifier_name}_{data_split}_matriz_confusao"
    output_path = input_path.with_name(f"{base_name}_1.png")
    index = 1
    while output_path.exists():
        index += 1
        output_path = input_path.with_name(f"{base_name}_{index}.png")
    return output_path


def plot_confusion_matrix(
    actual_labels,
    predicted_labels,
    classes,
    input_path: Path,
    classifier_name: str,
    data_split: str,
    model_description: str,
    preprocessing_description: str,
) -> tuple:
    """Gera, exibe e salva a matriz de confusão e as métricas do classificador."""
    matrix = confusion_matrix(actual_labels, predicted_labels, labels=classes)
    true_positives = np.diag(matrix)
    false_negatives = matrix.sum(axis=1) - true_positives
    false_positives = matrix.sum(axis=0) - true_positives
    true_negatives = matrix.sum() - (
        true_positives + false_negatives + false_positives
    )

    sensitivity_by_class = np.divide(
        true_positives,
        true_positives + false_negatives,
        out=np.zeros_like(true_positives, dtype=float),
        where=(true_positives + false_negatives) != 0,
    )
    specificity_by_class = np.divide(
        true_negatives,
        true_negatives + false_positives,
        out=np.zeros_like(true_negatives, dtype=float),
        where=(true_negatives + false_positives) != 0,
    )
    accuracy = accuracy_score(actual_labels, predicted_labels)
    sensitivity = sensitivity_by_class.mean()
    specificity = specificity_by_class.mean()
    f1 = f1_score(
        actual_labels,
        predicted_labels,
        labels=classes,
        average="macro",
        zero_division=0,
    )

    print(f"Matriz de confusão ({data_split}; linhas = real, colunas = previsto):")
    print(matrix)
    print(f"Acurácia ({data_split}): {accuracy:.4f}")
    print(f"Sensibilidade macro ({data_split}): {sensitivity:.4f}")
    print(f"Especificidade macro ({data_split}): {specificity:.4f}")
    print(f"F1-score macro ({data_split}): {f1:.4f}")

    display = ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=classes)
    display.plot(cmap="Blues", values_format="d", xticks_rotation="vertical")
    figure = display.figure_
    figure.suptitle(
        f"Matriz de confusão — {input_path.name} ({classifier_name}, {data_split})"
    )
    figure.text(
        0.5,
        0.01,
        f"Acurácia: {accuracy:.4f} | Sensibilidade macro: {sensitivity:.4f}\n"
        f"Especificidade macro: {specificity:.4f} | F1 macro: {f1:.4f}\n"
        f"{model_description}\n"
        f"Pré-processamento: {preprocessing_description}",
        ha="center",
        va="bottom",
        wrap=True,
    )
    figure.tight_layout(rect=(0, 0.19, 1, 0.93))

    output_path = _available_output_path(input_path, classifier_name, data_split)
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    print("Gráfico salvo em:", output_path)
    return matrix, f1, output_path


def show_plots() -> None:
    """Exibe as matrizes de confusão geradas nesta execução."""
    plt.show()
