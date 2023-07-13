import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from google.cloud import storage
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

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
    df['time'] = df['time'].apply(lambda x: datetime.fromtimestamp(int(x) / 1000).strftime('%Y-%m-%d'))
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""Arreglamos profundidades negativas"""

# Por valor absoluto
def replace_negative_with_absolute(df):
    df['depth'] = df['depth'].fillna(0).abs()
    df['mag'] = df['mag'].fillna(1).abs()
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

"""Crear columna pais a partir de columna place"""
def process_place_data(df):
    
    df['country'] = df['place'].str.split(',', n=1).str[-1].str.strip().str.lower()
    df['country'] = df['country'].fillna(df['place'])  
    
    # usa_cities = ["alabama", "california-nevada border region", '"sandywoods township, missouri"', 'the 1906 san francisco earthquake' "al", "alaska", "ak", "arizona", "az", "arkansas", "ar", "california", "ca", "colorado", "co", "connecticut", "ct", "delaware", "de", "florida", "fl", "georgia", "ga", "hawaii", "hi", "idaho", "id", "illinois", "il", "indiana", "in", "iowa", "ia", "kansas", "ks", "kentucky", "ky", "louisiana", "la", "maine", "me", "maryland", "md", "massachusetts", "ma", "michigan", "mi", "minnesota", "mn", "mississippi", "ms", "missouri", "mo", "montana", "mt", "nebraska", "ne", "nevada", "nv", "new hampshire", "nh", "new jersey", "nj", "new mexico", "nm", "new york", "ny", "north carolina", "nc", "north dakota", "nd", "ohio", "oh", "oklahoma", "ok", "oregon", "or", "pennsylvania", "pa", "rhode island", "ri", "south carolina", "sc", "south dakota", "sd", "tennessee", "tn", "texas", "tx", "utah", "ut", "vermont", "vt", "virginia", "va", "washington", "wa", "west virginia", "wv", "wisconsin", "wi", "wyoming", "wy"]   
    # df['country'] = df['country'].map(lambda x: 'united states' if x in usa_cities else x)
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def fill_missing_with_median(df, columns):
    """
    Fill missing values in specified columns with the median of each column.
    Optimized to calculate median and transform data type to float.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        columns (list): List of column names to fill with the median.

    Returns:
        pandas.DataFrame: The DataFrame with missing values filled by the median.
    """
    for column in columns:
        df[column] = df[column].fillna(df[column].median()).astype(float)

    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def fill_missing_with_text(df):
    columns = ['place',	'earthquakeType', 'country']
    df[columns] = df[columns].astype(str)
    for column in columns:
        df[column] = df[column].fillna('null')
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def tsunamis(df):
    columns = ['tsunami']
    
    for column in columns:                  # Verificar si las columnas existen en el DataFrame
        if column not in df.columns:
            df[column] = 0
    
    df[columns] = df[columns].astype(bool).astype(int)
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_id_column(df):
    """
    Create an 'id_e' column in the DataFrame by concatenating specified columns.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        pandas.DataFrame: The DataFrame with an additional 'id_e' column.
    """
    columns_to_join = ['time', 'place', 'earthquakeType', 'mag', 'longitude', 'latitude']
    df['id_e'] = df[columns_to_join].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
    df['id_e'] = df['id_e'].astype(str)
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def create_dataset():

    client = bigquery.Client()                                                      # Create a Google Cloud Storage client 
    table_ref = 'terra-safe-391718.AIRFLOW.USGS_JPN'                                # Specify your BigQuery table ID

    try:
        client.get_table(table_ref)                                                 # Check if the table exists
    except NotFound:                                                                # Table doesn't exist, create it and assign last_row = 1900
        schema = []                                                               # Empty schema field list
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        last_row = {'max_year': 1906}
    else:                                                                           # Table exists, execute the query to get the last_row
        query = f"""
        SELECT EXTRACT(YEAR FROM time) AS max_year
        FROM `{table_ref}`
        ORDER BY time DESC
        LIMIT 1
        """
        query_job = client.query(query)
        result = query_job.result()

        for row in result:
            last_row = row

    start_year = int(last_row['max_year'])
    end_year = datetime.now().year

    for year in range(start_year, end_year+1):
        for month in range(1, 13):

            url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={year}-{month}-01&endtime={year}-{month}-31&minlatitude=24.396308&maxlatitude=45.551483&minlongitude=122.934570&maxlongitude=154.003906'
            print(url)
            df = pd.DataFrame()

            data = []
            with requests.Session() as s:
                response = requests.get(url)

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
                        tsunami = properties["tsunami"]
                        sig = properties["sig"]
                        coordinates = geometry["coordinates"]
                        
                        records.append((time, mag, cdi, mmi, dmin, place, earthquakeType, coordinates, sig, tsunami)) # Agregar los valores individuales a la lista de registros

                    df = pd.DataFrame(records, columns=["time", "mag", "cdi", "mmi", "dmin", "place", "earthquakeType", "coordinates", "sig", "tsunami"])

                    df = change_time_format(df)
                    df = multiply_dmin(df)
                    df = separar_coordenadas(df)
                    df = replace_negative_with_absolute(df)
                    df = process_place_data(df)
                    df = tsunamis(df)
                    columns = ['mag', 'cdi', 'mmi', 'dmin', 'sig', 'depth']
                    df = fill_missing_with_median(df, columns)
                    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d')
                    df = fill_missing_with_text(df)
                    df = create_id_column(df)
                    
                    job_config = bigquery.LoadJobConfig()
                    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
                    job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
                    client.load_table_from_dataframe(df, table_ref, job_config=job_config).result()
                except json.decoder.JSONDecodeError:
                    print(f"Error en: {year}-{month}")

    client = bigquery.Client()
    deduplication_query = f"""
    DELETE FROM {table_ref}
    WHERE id_e IN (
        SELECT id_e
        FROM (
            SELECT id_e, COUNT(*) as count
            FROM {table_ref}
            GROUP BY id_e
        ) t
        WHERE count > 1
    );
    """
    
    # Execute the deduplication query
    query_job = client.query(deduplication_query)
    query_job.result()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

default_args = {
    'start_date': airflow.utils.dates.days_ago(0),
}

with DAG(
    'DAG_USGS_JPN',
    default_args=default_args,
    schedule_interval = '0 0 * * 0',
    catchup = False,
) as usgs_dag:

    etl_usgs = PythonOperator(
        task_id = "DAG_USGS_JPN",
        python_callable = create_dataset
    )

    etl_usgs