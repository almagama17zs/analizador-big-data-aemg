import pandas as pd
import streamlit as st

def cargar_archivo(archivo):
    try:
        nombre = archivo.name.lower()

        if nombre.endswith(".csv"):
            df = pd.read_csv(archivo)
        elif nombre.endswith(".json"):
            df = pd.read_json(archivo)
        elif nombre.endswith(".xlsx"):
            df = pd.read_excel(archivo)
        else:
            st.error("❌ Formato no soportado. Usa CSV, JSON o XLSX.")
            return None

        if df.empty:
            st.warning("⚠️ El archivo está vacío.")
            return None

        return df

    except Exception as e:
        st.error(f"❌ Error al cargar el archivo: {e}")
        return None

