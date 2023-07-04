# import argparse
import json
import requests
import pandas as pd

def loadAPI(min_year, max_year, min_eq_magnitude, country):

    api = "https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/earthquakes"

    payload = {
        'minYear': str(min_year),
        'maxYear': str(max_year),
        'minEqMagnitude': str(min_eq_magnitude),
        'country': country
    }

    data = []
    with requests.Session() as s:
        download = s.get(api, params=payload)
        data = download.json()

    # Crear una lista para almacenar los registros en el formato adecuado
    records = []

    # Obtener la clave "items" del resultado
    items = data["items"]

    # Iterar sobre los elementos de la lista y convertirlos al formato adecuado
    for item in items:
        record = json.loads(json.dumps(item))
        records.append(record)

    df = pd.DataFrame(records)
    df.to_csv("./demos/NOAA_CHILE_RESULTS.csv", index=False)

loadAPI(0, 2023, 0, 'Chile')






# min_year = 0
# max_year = 2023
# min_eq_magnitude = 0
# country = "Chile"

# results = loadAPI(min_year, max_year, min_eq_magnitude, country)