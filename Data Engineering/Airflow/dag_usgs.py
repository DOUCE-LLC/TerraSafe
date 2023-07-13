import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from google.cloud import storage

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import json
import requests
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import io
from io import BytesIO


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""Funcion para eliminar columnas"""
def remove_column(df, column_name):
    df.drop(column_name, axis=1, inplace=True)
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def separar_coordenadas(df):
    # Obtener los valores de la columna "coordinates" como una lista de listas
    coordinates = df['coordinates'].tolist()
    remove_column(df, 'coordinates')

    # Extraer los valores de longitud, latitud y profundidad en listas separadas
    longitude = [coord[0] for coord in coordinates]
    latitude = [coord[1] for coord in coordinates]
    depth = [coord[2] for coord in coordinates]

    # Agregar las nuevas columnas al DataFrame existente
    df['longitude'] = longitude
    df['latitude'] = latitude
    df['depth'] = depth

    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def change_time_format(df):
    df['time'] = df['time'].astype(str).apply(lambda x: datetime.fromtimestamp(int(x) / 1000).strftime('%Y-%m-%d'))
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Crear columna pais con API"""
# def obtener_pais(latitud, longitud, api_key):
#     url = f"https://api.opencagedata.com/geocode/v1/json?key={api_key}&q={latitud}+{longitud}&pretty=1"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         if len(data["results"]) > 0:
#             components = data["results"][0]["components"]
#             pais = components.get("country") or components.get("country_code")
#             return pais
#         else:
#             return "No se encontró ningún resultado para las coordenadas proporcionadas."
#     else:
#         return "Error al realizar la solicitud a la API."
# def agregar_pais(df, api_key):
#     df["country"] = df.apply(lambda row: obtener_pais(row["latitude"], row["longitude"]), axis=1)
#     return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Crear columna pais con libreria"""
# def obtener_pais(latitud, longitud):
#     geolocator = Nominatim(user_agent="mi_aplicacion")
#     location = geolocator.reverse((latitud, longitud), exactly_one=True)
#     if location is not None:
#         pais = location.raw['address'].get('country')
#         return pais
#     else:
#         return "No se encontró ningún resultado para las coordenadas proporcionadas."
# def agregar_pais_al_dataframe(df):
#     df['country'] = df.apply(lambda row: obtener_pais(row['latitude'], row['longitude']), axis=1)
#     return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Arreglamos profundidades negativas"""

# Por valor absoluto
def replace_negative_with_absolute(df):
    df['depth'] = df['depth'].fillna(0).abs()
    df['mag'] = df['mag'].abs()
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Por otro valor
def replace_negative_with_one(df):
    df.loc[df['depth'] < 0, 'depth'] = 1
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Rellenamos nulos con mediana"""
def replace_null_with_median(df):
    median = df['mag'].median()
    df['mag'].fillna(median, inplace=True)
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Conversion de grados a km en dmin"""
def multiply_dmin(df):
    df['dmin'] = df['dmin'] * 111.2
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Rellenamos nulos con mediana"""
def replace_null_with_median_dmin(df):
    median = df['dmin'].median()
    df['dmin'].fillna(median, inplace=True)
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Dejamos solo tipo terremoto y eliminamos la columna type"""
def filter_records_by_type(df):
    df = df[df['earthquakeType'] == 'earthquake']
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# def obtener_pais_desde_place(df):
#     df['country'] = df['place'].str.split(',').str[-1].str.strip()
#     return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Crear columna pais a partir de columna place"""
def process_place_data(df):
    
    df['Country'] = df['place'].str.split(',', n=1).str[-1].str.strip().str.lower()
    df['Country'] = df['Country'].fillna(df['place'])  
    
    usa_cities = ["alabama", "al", "alaska", "ak", "arizona", "az", "arkansas", "ar", "california", "ca", "colorado", "co", "connecticut", "ct", "delaware", "de", "florida", "fl", "georgia", "ga", "hawaii", "hi", "idaho", "id", "illinois", "il", "indiana", "in", "iowa", "ia", "kansas", "ks", "kentucky", "ky", "louisiana", "la", "maine", "me", "maryland", "md", "massachusetts", "ma", "michigan", "mi", "minnesota", "mn", "mississippi", "ms", "missouri", "mo", "montana", "mt", "nebraska", "ne", "nevada", "nv", "new hampshire", "nh", "new jersey", "nj", "new mexico", "nm", "new york", "ny", "north carolina", "nc", "north dakota", "nd", "ohio", "oh", "oklahoma", "ok", "oregon", "or", "pennsylvania", "pa", "rhode island", "ri", "south carolina", "sc", "south dakota", "sd", "tennessee", "tn", "texas", "tx", "utah", "ut", "vermont", "vt", "virginia", "va", "washington", "wa", "west virginia", "wv", "wisconsin", "wi", "wyoming", "wy"]   
    df['Country'] = df['Country'].map(lambda x: 'united states' if x in usa_cities else x)
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def deleteExistingFile(bucket_name, file_name):
    client = storage.Client()                   # Create a client for Cloud Storage
    bucket = client.get_bucket(bucket_name)     # Get the bucket

    blob = bucket.blob(file_name)                # Check if the file exists
    if blob.exists():
        blob.delete()                           # Delete the file

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_dataset():

    bucket_name = 'terrasafe'
    file_name = 'DAG_USGS.csv'
    usgs_date = 'last_usgs_date.csv'

    deleteExistingFile(bucket_name, usgs_date)

    storage_client = storage.Client()                                               # Create a Google Cloud Storage client
    bucket = storage_client.get_bucket(bucket_name)                                 # Get the specified bucket
    blob = bucket.blob(file_name)                                                   # Get the blob (file) from the bucket
    data = blob.download_as_string()                                                # Download the file content as a string
    df1 = pd.read_csv(io.BytesIO(data), encoding='utf-8')                           # Read the old CSV data into a pandas DataFrame
    last_row = str(df1['time'].tail(1).values[0])[:4]                               # Extract the last row's 'date' column value and keep only the first 4 characters
    bucket.blob(usgs_date).upload_from_string(last_row, content_type='text/csv')    # Save the file last_noaa_date.csv to Cloud Storage

    if last_row == '':
        last_row = 1900

    start_year = int(last_row)
    end_year = datetime.now().year

    df2 = pd.DataFrame()                                                            # Dataframe of the new data from the API

    for year in range(start_year, end_year+1):
        for month in range(1, 13):
            df3 = pd.DataFrame()
            url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

            params = {                                                              # Parámetros para la solicitud de datos
                "format": "geojson",
                "starttime": f"{year}-{month}-01",
                "endtime": f"{year}-{month}-31"
            }

            data = []
            with requests.Session() as s:
                response = requests.get(url, params=params)

                try:
                    data = response.json()
                    records = []                                                   # Crear una lista para almacenar los registros en el formato adecuado
                    
                    for feature in data["features"]:                               # Iterar sobre todos los elementos (características) en los datos

                        properties = feature["properties"]                         # Obtener las propiedades de cada terremoto
                        geometry = feature["geometry"]                             # Obtener la geometría de cada terremoto

                        time = properties["time"]                                  # Extraer los valores individuales...
                        mag = properties["mag"]
                        cdi = properties["cdi"]
                        mmi = properties["mmi"]
                        place = properties["place"]
                        dmin = properties["dmin"]
                        earthquakeType = properties["type"]
                        alert = properties["alert"]
                        tsunami = properties["tsunami"]
                        sig = properties["sig"]
                        coordinates = geometry["coordinates"]
                        
                        records.append((time, mag, cdi, mmi, dmin, place, earthquakeType, coordinates, alert, sig, tsunami)) # Agregar los valores individuales a la lista de registros

                    df3 = pd.DataFrame(records, columns=["time", "mag", "cdi", "mmi", "dmin", "place", "earthquakeType", "coordinates", "alert", "sig", "tsunami"])

                    df3 = change_time_format(df3)
                    df3 = replace_null_with_median(df3)
                    df3 = multiply_dmin(df3)
                    df3 = replace_null_with_median_dmin(df3)
                    df3 = separar_coordenadas(df3)
                    df3 = replace_negative_with_absolute(df3)
                    df3 = process_place_data(df3)

                    df2 = pd.concat([df2, df3]).drop_duplicates().reset_index(drop=True)
                except json.decoder.JSONDecodeError:
                    print(f"Error en: {year}-{month}")

    df1 = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
    df1.sort_values(by=['time'], ascending=True, inplace=True)

    client = storage.Client()                                                   # Create a client for Cloud Storage
    deleteExistingFile(bucket_name, file_name)                                  # Delete the existing file
    csv_buffer = pd.DataFrame.to_csv(df1, index=False)                          # Convert DataFrame to CSV and store it in a string buffer
    bucket = client.get_bucket(bucket_name)                                     # Specify the bucket in Cloud Storage
    blob = bucket.blob(file_name)                                               # Specify the file in Cloud Storage
    blob.upload_from_string(csv_buffer, content_type="text/csv")                # Upload the CSV data to the Cloud Storage bucket


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

default_args = {
    'start_date': airflow.utils.dates.days_ago(0),
}

with DAG(
    'usgs_dag',
    default_args=default_args,
    schedule_interval = '0 0 * * 0',
    catchup = False,
) as usgs_dag:

    etl_usgs = PythonOperator(
        task_id = "usgs_dag",
        python_callable = create_dataset
    )

    etl_usgs