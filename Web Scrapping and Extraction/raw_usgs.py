# https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=1930-01-01&endtime=1930-12-31
# si lo abris te descarga el csv.

# https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=1930-01-01&endtime=1930-12-31
# visualizar la api

import pandas as pd
import requests
import os

for year in range(2023, 2024):
    df1 = pd.DataFrame()

    for month in range(1, 13):
        # Crear la URL para el mes actual
        url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={year}-{month}-01&endtime={year}-{month}-31"

        # Descargar el archivo CSV
        response = requests.get(url)
        file_name = f"USGS_{year}_{month}.csv"

        with open(file_name, 'wb') as file:
            file.write(response.content)

        # Verificar si las columnas requeridas están presentes en el archivo CSV
        # required_columns = ['time', 'latitude', 'longitude', 'depth', 'mag', 'dmin', 'id', 'place', 'type']
        available_columns = pd.read_csv(file_name, nrows=0).columns.tolist()

        # if set(required_columns).issubset(available_columns):
        if available_columns:
            # Leer el archivo CSV y seleccionar las columnas requeridas
            df2 = pd.read_csv(file_name)

            # Ordenar df2 de forma ascendente
            df2.sort_values(by=['time'], ascending=True, inplace=True)

            # Concatenar el nuevo DataFrame con el anterior y eliminar duplicados
            df1 = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
        else:
            print(f'{file_name} have some problems...')

        # Eliminar el archivo CSV
        os.remove(file_name)

    # Guardar el DataFrame final en un archivo CSV
    output_file = f'../Data/Raw data/Raw_USGS_{year}.csv'
    df1.to_csv(output_file, index=False)
