import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

def cargar_desde_sql():
    """
    Streamlit interface to load data from a SQL database using pandas + SQLAlchemy.
    Compatible with Streamlit Cloud (no PySpark required).
    """
    st.subheader("⚙️ Conexión a base de datos SQL")

    tipo_db = st.selectbox(
        "🗄️ Tipo de base de datos",
        ["SQLite", "MySQL", "PostgreSQL", "SQL Server", "Oracle"],
        index=0
    )

    ejemplos_url = {
        "SQLite": "sqlite:///ruta/al/archivo.db",
        "MySQL": "mysql+pymysql://usuario:contraseña@host:3306/nombre_base",
        "PostgreSQL": "postgresql+psycopg2://usuario:contraseña@host:5432/nombre_base",
        "SQL Server": "mssql+pyodbc://usuario:contraseña@host:1433/nombre_base?driver=ODBC+Driver+17+for+SQL+Server",
        "Oracle": "oracle+cx_oracle://usuario:contraseña@host:1521/nombre_base"
    }

    url = st.text_input("🔗 URL de conexión SQLAlchemy", value=ejemplos_url[tipo_db])
    tabla = st.text_input("📋 Nombre de la tabla o consulta SQL", placeholder="mi_tabla o SELECT * FROM tabla")

    if st.button("🚀 Cargar datos desde SQL"):
        if not url or not tabla:
            st.warning("⚠️ Debes ingresar la URL de conexión y el nombre de la tabla o consulta.")
            return None

        try:
            engine = create_engine(url)

            if tabla.strip().lower().startswith("select"):
                df = pd.read_sql_query(tabla, engine)
            else:
                df = pd.read_sql_table(tabla, engine)

            st.success(f"✅ Datos cargados correctamente. Filas: {len(df)} — Columnas: {len(df.columns)}")
            st.dataframe(df.head())
            return df

        except Exception as e:
            st.error(f"❌ Error al cargar datos desde SQL: {e}")
            return None

    return None
