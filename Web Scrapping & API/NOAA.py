import argparse
import json
import requests
import time as clock
import pandas as pd

def get_earthquakes(min_year, max_year, min_eq_magnitude):
    protocol = "https://"
    host = "www.ngdc.noaa.gov"
    service = "/hazel/hazard-service/api/v1/earthquakes"

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

    program_start_time = clock.time()

    min_year = 0
    max_year = 2023
    min_eq_magnitude = 1

    results = get_earthquakes(min_year, max_year, min_eq_magnitude)

    records = []

    items = results["items"]

    for item in items:
        record = json.loads(json.dumps(item))
        records.append(record)

    # df = pd.DataFrame(records, columns=['id', 'year', 'month', 'day', 'hour', 'locationName', 'latitude', 'longitude', 'eqMagnitude', 'eqDepth', 'damageAmountOrder', 'damageMillionsDollars', 'publish', 'housesDestroyedAmountOrderTotal', 'country', 'deathsAmountOrder', 'injuriesAmountOrderTotal', 'intensity'])
    df = pd.DataFrame(records)

    df.to_csv("../Data/Raw data/Raw_NOAA.csv", index=False)

    elapsed_time = clock.time() - program_start_time
    print('Tiempo de ejecución del programa [s]: {:0.3f}'.format(elapsed_time))