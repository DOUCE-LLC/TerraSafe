import pandas as pd
from datetime import datetime
import requests
# from geopy.geocoders import Nominatim
import json
from google.cloud import storage
from datetime import datetime

api_key = "5e97aa77f5324945a2863959710ee2ad"

"""Funcion para eliminar columnas"""
def remove_column(df, column_name):
    df.drop(column_name, axis=1, inplace=True)
    return df

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

def change_time_format(df):
    df['time'] = df['time'].astype(str).apply(lambda x: datetime.fromtimestamp(int(x) / 1000).strftime('%Y-%m-%d'))
    return df

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

"""Arreglamos profundidades negativas"""

# Por valor absoluto
def replace_negative_with_absolute(df):
    df['depth'] = df['depth'].abs()
    df['mag'] = df['mag'].abs()
    return df

# Por otro valor
def replace_negative_with_one(df):
    df.loc[df['depth'] < 0, 'depth'] = 1
    return df

"""Rellenamos nulos con mediana"""
def replace_null_with_median(df):
    median = df['mag'].median()
    df['mag'].fillna(median, inplace=True)
    return df

"""Conversion de grados a km en dmin"""
def multiply_dmin(df):
    df['dmin'] = df['dmin'] * 111.2
    return df

"""Rellenamos nulos con mediana"""
def replace_null_with_median_dmin(df):
    median = df['dmin'].median()
    df['dmin'].fillna(median, inplace=True)
    return df

"""Dejamos solo tipo terremoto y eliminamos la columna type"""
def filter_records_by_type(df):
    df = df[df['earthquakeType'] == 'earthquake']
    return df

# def obtener_pais_desde_place(df):
#     df['country'] = df['place'].str.split(',').str[-1].str.strip()
#     return df

"""Crear columna pais a partir de columna place"""
def process_place_data(df):
    
    df['Country'] = df['place'].str.split(',', n=1).str[-1].str.strip().str.lower()
    df['Country'] = df['Country'].fillna(df['place'])  
    
    #usa_cities = ["california", "ca", "alaska", "ak", "hawaii", "hi", "washington", "wa", "oregon", "or", "nevada", "nv", "idaho", "id"]

    usa_cities = [
    "alabama", "al",
    "alaska", "ak",
    "arizona", "az",
    "arkansas", "ar",
    "california", "ca",
    "colorado", "co",
    "connecticut", "ct",
    "delaware", "de",
    "florida", "fl",
    "georgia", "ga",
    "hawaii", "hi",
    "idaho", "id",
    "illinois", "il",
    "indiana", "in",
    "iowa", "ia",
    "kansas", "ks",
    "kentucky", "ky",
    "louisiana", "la",
    "maine", "me",
    "maryland", "md",
    "massachusetts", "ma",
    "michigan", "mi",
    "minnesota", "mn",
    "mississippi", "ms",
    "missouri", "mo",
    "montana", "mt",
    "nebraska", "ne",
    "nevada", "nv",
    "new hampshire", "nh",
    "new jersey", "nj",
    "new mexico", "nm",
    "new york", "ny",
    "north carolina", "nc",
    "north dakota", "nd",
    "ohio", "oh",
    "oklahoma", "ok",
    "oregon", "or",
    "pennsylvania", "pa",
    "rhode island", "ri",
    "south carolina", "sc",
    "south dakota", "sd",
    "tennessee", "tn",
    "texas", "tx",
    "utah", "ut",
    "vermont", "vt",
    "virginia", "va",
    "washington", "wa",
    "west virginia", "wv",
    "wisconsin", "wi",
    "wyoming", "wy"
]   
    df['Country'] = df['Country'].map(lambda x: 'United States' if x in usa_cities else x)
    return df


#####################################################################################################


def create_dataset(start_year, end_year):

    df1 = pd.DataFrame()

    for year in range(start_year, end_year+1):
        for month in range(1, 3):
            for day in range(1, 32):
                df = pd.DataFrame()
                url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

                # Parámetros para la solicitud de datos
                params = {
                    "format": "geojson",
                    "starttime": f"{year}-{month}-{day-1}",
                    "endtime": f"{year}-{month}-{day}"
                }

                data = []
                with requests.Session() as s:
                    response = requests.get(url, params=params)

                    try:
                        data = response.json()
                        records = [] # Crear una lista para almacenar los registros en el formato adecuado
                        
                        for feature in data["features"]: # Iterar sobre todos los elementos (características) en los datos

                            properties = feature["properties"] # Obtener las propiedades de cada terremoto
                            geometry = feature["geometry"]     # Obtener la geometría de cada terremoto

                            # Extraer los valores individuales...
                            time = properties["time"]
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

                        df = pd.DataFrame(records, columns=["time", "mag", "cdi", "mmi", "dmin", "place", "earthquakeType", "coordinates", "alert", "sig", "tsunami"])

                        df = change_time_format(df)
                        df = replace_null_with_median(df)
                        df = multiply_dmin(df)
                        df = replace_null_with_median_dmin(df)
                        df = separar_coordenadas(df)
                        df = replace_negative_with_absolute(df)
                        # df = obtener_pais_desde_place(df)
                        df = process_place_data(df)

                        df.sort_values(by=['time'], ascending=True, inplace=True)
                        df1 = pd.concat([df1, df]).drop_duplicates().reset_index(drop=True)
                        print(f"{year}, {month}, {day}")
                    except json.decoder.JSONDecodeError:
                        print(f"No se encontraron datos para el período de tiempo especificado: {year}, {month}, {day}")

    # df1.to_csv(f"../../Data/Cleaned data/USGS.csv", index=False)

    # Define the bucket name and filename in the bucket
    bucket_name = "terrasafe"
    filename = "USGS.csv"

    # Convert DataFrame to CSV and store it in a string buffer
    csv_buffer = pd.DataFrame.to_csv(df1, index=False)

    # Specify the bucket and file path in Cloud Storage
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(filename)

    # Upload the CSV data to the Cloud Storage bucket
    blob.upload_from_string(csv_buffer, content_type="text/csv")

current_year = datetime.now().year
create_dataset(0, current_year)