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

### Exportar uma consulta do PostgreSQL para MAT
Edite a constante `QUERY` em `query_to_mat.py` com a consulta desejada e execute:
```bash
python query_to_mat.py
```

O arquivo de saída é definido pela constante `OUTPUT_PATH`. A conexão usa `DATABASE_URL` ou `postgresql://admin:1234@localhost:5432/database`. A variável MATLAB `data` é uma matriz numérica com uma linha por resultado; `parameter_names` contém os nomes das colunas na mesma ordem.

### Gerar a matriz de confusão
Depois de gerar o arquivo MAT, execute:
```bash
python grafico_confusao.py
```

O script usa a primeira coluna como rótulo (`0` = Normal, `1` = Falha), treina um classificador SVM com as demais colunas e salva/exibe a matriz de confusão em `matriz_confusao.png`.
