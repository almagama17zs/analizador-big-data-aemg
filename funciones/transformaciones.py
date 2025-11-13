# funciones/transformaciones.py
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from funciones.analisis import prepare_display_df, base_grid_from_df, CUSTOM_CSS_COMMON, calc_height_for_rows

# =======================
# 🗑️ DELETE COLUMN
# =======================
def eliminar_columna(df: pd.DataFrame) -> pd.DataFrame:
    """
    Streamlit UI to delete a column from the DataFrame.
    Supports undo last deletion and shows updated DataFrame.
    """
    st.subheader("🗑️ Eliminar columna")

    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados.")
        return df

    if "df_backup" not in st.session_state or st.session_state.df_backup.shape[1] != df.shape[1]:
        st.session_state.df_backup = df.copy()

    col_to_drop = st.selectbox("Selecciona la columna a eliminar", df.columns, key="drop_col")

    if st.button(f"Eliminar columna '{col_to_drop}'", key="btn_drop_col"):
        df = df.drop(columns=[col_to_drop])
        st.success(f"✅ Columna '{col_to_drop}' eliminada.")

    if st.button("↩️ Deshacer última eliminación", key="btn_undo_col"):
        if "df_backup" in st.session_state:
            df = st.session_state.df_backup.copy()
            st.success("↩️ Se ha restaurado la columna eliminada.")

    mostrar_df_actualizado(df)
    return df

# =======================
# 🔄 REPLACE VALUES
# =======================
def reemplazar_valor(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace specific values in a selected column.
    Supports undo and displays updated DataFrame.
    """
    st.subheader("♻️ Reemplazar valores en columna")

    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados.")
        return df

    if "df_backup" not in st.session_state:
        st.session_state.df_backup = df.copy()

    col_name = st.selectbox("Selecciona columna para reemplazar valores", df.columns, key="replace_col")
    if col_name:
        valor_viejo = st.text_input("Valor a reemplazar", key="old_val")
        valor_nuevo = st.text_input("Nuevo valor", key="new_val")

        if st.button("Reemplazar valor", key="btn_replace_val"):
            df[col_name] = df[col_name].replace(valor_viejo, valor_nuevo)
            st.success(f"✅ Valores '{valor_viejo}' reemplazados por '{valor_nuevo}' en columna '{col_name}'.")

    if st.button("↩️ Deshacer cambios", key="btn_undo_replace"):
        if "df_backup" in st.session_state:
            df = st.session_state.df_backup.copy()
            st.success("↩️ Cambios deshechos.")

    mostrar_df_actualizado(df)
    return df

# =======================
# 🧹 REMOVE DUPLICATES
# =======================
def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame.
    Supports undo and shows updated table.
    """
    st.subheader("🧹 Eliminar filas duplicadas")

    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados.")
        return df

    if "df_backup" not in st.session_state:
        st.session_state.df_backup = df.copy()

    if st.button("Eliminar duplicados", key="btn_drop_duplicates"):
        count_antes = df.shape[0]
        df = df.drop_duplicates()
        count_despues = df.shape[0]
        st.success(f"✅ Filas duplicadas eliminadas: {count_antes - count_despues}")

    if st.button("↩️ Deshacer eliminación duplicados", key="btn_undo_duplicates"):
        if "df_backup" in st.session_state:
            df = st.session_state.df_backup.copy()
            st.success("↩️ Cambios deshechos.")

    from funciones.transformaciones import mostrar_df_actualizado
    mostrar_df_actualizado(df)
    return df

# =======================
# 🔍 SEARCH TEXT
# =======================
def buscar_texto(df: pd.DataFrame) -> pd.DataFrame:
    """
    Search partial text in a column and filter the DataFrame.
    """
    st.subheader("🔍 Buscar texto parcial en columna")

    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados.")
        return df

    col_name = st.selectbox("Selecciona columna para buscar texto parcial", df.columns, key="search_col")
    if col_name:
        texto = st.text_input("Texto a buscar", key="search_text")
        if st.button("Buscar", key="btn_search_text"):
            df_filtrado = df[df[col_name].astype(str).str.contains(texto, na=False)]
            st.success(f"✅ Resultados filtrados por '{texto}' en columna '{col_name}'")
            mostrar_df_actualizado(df_filtrado)
            return df_filtrado

    mostrar_df_actualizado(df)
    return df

# =======================
# ➕ CREATE COMBINED COLUMN
# =======================
def crear_columna_combinada(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine multiple columns into a new one.
    Supports undo and displays updated DataFrame.
    """
    st.subheader("➕ Crear columna combinada")

    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados.")
        return df

    if "df_backup" not in st.session_state:
        st.session_state.df_backup = df.copy()

    cols = st.multiselect("Selecciona columnas a combinar", df.columns)
    nuevo_nombre = st.text_input("Nombre de la nueva columna", key="new_col_name")
    separador = st.text_input("Separador (ej: espacio, coma, guion)", " ", key="sep_col")

    if st.button("Crear columna combinada", key="btn_create_col"):
        if cols and nuevo_nombre:
            df[nuevo_nombre] = df[cols].astype(str).agg(separador.join, axis=1)
            st.success(f"✅ Columna combinada '{nuevo_nombre}' creada.")

    if st.button("↩️ Deshacer última creación", key="btn_undo_create"):
        if "df_backup" in st.session_state:
            df = st.session_state.df_backup.copy()
            st.success("↩️ Se ha deshecho la creación de la columna combinada.")

    mostrar_df_actualizado(df)
    return df

# =======================
# 🧹 REMOVE ROWS WITH NA
# =======================
def eliminar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with null values.
    """
    st.subheader("🧹 Eliminar filas con valores nulos")

    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados.")
        return df

    if st.button("Eliminar filas con valores nulos", key="btn_drop_na"):
        count_antes = df.shape[0]
        df = df.dropna()
        count_despues = df.shape[0]
        st.success(f"✅ Filas eliminadas: {count_antes - count_despues} | Filas restantes: {count_despues}")

    mostrar_df_actualizado(df)
    return df

# =======================
# 🌟 AUXILIARY FUNCTION TO SHOW UPDATED DF
# =======================
def mostrar_df_actualizado(df: pd.DataFrame):
    """
    Display DataFrame with AgGrid, blue headers, truncated text, and CSV export.
    """
    df_disp = prepare_display_df(df, max_len=200)
    gb = base_grid_from_df(df_disp)
    for c in df_disp.columns:
        gb.configure_column(c, headerTooltip=f"Columna: {c}")

    height_grid = calc_height_for_rows(len(df_disp), row_height=34, header_extra=80, max_height=600)
    AgGrid(
        df_disp,
        gridOptions=gb.build(),
        theme="streamlit",
        fit_columns_on_grid_load=False,
        allow_unsafe_jscode=False,
        custom_css=CUSTOM_CSS_COMMON,
        height=height_grid,
    )

    # Export CSV button
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="💾 Exportar CSV actualizado",
        data=csv,
        file_name="datos_actualizados.csv",
        mime="text/csv",
    )
