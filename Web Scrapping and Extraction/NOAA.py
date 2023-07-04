import argparse
import json
import requests
import time as clock
import pandas as pd

def get_earthquakes(min_year, max_year, min_eq_magnitude):
    """Return information about all earthquakes occurring between min_year and max_year and greater than
    min_eq_magnitude. Consult the API docs at https://www.ngdc.noaa.gov/hazel/view/swagger for details.

    Args:
      min_year (int): minimum year of earthquake query
      max_year (int): maximum year of earthquake query
      min_eq_magnitude (float): minimum earthquake magnitude of query

    Returns:
      dict containing query results [JSON]
    """
    # Define components of Hazard Event Lookup (HazEL) query:
    protocol = "https://"
    host = "www.ngdc.noaa.gov"
    service = "/hazel/hazard-service/api/v1/earthquakes"
    # Consult the API docs at https://www.ngdc.noaa.gov/hazel/view/swagger for different "service" endpoints.

    payload = {
        'minYear': str(min_year),
        'maxYear': str(max_year),
        'minEqMagnitude': str(min_eq_magnitude)
    }

    data = {}
    with requests.Session() as s:
        download = s.get(protocol + host + service, params=payload)
        data = download.json()

    return data

if __name__ == "__main__":

    # Let's track how long this takes.
    program_start_time = clock.time()

    min_year = 0
    max_year = 2023
    min_eq_magnitude = 1

    results = get_earthquakes(min_year, max_year, min_eq_magnitude)

    # Crear una lista para almacenar los registros en el formato adecuado
    records = []

    # Obtener la clave "items" del resultado
    items = results["items"]

    # Iterar sobre los elementos de la lista y convertirlos al formato adecuado
    for item in items:
        record = json.loads(json.dumps(item))
        records.append(record)

    # Crear el DataFrame con las columnas especificadas
    df = pd.DataFrame(records, columns=['id', 'year', 'month', 'day', 'hour', 'locationName', 'latitude', 'longitude', 'eqMagnitude', 'eqDepth', 'damageAmountOrder', 'damageMillionsDollars', 'publish', 'housesDestroyedAmountOrderTotal', 'country', 'deathsAmountOrder', 'injuriesAmountOrderTotal', 'intensity'])

    # Guardar el DataFrame en un archivo CSV
    df.to_csv("../Data/Raw data/NOAA.csv", index=False)

    # Capturar el tiempo de ejecución del programa.
    elapsed_time = clock.time() - program_start_time
    print('Tiempo de ejecución del programa [s]: {:0.3f}'.format(elapsed_time))
