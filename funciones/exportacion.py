from datetime import datetime

def exportar_datos(df):
    """
    Exporta el DataFrame a CSV o XLSX con nombre y timestamp.
    """
    formato = input("¿En qué formato deseas exportar? (csv/xlsx): ").lower()
    salida = input("Introduce el nombre base del archivo de salida (sin extensión): ")
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_final = f"{salida}_{timestamp}"
    
    pdf = df.toPandas()
    
    if formato == "csv":
        pdf.to_csv(f"{nombre_final}.csv", index=False)
        print(f"✅ Datos exportados a {nombre_final}.csv")
    elif formato == "xlsx":
        pdf.to_excel(f"{nombre_final}.xlsx", index=False)
        print(f"✅ Datos exportados a {nombre_final}.xlsx")
    else:
        print("⚠️ Formato no soportado. Usa 'csv' o 'xlsx'.")
