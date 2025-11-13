# funciones/graficos.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from funciones.analisis import prepare_display_df

# =========================
# 📊 HISTOGRAM
# =========================
def graficar_histograma(df: pd.DataFrame):
    """
    Plot a histogram for a numeric column
    """
    st.subheader("📊 Graficar histograma")
    
    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados.")
        return

    # Select numeric columns
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if not num_cols:
        st.info("⚠️ No hay columnas numéricas para graficar.")
        return

    col = st.selectbox("Selecciona columna para el histograma", num_cols, key="hist_col")
    bins = st.slider(
        "Número de bins (intervalos)", min_value=5, max_value=100, value=20,
        help="Número de intervalos en los que se divide el rango de valores."
    )

    # Plot histogram on button click
    if st.button("Graficar histograma", key="btn_hist"):
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df[col], bins=bins, kde=True, ax=ax, color="#007ACC")
        ax.set_title(f"Histograma de {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)

# =========================
# 📊 BAR CHART
# =========================
def graficar_barras(df: pd.DataFrame):
    """
    Plot a bar chart of numeric values aggregated by a categorical column
    """
    st.subheader("📊 Gráfico de barras")
    
    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados.")
        return

    # Select categorical and numeric columns
    cat_cols = [c for c in df.columns if df[c].dtype == "object" or df[c].dtype.name == "category"]
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

    if not cat_cols or not num_cols:
        st.info("⚠️ Se requiere al menos una columna categórica y una numérica.")
        return

    col_cat = st.selectbox("Columna categórica", cat_cols, key="bar_cat")
    col_num = st.selectbox("Columna numérica", num_cols, key="bar_num")

    top_n = st.slider(
        "Número máximo de categorías a mostrar", 5, 50, 15,
        help="Limita el número de barras visibles para evitar amontonamiento."
    )

    # Plot bar chart on button click
    if st.button("Graficar barras", key="btn_bar"):
        grouped = df.groupby(col_cat)[col_num].sum().reset_index().sort_values(col_num, ascending=False)
        grouped = grouped.head(top_n)
        
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=col_cat, y=col_num, data=grouped, ax=ax, palette="Blues_d")
        ax.set_title(f"{col_num} por {col_cat}")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)
