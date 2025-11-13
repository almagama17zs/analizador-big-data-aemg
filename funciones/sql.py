# funciones/sql.py
import streamlit as st
from pyspark.sql import SparkSession

def cargar_desde_sql():
    """
    Streamlit interface to load data from a SQL database using Spark.
    Allows selecting the database type and automatically generates the JDBC URL.
    """
    st.subheader("⚙️ Conexión a base de datos SQL")

    # ===== Select database engine =====
    tipo_db = st.selectbox(
        "🗄️ Tipo de base de datos",
        ["MySQL", "PostgreSQL", "SQL Server", "Oracle", "SQLite"],
        index=0
    )

    # Suggested base JDBC URLs
    jdbc_bases = {
        "MySQL": "jdbc:mysql://host:3306/nombre_base",
        "PostgreSQL": "jdbc:postgresql://host:5432/nombre_base",
        "SQL Server": "jdbc:sqlserver://host:1433;databaseName=nombre_base",
        "Oracle": "jdbc:oracle:thin:@host:1521:nombre_base",
        "SQLite": "jdbc:sqlite:/ruta/al/archivo.db"
    }

    # User input for connection parameters
    url = st.text_input("🔗 URL de conexión JDBC", value=jdbc_bases[tipo_db])
    tabla = st.text_input(
        "📋 Nombre de la tabla o consulta SQL (usa paréntesis si es SELECT)",
        placeholder="mi_tabla o (SELECT * FROM tabla)"
    )
    usuario = st.text_input("👤 Usuario", placeholder="usuario", key="sql_user")
    contrasena = st.text_input("🔒 Contraseña", type="password", key="sql_password")

    # ===== Button to execute load =====
    if st.button("🚀 Cargar datos desde SQL"):
        # Validate input fields
        if tipo_db != "SQLite" and not all([url, tabla, usuario, contrasena]):
            st.warning("⚠️ Completa todos los campos para conectar.")
            return None
        if tipo_db == "SQLite" and not url:
            st.warning("⚠️ Indica la ruta al archivo .db de SQLite.")
            return None

        try:
            # Initialize Spark session
            spark = SparkSession.builder.appName("AnalizadorBigData").getOrCreate()
            reader = spark.read.format("jdbc").option("url", url).option("dbtable", tabla)

            if tipo_db != "SQLite":
                reader = reader.option("user", usuario).option("password", contrasena)

            # Load data
            df = reader.load()

            st.success(f"✅ Datos cargados correctamente desde {tipo_db}. Filas: {df.count()} — Columnas: {len(df.columns)}")
            return df

        except Exception as e:
            st.error(f"❌ Error al cargar datos desde {tipo_db}: {e}")
            return None

    return None
