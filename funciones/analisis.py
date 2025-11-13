# funciones/analisis.py
import streamlit as st
import pandas as pd
import locale
from st_aggrid import AgGrid, GridOptionsBuilder

# =========================================================
# 🌍 LOCALIZATION CONFIGURATION
# =========================================================
try:
    locale.setlocale(locale.LC_ALL, "")
except:
    locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")

# =========================================================
# 🎨 GLOBAL CSS — applies to all AgGrid tables
# =========================================================
GLOBAL_CSS = """
<style>
/* ======= Blue headers ======= */
.ag-theme-streamlit .ag-header-cell-label,
.ag-theme-streamlit .ag-header-cell-text {
    color: #007ACC !important;
    font-weight: 700 !important;
}
.blue-header .ag-header-cell-label,
.blue-header .ag-header-cell-text {
    color: #007ACC !important;
    font-weight: 700 !important;
}

/* ======= Compact cells ======= */
.ag-theme-streamlit .ag-cell {
    line-height: 18px !important;
    max-height: 36px !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}

/* ======= Force full width ======= */
.ag-root-wrapper, .ag-center-cols-container, .ag-body-viewport, .ag-center-cols-viewport {
    width: 100% !important;
    min-width: 100% !important;
}

/* ======= Remove bottom gap ======= */
.ag-root-wrapper-body, .ag-body-viewport, .ag-body-horizontal-scroll, .ag-center-cols-viewport {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}

/* ======= Compact expanders ======= */
div[data-testid="stExpander"] {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# =========================================================
# 🎨 Additional CSS injected into AgGrid iframe
# =========================================================
CUSTOM_CSS_COMMON = {
    ".ag-root-wrapper": {"width": "100% !important"},
    ".ag-center-cols-container": {"width": "100% !important"},
    ".ag-header-cell-label": {"color": "#007ACC !important", "font-weight": "700 !important"},
    ".ag-header-cell-text": {"color": "#007ACC !important", "font-weight": "700 !important"},
    ".blue-header .ag-header-cell-label": {"color": "#007ACC !important", "font-weight": "700 !important"},
}

# =========================================================
# 🧱 AUXILIARY FUNCTIONS
# =========================================================
def prepare_display_df(df: pd.DataFrame, max_len: int = 60) -> pd.DataFrame:
    """Truncate long text to avoid huge rows."""
    df_copy = df.copy()
    for c in df_copy.columns:
        df_copy[c] = df_copy[c].apply(
            lambda x: str(x)[:max_len] + "..." if isinstance(x, str) and len(str(x)) > max_len else x
        )
    return df_copy


def calc_height_for_rows(n_rows: int, row_height: int = 32, header_extra: int = 70, max_height: int = 700) -> int:
    """Estimate a reasonable AgGrid height based on the number of rows."""
    h = header_extra + n_rows * row_height
    h = int(h * 0.96)
    return min(max(h, 180), max_height)


def base_grid_from_df(df: pd.DataFrame) -> GridOptionsBuilder:
    """Create a compact and consistent GridOptionsBuilder."""
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        editable=False,
        resizable=True,
        sortable=True,
        wrapText=False,
        autoHeight=False,
        minWidth=100,
        maxWidth=350,
        headerClass="blue-header",
    )
    gb.configure_grid_options(
        domLayout="autoHeight", enableBrowserTooltips=True, suppressAutoSize=True
    )
    return gb


# =========================================================
# 🧠 GENERAL DATAFRAME INFORMATION
# =========================================================
def mostrar_info(df: pd.DataFrame):
    """Display structure, statistics, and first rows with AgGrid."""
    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados para analizar.")
        return

    # -----------------------------
    # STRUCTURE
    # -----------------------------
    with st.expander("🧱 Estructura del DataFrame", expanded=False):
        info_df = pd.DataFrame({
            "Encabezado": df.columns,
            "Tipo de datos": df.dtypes.astype(str),
            "Nulos": df.isna().sum(),
            "Valores únicos": df.nunique()
        }).reset_index(drop=True)

        # Tooltips
        tooltips_estructura = {
            "Encabezado": "Column name",
            "Tipo de datos": "Data type (int, float, object, datetime, etc.)",
            "Nulos": "Number of missing values (NaN)",
            "Valores únicos": "Number of distinct values in the column"
        }

        gb = base_grid_from_df(info_df)
        for col in info_df.columns:
            gb.configure_column(col, headerTooltip=tooltips_estructura.get(col, ""))

        custom_css_no_gap = {
            ".ag-center-cols-viewport": {"overflow-x": "hidden !important"},
            ".ag-body-horizontal-scroll": {"display": "none !important"},
            ".ag-center-cols-container": {"width": "100% !important"},
            ".ag-root-wrapper": {"width": "100% !important"},
            ".ag-header-cell-label": {"color": "#007ACC !important", "font-weight": "700 !important"},
            ".ag-header-cell-text": {"color": "#007ACC !important", "font-weight": "700 !important"},
        }

        height_info = calc_height_for_rows(len(info_df), row_height=34, header_extra=80, max_height=600)

        AgGrid(
            info_df,
            gridOptions=gb.build(),
            theme="streamlit",
            allow_unsafe_jscode=False,
            custom_css=custom_css_no_gap,
            height=height_info,
            fit_columns_on_grid_load=True,
        )

        st.info(
            "ℹ️ **Estructura:** columnas, tipos, nulos y valores únicos. "
            "Pasa el ratón sobre un encabezado para ver la explicación."
        )


# =========================================================
# 📄 DISPLAY COLUMN
# =========================================================
def mostrar_columna(df: pd.DataFrame):
    """Display data from a single column in AgGrid."""
    st.subheader("📄 Mostrar datos de una columna")
    columna = st.selectbox("Selecciona una columna", df.columns, key="show_col")

    if columna:
        col_df = df[[columna]].reset_index(drop=True)
        col_disp = prepare_display_df(col_df, max_len=10000)

        gb = GridOptionsBuilder.from_dataframe(col_disp)
        gb.configure_default_column(
            editable=False,
            resizable=True,
            sortable=True,
            wrapText=True,
            autoHeight=False,
            minWidth=300,
        )
        gb.configure_column(columna, headerClass="blue-header", headerTooltip=f"Columna: {columna}")
        gb.configure_grid_options(
            domLayout="normal",
            enableBrowserTooltips=True,
            suppressHorizontalScroll=False
        )

        # CSS definition
        custom_css_no_gap = {
            ".ag-root-wrapper": {"width": "100% !important"},
            ".ag-center-cols-container": {"width": "100% !important"},
            ".blue-header .ag-header-cell-label": {"color": "#007ACC !important", "font-weight": "700 !important"},
        }

        row_height = 32
        header_height = 36
        visible_rows = 20
        height = header_height + row_height * visible_rows

        AgGrid(
            col_disp,
            gridOptions=gb.build(),
            theme="streamlit",
            allow_unsafe_jscode=False,
            custom_css=custom_css_no_gap,
            height=height,
            fit_columns_on_grid_load=False,
        )


# =========================================================
# ↕️ SORT DATA
# =========================================================
def ordenar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Show full DataFrame, allow sorting by clicking headers, and enable CSV export."""
    st.subheader("↕️ Ordenar datos")

    # Working copy
    df_disp = prepare_display_df(df, max_len=120)

    # Configure AgGrid with blue headers and tooltips
    gb = base_grid_from_df(df_disp)
    for col in df_disp.columns:
        gb.configure_column(col, headerTooltip=f"Columna: {col}")

    # Set height for scrollable view (max 700 px)
    height_grid = calc_height_for_rows(len(df_disp), row_height=34, header_extra=80, max_height=700)

    # CSS — force scroll visible, blue headers, no ghost column
    custom_css_scroll = {
        ".ag-center-cols-viewport": {
            "overflow-x": "auto !important",
            "overflow-y": "auto !important",
        },
        ".ag-body-horizontal-scroll": {"display": "block !important"},
        ".ag-root-wrapper": {"width": "100% !important"},
        ".ag-center-cols-container": {"width": "100% !important"},
        ".ag-header-cell-label": {
            "color": "#007ACC !important",
            "font-weight": "700 !important",
        },
        ".blue-header .ag-header-cell-label": {
            "color": "#007ACC !important",
            "font-weight": "700 !important",
        },
    }

    # Display interactive AgGrid
    grid_response = AgGrid(
        df_disp,
        gridOptions=gb.build(),
        theme="streamlit",
        fit_columns_on_grid_load=False,
        allow_unsafe_jscode=False,
        custom_css=custom_css_scroll,
        height=height_grid,
    )

    # Retrieve sorted DataFrame from AgGrid
    sorted_df = pd.DataFrame(grid_response["data"])

    st.info("ℹ️ **Ordenar Datos:** Haz clic en cualquier encabezado para ordenar la columna de forma ascendente o descendente.")

    # ========================
    # 📤 Export sorted CSV
    # ========================
    csv = sorted_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="💾 Exportar CSV ordenado",
        data=csv,
        file_name="datos_ordenados.csv",
        mime="text/csv",
        help="Descarga el archivo con el orden actual mostrado en la tabla.",
    )

    return sorted_df


# =========================================================
# 📊 GROUP DATA
# =========================================================
def agrupar_datos(df: pd.DataFrame):
    """Group DataFrame by a categorical column and display stats for a numerical column."""
    st.subheader("📊 Agrupar datos por columna")

    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados.")
        return

    # Identify categorical and numerical columns
    cat_cols = [c for c in df.columns if df[c].dtype == 'object' or df[c].dtype.name == 'category']
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

    if not cat_cols or not num_cols:
        st.info("⚠️ Necesitas al menos una columna categórica y una numérica.")
        return

    col1, col2 = st.columns(2)
    with col1:
        group_col = st.selectbox("Selecciona columna para agrupar", cat_cols, key="group_col")
    with col2:
        val_col = st.selectbox("Selecciona columna numérica", num_cols, key="num_col")

    # Save result in session for persistence
    if "grouped_df" not in st.session_state:
        st.session_state.grouped_df = None

    if st.button("🔹 Calcular estadísticas", key="group_btn"):
        grouped_df = df.groupby(group_col)[val_col].describe().reset_index()
        st.session_state.grouped_df = grouped_df  # save result

    # Display table if result exists
    if st.session_state.grouped_df is not None:
        grouped_disp = prepare_display_df(st.session_state.grouped_df, max_len=200)
        gb = base_grid_from_df(grouped_disp)
        for col in grouped_disp.columns:
            gb.configure_column(col, headerTooltip=f"Columna: {col}")

        # CSS scroll + blue headers
        custom_css_scroll = {
            ".ag-header-cell-label": {
                "color": "#007ACC !important",
                "font-weight": "700 !important"
            },
            ".ag-root-wrapper": {
                "width": "100% !important",
                "height": "100% !important",
            },
            ".ag-center-cols-viewport": {
                "overflow-x": "auto !important",
                "overflow-y": "auto !important",
                "min-height": "400px !important"
            },
            ".ag-body-horizontal-scroll-viewport": {
                "overflow-x": "auto !important"
            },
            ".ag-body-viewport": {
                "overflow-y": "auto !important"
            },
        }

        # Configure grid
        grid_options = gb.build()
        grid_options["domLayout"] = "normal"
        grid_options["suppressHorizontalScroll"] = False
        grid_options["suppressVerticalScroll"] = False

        # Display table with scroll and dynamic sorting
        AgGrid(
            grouped_disp,
            gridOptions=grid_options,
            theme="streamlit",
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=False,
            custom_css=custom_css_scroll,
            height=600,
        )

        # Export CSV
        csv = st.session_state.grouped_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="💾 Exportar CSV",
            data=csv,
            file_name=f"agrupacion_{group_col}_por_{val_col}.csv",
            mime="text/csv",
        )

        st.info("ℹ️ **Agrupar Datos:** Agrupa una columna categórica y calcula estadísticas sobre una numérica. Puedes ordenar haciendo clic en los encabezados sin que se cierre la tabla.")


# =========================================================
# 🔍 FILTER DATA
# =========================================================
def filtrar_datos(df: pd.DataFrame):
    """Filter DataFrame rows based on conditions and export filtered CSV."""
    st.subheader("🔍 Filtrar filas")

    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados.")
        return

    # Select column for filtering rows
    col = st.selectbox("Selecciona columna para filtrar filas", df.columns, key="filter_row_col")

    # Filter input based on column type
    if pd.api.types.is_numeric_dtype(df[col]):
        min_val = float(df[col].min())
        max_val = float(df[col].max())
        filtro = st.slider(f"Selecciona rango para {col}", min_value=min_val, max_value=max_val, value=(min_val, max_val))
        df_filtrado = df[(df[col] >= filtro[0]) & (df[col] <= filtro[1])]
    else:
        opciones = df[col].dropna().unique().tolist()
        seleccion = st.multiselect(f"Selecciona valores de {col}", opciones, default=opciones)
        df_filtrado = df[df[col].isin(seleccion)]

    # Save in session
    st.session_state['filas_filtradas'] = df_filtrado

    # Display filtered table
    if 'filas_filtradas' in st.session_state and not st.session_state['filas_filtradas'].empty:
        df_disp = prepare_display_df(st.session_state['filas_filtradas'], max_len=200)
        gb = base_grid_from_df(df_disp)
        for c in df_disp.columns:
            gb.configure_column(c, headerTooltip=f"Columna: {c}")

        custom_css_scroll = {
            ".ag-header-cell-label": {"color": "#007ACC !important", "font-weight": "700 !important"},
            ".ag-root-wrapper": {"width": "100% !important", "height": "100% !important"},
            ".ag-center-cols-viewport": {"overflow-x": "auto !important", "overflow-y": "auto !important", "min-height": "400px !important"},
            ".ag-body-horizontal-scroll-viewport": {"overflow-x": "auto !important"},
            ".ag-body-viewport": {"overflow-y": "auto !important"},
        }

        height_grid = calc_height_for_rows(len(df_disp), row_height=34, header_extra=80, max_height=600)

        AgGrid(
            df_disp,
            gridOptions=gb.build(),
            theme="streamlit",
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=False,
            custom_css=custom_css_scroll,
            height=height_grid,
        )

        # Export filtered CSV
        csv = st.session_state['filas_filtradas'].to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"💾 Exportar CSV filas filtradas ({col})",
            data=csv,
            file_name=f"filas_filtradas_{col}.csv",
            mime="text/csv",
        )

        st.info("ℹ️ **Filtrar filas:** Puedes ordenar columnas haciendo clic en los encabezados sin que se cierre la tabla.")


# =========================================================
# 🗑️ DELETE COLUMN
# =========================================================
def eliminar_columna(df: pd.DataFrame) -> pd.DataFrame:
    """Delete a column from the DataFrame and export CSV of resulting table."""
    st.subheader("🗑️ Eliminar columna")
    
    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados.")
        return df

    col_elim = st.selectbox("Selecciona columna a eliminar", df.columns, key="elim_col")
    df_resultante = df.drop(columns=[col_elim])

    # Display table with scroll and blue headers
    df_disp = prepare_display_df(df_resultante, max_len=200)
    gb = base_grid_from_df(df_disp)
    for c in df_disp.columns:
        gb.configure_column(c, headerTooltip=f"Columna: {c}")

    custom_css_scroll = {
        ".ag-header-cell-label": {"color": "#007ACC !important", "font-weight": "700 !important"},
        ".ag-root-wrapper": {"width": "100% !important", "height": "100% !important"},
        ".ag-center-cols-viewport": {"overflow-x": "auto !important", "overflow-y": "auto !important", "min-height": "400px !important"},
        ".ag-body-horizontal-scroll-viewport": {"overflow-x": "auto !important"},
        ".ag-body-viewport": {"overflow-y": "auto !important"},
    }

    height_grid = calc_height_for_rows(len(df_disp), row_height=34, header_extra=80, max_height=600)

    AgGrid(
        df_disp,
        gridOptions=gb.build(),
        theme="streamlit",
        fit_columns_on_grid_load=False,
        allow_unsafe_jscode=False,
        custom_css=custom_css_scroll,
        height=height_grid,
    )

    # Export CSV
    csv = df_resultante.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"💾 Exportar CSV sin columna ({col_elim})",
        data=csv,
        file_name=f"df_sin_{col_elim}.csv",
        mime="text/csv",
    )

    st.info("ℹ️ **Eliminar columna:** Haz clic en cualquier encabezado para ordenar columnas.")
    return df_resultante

# =========================================================
# 📊 GROUP STATISTICS BY COLUMN
# =========================================================
def estadisticas_por_grupo(df: pd.DataFrame):
    """
    Group statistics by column — stable and optimized version
    - Smooth scroll without gaps
    - 30 visible rows
    - Tooltips on headers
    - Export full CSV
    - No table collapse when sorting
    """
    st.subheader("📊 Estadísticas por grupo")

    if df is None or df.empty:
        st.warning("⚠️ No hay datos cargados para analizar.")
        return

    # Detect categorical and numerical columns
    cat_cols = [c for c in df.columns if df[c].dtype == "object" or df[c].dtype.name == "category"]
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

    if not cat_cols:
        st.info("⚠️ No hay columnas categóricas disponibles para agrupar.")
        return
    if not num_cols:
        st.info("⚠️ No hay columnas numéricas disponibles para calcular estadísticas.")
        return

    # User selects grouping and numerical columns
    group_col = st.selectbox("Columna de agrupación (categórica)", cat_cols, key="group_stats_col")
    stat_col = st.selectbox("Columna numérica (estadística)", num_cols, key="group_stats_num")

    # Session persistence
    if "grouped_stats" not in st.session_state:
        st.session_state.grouped_stats = None

    # Compute grouped statistics
    if st.button("🔹 Calcular estadísticas por grupo", key="btn_group_stats"):
        st.session_state.grouped_stats = df.groupby(group_col)[stat_col].describe().reset_index()

    # Display grouped table if available
    if st.session_state.grouped_stats is not None:
        grouped = st.session_state.grouped_stats.copy()

        # Tooltips for headers
        tooltips = {
            group_col: f"Categoría agrupada ({group_col})",
            "count": "Number of non-null observations",
            "mean": "Average of numeric values",
            "std": "Standard deviation (measure of spread)",
            "min": "Minimum value observed",
            "25%": "First quartile (25th percentile)",
            "50%": "Median (50th percentile)",
            "75%": "Third quartile (75th percentile)",
            "max": "Maximum value observed",
        }

        # Configure AgGrid
        gb = GridOptionsBuilder.from_dataframe(grouped)
        for col in grouped.columns:
            gb.configure_column(
                col,
                headerTooltip=tooltips.get(col, f"Columna: {col}"),
                sortable=True,
                resizable=True,
                wrapText=False,
            )

        gb.configure_default_column(editable=False)
        gb.configure_grid_options(enableBrowserTooltips=True)
        grid_options = gb.build()

        # Determine height (max 30 visible rows)
        max_visible_rows = 30
        total_rows = len(grouped)
        row_height = 30
        base_height = 70  # header + margin
        height = base_height + min(total_rows, max_visible_rows) * row_height

        # Render table with efficient scroll
        AgGrid(
            grouped,
            gridOptions=grid_options,
            height=height,
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=False,
            theme="streamlit",
            enable_enterprise_modules=False,
        )

        # Export full CSV
        csv = grouped.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="💾 Exportar CSV completo (estadísticas por grupo)",
            data=csv,
            file_name=f"estadisticas_por_grupo_{group_col}_por_{stat_col}.csv",
            mime="text/csv",
            help="Descarga la tabla completa con todas las estadísticas calculadas.",
        )

        st.info(
            "ℹ️ **Consejo:** pasa el ratón sobre los encabezados para ver su explicación. "
            "Puedes ordenar y desplazarte sin perder la tabla."
        )