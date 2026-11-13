
#%%
from scipy.io import loadmat
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler

# %%
# Carregar dados
data = loadmat(
    "Dados_Processados/inteiros/normal_vs_over_outerrace_all_features.mat"
)["data"][:, 2:]

# Nomes das variáveis na mesma ordem em que aparecem em query.sql
variaveis = [
    "acel_x1_variancia",
    "acel_x1_rms",
    "acel_x1_obliquidade",
    "acel_x1_curtose",
    "acel_x1_fator_crista",
    "acel_y1_variancia",
    "acel_y1_rms",
    "acel_y1_obliquidade",
    "acel_y1_curtose",
    "acel_y1_fator_crista",
    "acel_z1_variancia",
    "acel_z1_rms",
    "acel_z1_obliquidade",
    "acel_z1_curtose",
    "acel_z1_fator_crista",
    "acel_x2_variancia",
    "acel_x2_rms",
    "acel_x2_obliquidade",
    "acel_x2_curtose",
    "acel_x2_fator_crista",
    "acel_y2_variancia",
    "acel_y2_rms",
    "acel_y2_obliquidade",
    "acel_y2_curtose",
    "acel_y2_fator_crista",
    "acel_z2_variancia",
    "acel_z2_rms",
    "acel_z2_obliquidade",
    "acel_z2_curtose",
    "acel_z2_fator_crista",
    "mic_variancia",
    "mic_rms",
    "mic_obliquidade",
    "mic_curtose",
    "mic_fator_crista",
]
n_variaveis = data.shape[1]

# Padronização
scaler = StandardScaler()
data = scaler.fit_transform(data)

# Aplicar PCA
pca = PCA()
pca.fit(data)

# Variância explicada
variancia = pca.explained_variance_ratio_
variancia_acumulada = np.cumsum(variancia)
# %%
# Selecionar componentes que explicam 95% da variância
limite = 0.95

k = np.argmax(variancia_acumulada >= limite) + 1

print(f"Quantidade de variáveis originais: {n_variaveis}")
print(f"Componentes selecionados: {k}")
print(f"Variância explicada: {variancia_acumulada[k-1]*100:.2f}%")

# %%
# Calcular contribuição das features
autovalores = pca.explained_variance_[:k]
autovetores = pca.components_[:k, :].T

contribuicao = (autovetores ** 2) * autovalores

# Somar contribuições dos componentes selecionados
importancia = contribuicao.sum(axis=1)

# Normalizar para percentual
importancia_percentual = (
    importancia / importancia.sum()
) * 100

# %%
# Criar ranking
resultado = pd.DataFrame({
    "Variavel": variaveis,
    "Importancia": importancia_percentual
})

resultado = resultado.sort_values(
    by="Importancia",
    ascending=True
)

print("\nRanking das variáveis:")
print(resultado.to_string(index=False))

# %%
# Gráfico 1 - Variância explicada acumulada
plt.figure(figsize=(10, 5))

plt.plot(
    np.arange(1, len(variancia_acumulada) + 1),
    variancia_acumulada * 100,
    marker="o"
)

plt.axhline(
    y=limite * 100,
    linestyle="--",
    label=f"{limite*100:.0f}% de variância"
)

plt.axvline(
    x=k,
    linestyle="--",
    label=f"{k} componentes"
)

plt.xlabel("Componentes principais")
plt.ylabel("Variância acumulada (%)")
plt.title("Variância explicada acumulada - PCA")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Gráfico 2 - Contribuição das 35 features
plt.figure(figsize=(14, 8))

plt.barh(
    resultado["Variavel"],
    resultado["Importancia"],
    edgecolor="black"
)

plt.xlabel("Contribuição (%)")
plt.ylabel("Variáveis")
plt.title(f"Contribuição das features - PCA ({k} componentes)")
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.show()

# # %%
# # Gráfico 3 - Top 15 features
# top15 = resultado.tail(15)

# plt.figure(figsize=(10, 7))

# plt.barh(
#     top15["Variavel"],
#     top15["Importancia"],
#     edgecolor="black"
# )

# plt.xlabel("Contribuição (%)")
# plt.ylabel("Variáveis")
# plt.title("15 features com maior contribuição - PCA")
# plt.grid(axis="x", alpha=0.3)
# plt.tight_layout()
# plt.show()

# %%
