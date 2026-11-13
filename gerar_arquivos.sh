#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
mkdir -p Dados_Processados/fatiados Dados_Processados/inteiros

./.venv/bin/python query_to_mat.py -q query_arquivo_fatiado.sql -o Dados_Processados/fatiados/normal_vs_under_ballfault_all_features.mat -c normal "underhang ball fault"
./.venv/bin/python query_to_mat.py -q query_arquivo_fatiado.sql -o Dados_Processados/fatiados/normal_vs_under_outerrace_all_features.mat -c normal "underhang outer race"
./.venv/bin/python query_to_mat.py -q query_arquivo_fatiado.sql -o Dados_Processados/fatiados/normal_vs_under_cagefault_all_features.mat -c normal "underhang cage fault"
./.venv/bin/python query_to_mat.py -q query_arquivo_fatiado.sql -o Dados_Processados/fatiados/normal_vs_over_ballfault_all_features.mat -c normal "overhang ball fault"
./.venv/bin/python query_to_mat.py -q query_arquivo_fatiado.sql -o Dados_Processados/fatiados/normal_vs_over_outerrace_all_features.mat -c normal "overhang outer race"
./.venv/bin/python query_to_mat.py -q query_arquivo_fatiado.sql -o Dados_Processados/fatiados/normal_vs_over_cagefault_all_features.mat -c normal "overhang cage fault"
./.venv/bin/python query_to_mat.py -q query_arquivo_fatiado.sql -o Dados_Processados/fatiados/normal_vs_horiz_misali_all_features.mat -c normal "horizontal misalignment"
./.venv/bin/python query_to_mat.py -q query_arquivo_fatiado.sql -o Dados_Processados/fatiados/normal_vs_vert_misali_all_features.mat -c normal "vertical misalignment"
./.venv/bin/python query_to_mat.py -q query_arquivo_fatiado.sql -o Dados_Processados/fatiados/normal_vs_imbalance_all_features.mat -c normal imbalance
./.venv/bin/python query_to_mat.py -q query_arquivo_fatiado.sql -o Dados_Processados/fatiados/all_conditions_all_features.mat -c normal "underhang ball fault" "underhang outer race" "underhang cage fault" "overhang ball fault" "overhang outer race" "overhang cage fault" "horizontal misalignment" "vertical misalignment" imbalance

./.venv/bin/python query_to_mat.py -q query_arquivo_inteiro.sql -o Dados_Processados/inteiros/normal_vs_under_ballfault_all_features.mat -c normal "underhang ball fault"
./.venv/bin/python query_to_mat.py -q query_arquivo_inteiro.sql -o Dados_Processados/inteiros/normal_vs_under_outerrace_all_features.mat -c normal "underhang outer race"
./.venv/bin/python query_to_mat.py -q query_arquivo_inteiro.sql -o Dados_Processados/inteiros/normal_vs_under_cagefault_all_features.mat -c normal "underhang cage fault"
./.venv/bin/python query_to_mat.py -q query_arquivo_inteiro.sql -o Dados_Processados/inteiros/normal_vs_over_ballfault_all_features.mat -c normal "overhang ball fault"
./.venv/bin/python query_to_mat.py -q query_arquivo_inteiro.sql -o Dados_Processados/inteiros/normal_vs_over_outerrace_all_features.mat -c normal "overhang outer race"
./.venv/bin/python query_to_mat.py -q query_arquivo_inteiro.sql -o Dados_Processados/inteiros/normal_vs_over_cagefault_all_features.mat -c normal "overhang cage fault"
./.venv/bin/python query_to_mat.py -q query_arquivo_inteiro.sql -o Dados_Processados/inteiros/normal_vs_horiz_misali_all_features.mat -c normal "horizontal misalignment"
./.venv/bin/python query_to_mat.py -q query_arquivo_inteiro.sql -o Dados_Processados/inteiros/normal_vs_vert_misali_all_features.mat -c normal "vertical misalignment"
./.venv/bin/python query_to_mat.py -q query_arquivo_inteiro.sql -o Dados_Processados/inteiros/normal_vs_imbalance_all_features.mat -c normal imbalance
./.venv/bin/python query_to_mat.py -q query_arquivo_inteiro.sql -o Dados_Processados/inteiros/all_conditions_all_features.mat -c normal "underhang ball fault" "underhang outer race" "underhang cage fault" "overhang ball fault" "overhang outer race" "overhang cage fault" "horizontal misalignment" "vertical misalignment" imbalance

echo "Geração dos arquivos concluída com sucesso."
