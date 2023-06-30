import ydata_profiling as ydata
import pandas as pd
import os

# Ruta de la carpeta con los archivos CSV
carpeta_datos = '../Data/Raw data/'

# Obtener la lista de archivos CSV en la carpeta
archivos_csv = [archivo for archivo in os.listdir(carpeta_datos) if archivo.endswith('.csv')]

# Iterar sobre cada archivo CSV
for archivo in archivos_csv:
    ruta_archivo = os.path.join(carpeta_datos, archivo)
    
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv(ruta_archivo)
    
    # Generar el informe de perfil de datos
    profile = ydata.ProfileReport(df)
    
    # Generar el nombre de archivo para el informe HTML
    nombre_informe = archivo.replace('.csv', '.html')
    
    # Guardar el informe como HTML
    ruta_informe = os.path.join('./routes/', nombre_informe)
    profile.to_file(ruta_informe)
