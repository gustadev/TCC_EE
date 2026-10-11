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