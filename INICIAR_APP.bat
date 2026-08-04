@echo off
title Academia de Riesgos Financieros
cd /d "%~dp0"

if not exist ".venv" (
    echo Creando entorno virtual...
    python -m venv .venv
)

call .venv\Scripts\activate

echo Instalando o verificando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Abriendo la aplicacion...
streamlit run app.py
pause
