import streamlit as st
from pathlib import Path
import os
import sys
import webbrowser
import threading
import streamlit.web.cli as stcli

# ===== 🧠 CONFIGURATION FOR EXECUTION FROM .EXE =====
def run_streamlit():
    sys.argv = [
        "streamlit",
        "run",
        os.path.abspath(__file__),
        "--server.port=8501",
        "--browser.serverAddress=localhost",
        "--server.headless=true"
    ]
    stcli.main()

if __name__ == "__main__":
    # If the program is executed from an .exe, automatically open the browser
    if getattr(sys, "frozen", False):
        threading.Thread(target=lambda: webbrowser.open("http://localhost:8501")).start()
        run_streamlit()
        sys.exit()

# ===== 🧠 GENERAL CONFIGURATION =====
st.set_page_config(
    page_title="Analizador Big Data AEMG",
    page_icon="assets/logo_favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== 🎨 GLOBAL STYLE =====
st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.block-container {padding-top:0 !important; padding-bottom:0 !important;}
.main-title {display:flex; align-items:center; justify-content:center; background-color:#e6f0fa;
             padding:0.6rem; border-radius:10px; margin-bottom:0.8rem; box-shadow:0 2px 6px rgba(0,0,0,0.1);}
.main-title h1 {color:#007ACC; font-size:38px; font-weight:800; margin:0; padding:0;}
section[data-testid="stSidebar"] {background-color:#f2f6fc !important; padding-top:0 !important; margin-top:-3rem !important;}
div[data-testid="stSidebarContent"] {padding-top:0 !important; margin-top:-2rem !important;}
[data-testid="stSidebar"] img {margin-top:0 !important; margin-bottom:0.5rem !important; display:block; margin-left:auto; margin-right:auto;}
.stSelectbox label {font-size:18px !important; font-weight:600 !important; color:#007ACC !important; margin-bottom:0.3rem !important;}
div[data-baseweb="select"] {font-size:16px !important;}
.blue-header {color:#007ACC !important; font-weight:bold !important;}
h2,h3,h4 {color:#007ACC !important; font-weight:700 !important; margin-top:0.2rem !important; margin-bottom:0.2rem !important;}

/* ===== 🔧 WIDEN SIDEBAR ===== */
[data-testid="stSidebar"] {
    width: 340px !important;      /* desired width */
    min-width: 340px !important;
}
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stExpander,
[data-testid="stSidebar"] .stButton {
    width: 100% !important;
}
[data-testid="stSidebarContent"] {
    padding-right: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ===== 🖼️ TITLE =====
st.markdown('<div class="main-title"><h1>📊 Analizador Big Data AEMG</h1></div>', unsafe_allow_html=True)
st.markdown("---")

# ===== 🖼️ LOGO =====
logo_path = Path("assets/logo.png")
# Display logo if it exists, otherwise show a warning
if logo_path.exists():
    st.sidebar.image(str(logo_path), width=150)
else:
    st.sidebar.warning("⚠️ Logo no encontrado en assets/logo.png")

# ===== 📋 ORDERED MENU =====
menu = st.sidebar.selectbox("📂 Menú de opciones", [
    "Inicio",
    "Cargar archivo",
    "Cargar desde SQL",
    "Mostrar información general",
    "Mostrar los datos de una columna",
    "Ordenar datos",
    "Eliminar columna",
    "Eliminar duplicados",
    "Eliminar filas con valores nulos",
    "Agrupar por columna",
    "Reemplazar valores en columna",
    "Buscar texto parcial en columna",
    "Crear columna combinada",
    "Graficar histograma",
    "Graficar gráfico de barras",
    "Estadísticas por grupo"
])

# ===== 📂 IMPORT FUNCTIONS =====
from funciones.carga import cargar_archivo
from funciones.analisis import mostrar_info, mostrar_columna, ordenar_datos, agrupar_datos, filtrar_datos, estadisticas_por_grupo
from funciones.transformaciones import eliminar_columna, reemplazar_valor, eliminar_duplicados, buscar_texto, crear_columna_combinada, eliminar_nulos
from funciones.graficos import graficar_histograma, graficar_barras
from funciones.sql import cargar_desde_sql

# ===== 🧠 GLOBAL VARIABLE =====
# Initialize dataframe in session state if not already set
if "df" not in st.session_state:
    st.session_state.df = None

# ===== ✅ AUXILIARY FUNCTIONS =====
def necesita_df():
    # Check if a dataframe is loaded
    if st.session_state.df is None:
        st.warning("⚠️ Carga un archivo primero.")
        return False
    return True

# ===== 🔄 MAIN FUNCTIONALITY =====
if menu == "Inicio":
    st.info("👋 Bienvenido al Analizador Big Data AEMG. Usa el menú lateral para comenzar.")

elif menu == "Cargar archivo":
    archivo = st.file_uploader("📂 Sube aquí tu base de datos (.csv, .json, .xlsx)", type=["csv","json","xlsx"])
    if archivo:
        # Load file into dataframe
        df = cargar_archivo(archivo)
        if df is not None:
            st.session_state.df = df
            st.success(f"✅ Archivo **{archivo.name}** cargado: {df.shape[0]} filas x {df.shape[1]} columnas")
        else:
            st.error("❌ Error al cargar archivo.")

elif menu == "Cargar desde SQL":
    # Load dataframe from SQL database
    df = cargar_desde_sql()
    if df is not None:
        st.session_state.df = df
        st.success("✅ Datos cargados desde SQL.")
    else:
        st.warning("⚠️ No se pudieron cargar datos desde SQL.")

elif menu == "Mostrar información general":
    if necesita_df(): mostrar_info(st.session_state.df)

elif menu == "Mostrar los datos de una columna":
    if necesita_df(): mostrar_columna(st.session_state.df)

elif menu == "Ordenar datos":
    if necesita_df(): st.session_state.df = ordenar_datos(st.session_state.df)

elif menu == "Eliminar columna":
    if necesita_df(): st.session_state.df = eliminar_columna(st.session_state.df)

elif menu == "Eliminar duplicados":
    if necesita_df(): st.session_state.df = eliminar_duplicados(st.session_state.df)

elif menu == "Eliminar filas con valores nulos":
    if necesita_df(): st.session_state.df = eliminar_nulos(st.session_state.df)

elif menu == "Agrupar por columna":
    if necesita_df(): agrupar_datos(st.session_state.df)

elif menu == "Reemplazar valores en columna":
    if necesita_df(): st.session_state.df = reemplazar_valor(st.session_state.df)

elif menu == "Buscar texto parcial en columna":
    if necesita_df(): buscar_texto(st.session_state.df)

elif menu == "Crear columna combinada":
    if necesita_df(): st.session_state.df = crear_columna_combinada(st.session_state.df)

elif menu == "Graficar histograma":
    if necesita_df(): graficar_histograma(st.session_state.df)

elif menu == "Graficar gráfico de barras":
    if necesita_df(): graficar_barras(st.session_state.df)

elif menu == "Estadísticas por grupo":
    if necesita_df(): estadisticas_por_grupo(st.session_state.df)
