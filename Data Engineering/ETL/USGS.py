
import pandas as pd
from datetime import datetime
import requests
from geopy.geocoders import Nominatim

df = pd.read_csv('../Data/Raw data/USGS_2000.csv')

df.info()

df.head(1)

df.describe()

"""Funcion para eliminar columnas"""
def remove_column(df, column_name):
    df.drop(column_name, axis=1, inplace=True)
    return df

"""Cambiamos el formato de la columna time, a YYYY-MM-DD"""
def change_time_format(df):
    df['time'] = df['time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d'))
    return df

df = change_time_format(df)

"""Crear columna pais con API"""
def obtener_pais(latitud, longitud, api_key):
    url = f"https://api.opencagedata.com/geocode/v1/json?key={api_key}&q={latitud}+{longitud}&pretty=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data["results"]) > 0:
            components = data["results"][0]["components"]
            pais = components.get("country") or components.get("country_code")
            return pais
        else:
            return "No se encontró ningún resultado para las coordenadas proporcionadas."
    else:
        return "Error al realizar la solicitud a la API."

def agregar_pais(df, api_key):
    df["country"] = df.apply(lambda row: obtener_pais(row["latitude"], row["longitude"], api_key), axis=1)
    return df

api_key = "5e97aa77f5324945a2863959710ee2ad"

df = agregar_pais(df, api_key)

"""Crear columna pais con libreria"""
def obtener_pais(latitud, longitud):
    geolocator = Nominatim(user_agent="mi_aplicacion")
    location = geolocator.reverse((latitud, longitud), exactly_one=True)
    if location is not None:
        pais = location.raw['address'].get('country')
        return pais
    else:
        return "No se encontró ningún resultado para las coordenadas proporcionadas."

def agregar_pais_al_dataframe(df):
    df['country'] = df.apply(lambda row: obtener_pais(row['latitude'], row['longitude']), axis=1)
    return df

df = agregar_pais_al_dataframe(df)

""" Eliminamos latitud y longitud"""
df = remove_column(df, 'latitude')
df = remove_column(df, 'longitude')

"""Arreglamos profundidades negativas"""
# Por valor absoluto
def replace_negative_with_absolute(df):
    df['depth'] = df['depth'].abs()
    return df

df = replace_negative_with_absolute(df)

# Por otro valor
def replace_negative_with_one(df):
    df.loc[df['depth'] < 0, 'depth'] = 1
    return df

df_modified = replace_negative_with_one(df)

"""Rellenamos nulos con mediana"""

def replace_null_with_median(df):
    median = df['mag'].median()
    df['mag'].fillna(median, inplace=True)
    return df

df = replace_null_with_median(df)

"""Conversion de grados a km en dmin"""

def multiply_dmin(df):
    df['dmin'] = df['dmin'] * 111.2
    return df

df = multiply_dmin(df)

"""Rellenamos nulos con mediana"""
def replace_null_with_median_dmin(df):
    median = df['dmin'].median()
    df['dmin'].fillna(median, inplace=True)
    return df

df = replace_null_with_median_dmin(df)

"""Dejamos solo tipo terremoto y eliminamos la columna type"""
def filter_records_by_type(df):
    df = df[df['type'] == 'earthquake']
    return df

df = filter_records_by_type(df)

df = remove_column(df, 'type')

"""Eliminamos id"""
df = remove_column(df, 'id')

#####################################################################################################
def create_dataset(start_year, end_year):
    # URL de la API de terremotos del USGS
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    # Parámetros para la solicitud de datos
    params = {
        "format": "geojson",
        "starttime": f"{start_year}-01-01",
        "endtime": f"{end_year}-01-02",
        "limit": 20000  # Cambiar el valor de limit a un número suficientemente grande
    }

    try:
        # Realizar la solicitud GET a la API con los parámetros especificados
        response = requests.get(url, params=params)
        # Comprobar si hay errores en la respuesta
        response.raise_for_status()

        # Obtener los datos en formato JSON de la respuesta
        data = response.json()
        # Lista para almacenar los registros de propiedades de los terremotos
        records = []

        # Iterar sobre todos los elementos (características) en los datos
        for feature in data["features"]:
            # Obtener las propiedades de cada terremoto
            properties = feature["properties"]
            # Agregar las propiedades a la lista de registros
            records.append(properties)

        # Crear un DataFrame de pandas a partir de los registros de propiedades
        df = pd.DataFrame(records)
        return df

    except requests.exceptions.HTTPError as err:
        # Manejar un error HTTP que ocurra durante la solicitud
        print(f"Ocurrió un error HTTP: {err}")
    except requests.exceptions.RequestException as err:
        # Manejar cualquier otro error de solicitud
        print(f"Ocurrió un error durante la solicitud: {err}")
    except ValueError as err:
        # Manejar un error al analizar la respuesta JSON
        print(f"Error al analizar la respuesta JSON: {err}")

    return None

# Ejemplo de uso
start_year = "2014"
end_year = "2014"
# Crear el conjunto de datos llamando a la función create_dataset
dataset = create_dataset(start_year, end_year)

# Verificar si el conjunto de datos no es None
if dataset is not None:
    # Imprimir el conjunto de datos completo
    print(dataset)