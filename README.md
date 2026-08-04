# Academia de Gestión de Riesgos Financieros — Ecuador

Aplicación educativa desarrollada con Python y Streamlit para enseñar modelos de
gestión de riesgos aplicables a bancos y cooperativas de ahorro y crédito del Ecuador.

## Contenido

- Tablero ejecutivo y mapa integral de riesgos.
- Riesgo de crédito: score, probabilidad de incumplimiento y matriz de transición.
- Pérdida esperada: PD × LGD × EAD.
- Riesgo de liquidez: brechas por bandas, liquidez acumulada y escenarios.
- Riesgo de mercado: VaR histórico, paramétrico y estrés de tasas.
- Riesgo operativo: matriz probabilidad-impacto, eventos y controles.
- Pruebas de estrés integradas.
- Laboratorio de datos con carga de CSV o Excel.
- Glosario y referencias regulatorias ecuatorianas.

## Advertencia

Los datos, umbrales, resultados y modelos incluidos son simulados y tienen fines
exclusivamente educativos. No sustituyen la normativa vigente, la validación de
modelos, el criterio profesional, auditorías, políticas institucionales ni los
reportes requeridos por la Superintendencia de Bancos o la SEPS.

## Requisitos

- Python 3.10 o superior
- Visual Studio Code
- Extensión de Python para VS Code

## Instalación en Windows

1. Descomprima la carpeta.
2. Abra la carpeta completa en Visual Studio Code.
3. Abra una terminal en VS Code.
4. Ejecute:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

También puede ejecutar `INICIAR_APP.bat`.

## Instalación en macOS o Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Estructura

```text
Academia_Riesgos_Financieros_Ecuador/
├── app.py
├── requirements.txt
├── README.md
├── INICIAR_APP.bat
├── data/
│   └── cartera_demo.csv
├── modules/
│   ├── data_factory.py
│   └── calculations.py
└── .streamlit/
    └── config.toml
```
