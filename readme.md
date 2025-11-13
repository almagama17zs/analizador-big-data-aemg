# 📊 Analizador Big Data AEMG

Aplicación interactiva desarrollada con **Streamlit** para análisis, transformación y visualización de datos.  
Permite cargar archivos CSV, Excel o JSON, conectarse a bases de datos SQL y realizar operaciones comunes de análisis de Big Data de forma visual y sencilla.

---

## 🚀 Características principales

- Carga de datos desde archivos locales o bases SQL.
- Exploración y limpieza de datos (eliminar nulos, duplicados, columnas, etc.).
- Transformaciones y combinaciones de columnas.
- Visualizaciones con **Plotly**, **Matplotlib** y **Seaborn**.
- Estadísticas agrupadas.
- Exportación de resultados.

---

## 🗂️ Estructura del proyecto
analizador_big_data_aemg/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── .streamlit/
│ └── config.toml
│
├── assets/
│ ├── logo.png
│ └── logo_favicon.png
│
├── funciones/
│ ├── init.py
│ ├── analisis.py
│ ├── carga.py
│ ├── exportacion.py
│ ├── graficos.py
│ ├── sql.py
│ └── transformaciones.py
└──
---

## 🧩 Requisitos

- Python 3.8 o superior  
- Streamlit  
- Pandas, NumPy, Plotly, Seaborn, Matplotlib, Scikit-learn, SQLAlchemy, OpenPyXL  

Todas las dependencias se instalan automáticamente desde el archivo `requirements.txt`.

--- 

## ⚙️ Instalación local

1. Clona el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/analizador_big_data_aemg.git
   cd analizador_big_data_aemg