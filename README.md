# PFC Software

## Instalação de Requisitos

### Linux
Cria e ativa a `.venv`; em seguida, instala as dependencias do projeto.
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Windows (PowerShell)
Cria e ativa a `.venv`; em seguida, instala as dependencias do projeto.
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Utilizando os scripts
Apos ativar o ambiente virtual (Linux: `source .venv/bin/activate`; Windows: `.venv\Scripts\Activate.ps1`), execute os scripts com `python script.py`.

### Gerar conjuntos MAT para classificação
Com o PostgreSQL configurado, execute o shellscript:
```bash
bash gerar_arquivos.sh
```

Ele salva os arquivos em `Dados_Processados/fatiados` e `Dados_Processados/inteiros`: nove arquivos para comparações entre `normal` e cada falha, além de `all_conditions_all_features.mat` com todas as condições em cada pasta. Cada arquivo contém a matriz `data` e os nomes das colunas em `parameter_names`.

A conexão usa `DATABASE_URL` ou `postgresql://admin:1234@localhost:5432/database`. Para usar outra conexão:
```bash
DATABASE_URL=postgresql://usuario:senha@localhost:5432/database bash gerar_arquivos.sh
```

### Executar o KMeans e gerar a matriz de confusão
Depois de gerar o arquivo MAT, escolha o tipo de normalização:
```bash
python kmeans_from_file.py caminho/arquivo.mat --scaling minmax
python kmeans_from_file.py caminho/arquivo.mat --scaling standard
python kmeans_from_file.py caminho/arquivo.mat --scaling none
python kmeans_from_file.py caminho/arquivo.mat --scaling standard --reduction pca --n-components 3
python kmeans_from_file.py caminho/arquivo.mat --scaling standard --reduction ica --n-components 3
```

`--scaling` aceita `minmax` (padrão), `standard` (centraliza pela média e divide pelo desvio padrão) ou `none` (desativa a normalização). O arquivo MAT pode ser omitido para usar `Dados_Processados/normal_vs_horiz_misali.mat`.

`--reduction` seleciona `pca` ou `ica`; sem essa opção, nenhuma redução é aplicada. `--n-components` define a quantidade de componentes (padrão: 3). A redução é ajustada usando somente os dados de treino e depois aplicada aos dados de teste.
