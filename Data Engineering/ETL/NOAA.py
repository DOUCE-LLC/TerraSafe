import json
import requests
import pandas as pd
import numpy as np

# Interfaz grafica: https://www.ngdc.noaa.gov/hazel/view/hazards/earthquake/search

def dropUnnecessaryColumns(df):
    columns_to_drop = ['id', 'publish', 'regionCode', 'eqMagMw', 'eqMagMb', 'eqMagUnk', 'eqMagMl', 'volcanoEventId', 'tsunamiEventId', 'eqMagMfa', 'eqMagMs', 'hour', 'second', 'minute', 'missing', 'missingAmountOrder', 'missingTotal', 'missingAmountOrderTotal', 'area']
    df.drop(columns=columns_to_drop, inplace=True)
    return df

def dateColumn(df):
    df['year'].fillna(3000, inplace=True)
    df['month'].fillna(0, inplace=True)
    df['day'].fillna(0, inplace=True)

    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['day'] = df['day'].astype(int)

    df['year'] = df['year'].astype(str)
    df['month'] = df['month'].astype(str)
    df['day'] = df['day'].astype(str)

    # Agregar ceros a las columnas 'month' y 'day' si tienen un solo dígito o son null/vacíos
    df['month'] = df['month'].fillna('').apply(lambda x: str(x).zfill(2))
    df['day'] = df['day'].fillna('').apply(lambda x: str(x).zfill(2))
    
    # Reemplazar los valores de año null/vacíos por 'null'
    df['year'] = df['year'].fillna('null')
    
    # Concatenar las columnas year, month, y day en formato AAAA-MM-DD
    df['date'] = df[['year', 'month', 'day']].agg('-'.join, axis=1)
    
    return df

def dropDateColumns(df):
    df = df.drop(['year', 'month', 'day'], axis=1)
    return df

# Deaths columns...

def updatedDeaths(df):
    df['updatedDeaths'] = df[['deathsTotal', 'deaths']].max(axis=1)
    return df

def updatedDeathsAmountOrder(df):
    df['updatedDeathsAmountOrder'] = df[['deathsAmountOrder', 'deathsAmountOrderTotal']].max(axis=1)
    return df

def dropDeathsColumns(df):
    df = df.drop(['deathsTotal', 'deaths', 'deathsAmountOrder', 'deathsAmountOrderTotal'], axis=1)
    return df

def fillUpdatedDeaths(df):
    # Operación 1: Llenar valores en updatedDeaths cuando updatedDeathsAmountOrder no es nulo y updatedDeaths es nulo
    for index, row in df.iterrows():
        if pd.notnull(row['updatedDeathsAmountOrder']) and pd.isnull(row['updatedDeaths']):
            if row['updatedDeathsAmountOrder'] == 0:
                df.at[index, 'updatedDeaths'] = 0
            elif row['updatedDeathsAmountOrder'] == 1:
                df.at[index, 'updatedDeaths'] = 1
            elif row['updatedDeathsAmountOrder'] == 2:
                df.at[index, 'updatedDeaths'] = 51
            elif row['updatedDeathsAmountOrder'] == 3:
                df.at[index, 'updatedDeaths'] = 101
            elif row['updatedDeathsAmountOrder'] == 4:
                df.at[index, 'updatedDeaths'] = 1000
    return df

def fillUpdatedDeaths2(df):
    # Operación 2: Rellenar valores en updatedDeathsAmountOrder si es nulo, según el rango correspondiente en updatedDeaths
    for index, row in df.iterrows():
        if pd.isnull(row['updatedDeathsAmountOrder']) and pd.notnull(row['updatedDeaths']):
            updated_deaths = row['updatedDeaths']
            if updated_deaths == 0:
                df.at[index, 'updatedDeathsAmountOrder'] = 0
            elif 1 <= updated_deaths <= 50:
                df.at[index, 'updatedDeathsAmountOrder'] = 1
            elif 51 <= updated_deaths <= 100:
                df.at[index, 'updatedDeathsAmountOrder'] = 2
            elif 101 <= updated_deaths <= 1000:
                df.at[index, 'updatedDeathsAmountOrder'] = 3
            elif updated_deaths > 1000:
                df.at[index, 'updatedDeathsAmountOrder'] = 4
    return df

# Injuries columns...

def updatedInjuries(df):
    df['updatedInjuries'] = df[['injuriesTotal', 'injuries']].max(axis=1)
    return df

def updatedInjuriesAmountOrder(df):
    df['updatedInjuriesAmountOrder'] = df[['injuriesAmountOrder', 'injuriesAmountOrderTotal']].max(axis=1)
    return df

def dropInjuriesColumns(df):
    df = df.drop(['injuriesTotal', 'injuries', 'injuriesAmountOrder', 'injuriesAmountOrderTotal'], axis=1)
    return df

def fillUpdatedInjuries(df):
    # Operación 1: Llenar valores en updatedInjuries cuando updatedInjuriesAmountOrder no es nulo y updatedInjuries es nulo
    for index, row in df.iterrows():
        if pd.notnull(row['updatedInjuriesAmountOrder']) and pd.isnull(row['updatedInjuries']):
            if row['updatedInjuriesAmountOrder'] == 0:
                df.at[index, 'updatedInjuries'] = 0
            elif row['updatedInjuriesAmountOrder'] == 1:
                df.at[index, 'updatedInjuries'] = 1
            elif row['updatedInjuriesAmountOrder'] == 2:
                df.at[index, 'updatedInjuries'] = 51
            elif row['updatedInjuriesAmountOrder'] == 3:
                df.at[index, 'updatedInjuries'] = 101
            elif row['updatedInjuriesAmountOrder'] == 4:
                df.at[index, 'updatedInjuries'] = 1000
    return df

def fillUpdatedInjuries2(df):
    # Operación 2: Rellenar valores en updatedInjuriesAmountOrder si es nulo, según el rango correspondiente en updatedInjuries
    for index, row in df.iterrows():
        if pd.isnull(row['updatedInjuriesAmountOrder']) and pd.notnull(row['updatedInjuries']):
            updated_injuries = row['updatedInjuries']
            if updated_injuries == 0:
                df.at[index, 'updatedInjuriesAmountOrder'] = 0
            elif 1 <= updated_injuries <= 50:
                df.at[index, 'updatedInjuriesAmountOrder'] = 1
            elif 51 <= updated_injuries <= 100:
                df.at[index, 'updatedInjuriesAmountOrder'] = 2
            elif 101 <= updated_injuries <= 1000:
                df.at[index, 'updatedInjuriesAmountOrder'] = 3
            elif updated_injuries > 1000:
                df.at[index, 'updatedInjuriesAmountOrder'] = 4
    return df

# HousesDamaged columns...

def updatedHousesDamaged(df):
    df['updatedHousesDamaged'] = df[['housesDamagedTotal', 'housesDamaged']].max(axis=1)
    return df

def updatedHousesDamagedAmountOrder(df):
    df['updatedHousesDamagedAmountOrder'] = df[['housesDamagedAmountOrder', 'housesDamagedAmountOrderTotal']].max(axis=1)
    return df

def dropHousesDamagedColumns(df):
    df = df.drop(['housesDamagedTotal', 'housesDamaged', 'housesDamagedAmountOrder', 'housesDamagedAmountOrderTotal'], axis=1)
    return df

def fillUpdatedHousesDamaged(df):
    # Operación 1: Llenar valores en updatedHousesDamaged cuando updatedHousesDamagedAmountOrder no es nulo y updatedHousesDamaged es nulo
    for index, row in df.iterrows():
        if pd.notnull(row['updatedHousesDamagedAmountOrder']) and pd.isnull(row['updatedHousesDamaged']):
            if row['updatedHousesDamagedAmountOrder'] == 0:
                df.at[index, 'updatedHousesDamaged'] = 0
            elif row['updatedHousesDamagedAmountOrder'] == 1:
                df.at[index, 'updatedHousesDamaged'] = 1
            elif row['updatedHousesDamagedAmountOrder'] == 2:
                df.at[index, 'updatedHousesDamaged'] = 51
            elif row['updatedHousesDamagedAmountOrder'] == 3:
                df.at[index, 'updatedHousesDamaged'] = 101
            elif row['updatedHousesDamagedAmountOrder'] == 4:
                df.at[index, 'updatedHousesDamaged'] = 1000
    return df

def fillUpdatedHousesDamaged2(df):
    # Operación 2: Rellenar valores en updatedHousesDamagedAmountOrder si es nulo, según el rango correspondiente en updatedHousesDamaged
    for index, row in df.iterrows():
        if pd.isnull(row['updatedHousesDamagedAmountOrder']) and pd.notnull(row['updatedHousesDamaged']):
            updated_housesDamaged = row['updatedHousesDamaged']
            if updated_housesDamaged == 0:
                df.at[index, 'updatedHousesDamagedAmountOrder'] = 0
            elif 1 <= updated_housesDamaged <= 50:
                df.at[index, 'updatedHousesDamagedAmountOrder'] = 1
            elif 51 <= updated_housesDamaged <= 100:
                df.at[index, 'updatedHousesDamagedAmountOrder'] = 2
            elif 101 <= updated_housesDamaged <= 1000:
                df.at[index, 'updatedHousesDamagedAmountOrder'] = 3
            elif updated_housesDamaged > 1000:
                df.at[index, 'updatedHousesDamagedAmountOrder'] = 4
    return df

# HousesDestroyed columns...

def updatedHousesDestroyed(df):
    df['updatedHousesDestroyed'] = df[['housesDestroyedTotal', 'housesDestroyed']].max(axis=1)
    return df

def updatedHousesDestroyedAmountOrder(df):
    df['updatedHousesDestroyedAmountOrder'] = df[['housesDestroyedAmountOrder', 'housesDestroyedAmountOrderTotal']].max(axis=1)
    return df

def dropHousesDestroyedColumns(df):
    df = df.drop(['housesDestroyedTotal', 'housesDestroyed', 'housesDestroyedAmountOrder', 'housesDestroyedAmountOrderTotal'], axis=1)
    return df

def fillUpdatedHousesDestroyed(df):
    # Operación 1: Llenar valores en updatedHousesDestroyed cuando updatedHousesDestroyedAmountOrder no es nulo y updatedHousesDestroyed es nulo
    for index, row in df.iterrows():
        if pd.notnull(row['updatedHousesDestroyedAmountOrder']) and pd.isnull(row['updatedHousesDestroyed']):
            if row['updatedHousesDestroyedAmountOrder'] == 0:
                df.at[index, 'updatedHousesDestroyed'] = 0
            elif row['updatedHousesDestroyedAmountOrder'] == 1:
                df.at[index, 'updatedHousesDestroyed'] = 1
            elif row['updatedHousesDestroyedAmountOrder'] == 2:
                df.at[index, 'updatedHousesDestroyed'] = 51
            elif row['updatedHousesDestroyedAmountOrder'] == 3:
                df.at[index, 'updatedHousesDestroyed'] = 101
            elif row['updatedHousesDestroyedAmountOrder'] == 4:
                df.at[index, 'updatedHousesDestroyed'] = 1000
    return df

def fillUpdatedHousesDestroyed2(df):
    # Operación 2: Rellenar valores en updatedHousesDestroyedAmountOrder si es nulo, según el rango correspondiente en updatedHousesDestroyed
    for index, row in df.iterrows():
        if pd.isnull(row['updatedHousesDestroyedAmountOrder']) and pd.notnull(row['updatedHousesDestroyed']):
            updated_housesDestroyed = row['updatedHousesDestroyed']
            if updated_housesDestroyed == 0:
                df.at[index, 'updatedHousesDestroyedAmountOrder'] = 0
            elif 1 <= updated_housesDestroyed <= 50:
                df.at[index, 'updatedHousesDestroyedAmountOrder'] = 1
            elif 51 <= updated_housesDestroyed <= 100:
                df.at[index, 'updatedHousesDestroyedAmountOrder'] = 2
            elif 101 <= updated_housesDestroyed <= 1000:
                df.at[index, 'updatedHousesDestroyedAmountOrder'] = 3
            elif updated_housesDestroyed > 1000:
                df.at[index, 'updatedHousesDestroyedAmountOrder'] = 4
    return df

# Damage columns...

def updatedDamage(df):
    df['updatedDamage'] = df[['damageMillionsDollarsTotal', 'damageMillionsDollars']].max(axis=1)
    return df

def updatedDamageAmountOrder(df):
    df['updatedDamageAmountOrder'] = df[['damageAmountOrder', 'damageAmountOrderTotal']].max(axis=1)
    return df

def dropDamageColumns(df):
    df = df.drop(['damageMillionsDollarsTotal', 'damageMillionsDollars', 'damageAmountOrder', 'damageAmountOrderTotal'], axis=1)
    return df

def fillUpdatedDamage(df):
    # Operación 1: Llenar valores en updatedDamage cuando updatedDamageAmountOrder no es nulo y updatedDamage es nulo
    for index, row in df.iterrows():
        if pd.notnull(row['updatedDamageAmountOrder']) and pd.isnull(row['updatedDamage']):
            if row['updatedDamageAmountOrder'] == 0:
                df.at[index, 'updatedDamage'] = 0.0
            elif row['updatedDamageAmountOrder'] == 1:
                df.at[index, 'updatedDamage'] = 0.5
            elif row['updatedDamageAmountOrder'] == 2:
                df.at[index, 'updatedDamage'] = 1.0
            elif row['updatedDamageAmountOrder'] == 3:
                df.at[index, 'updatedDamage'] = 5.0
            elif row['updatedDamageAmountOrder'] == 4:
                df.at[index, 'updatedDamage'] = 25.0
    return df

def fillUpdatedDamage2(df):
    # Operación 2: Rellenar valores en updatedDamageAmountOrder si es nulo, según el rango correspondiente en updatedDamage
    for index, row in df.iterrows():
        if pd.isnull(row['updatedDamageAmountOrder']) and pd.notnull(row['updatedDamage']):
            updated_damage = row['updatedDamage']
            if updated_damage == 0.0:
                df.at[index, 'updatedDamageAmountOrder'] = 0
            elif 0.0 <= updated_damage < 1.0:
                df.at[index, 'updatedDamageAmountOrder'] = 1
            elif 1.0 <= updated_damage < 5.0:
                df.at[index, 'updatedDamageAmountOrder'] = 2
            elif 5.0 <= updated_damage < 25.0:
                df.at[index, 'updatedDamageAmountOrder'] = 3
            elif updated_damage > 25.0:
                df.at[index, 'updatedDamageAmountOrder'] = 4
    return df


# def loadAPI(min_year, max_year, min_eq_magnitude, country):
def loadAPI(min_year, max_year, min_eq_magnitude):

    api = "https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/earthquakes"

    payload = {
        'minYear': str(min_year),
        'maxYear': str(max_year),
        'minEqMagnitude': str(min_eq_magnitude)
        # 'country': country
    }

    data = []
    with requests.Session() as s:
        download = s.get(api, params=payload)
        data = download.json()
        print(download.url)

    # Crear una lista para almacenar los registros en el formato adecuado
    records = []

    # Obtener la clave "items" del resultado
    items = data["items"]

    # Iterar sobre los elementos de la lista y convertirlos al formato adecuado
    for item in items:
        record = json.loads(json.dumps(item))
        records.append(record)

    df = pd.DataFrame(records)

    # Transformaciones...
    df = dropUnnecessaryColumns(df)
    df = dateColumn(df)
    df = dropDateColumns(df)
    df = updatedDeaths(df)
    df = updatedDeathsAmountOrder(df)
    df = fillUpdatedDeaths(df)
    df = fillUpdatedDeaths2(df)
    df = dropDeathsColumns(df)
    df = updatedInjuries(df)
    df = updatedInjuriesAmountOrder(df)
    df = fillUpdatedInjuries(df)
    df = fillUpdatedInjuries2(df)
    df = dropInjuriesColumns(df)
    df = updatedHousesDamaged(df)
    df = updatedHousesDamagedAmountOrder(df)
    df = fillUpdatedHousesDamaged(df)
    df = fillUpdatedHousesDamaged2(df)
    df = dropHousesDamagedColumns(df)
    df = updatedHousesDestroyed(df)
    df = updatedHousesDestroyedAmountOrder(df)
    df = fillUpdatedHousesDestroyed(df)
    df = fillUpdatedHousesDestroyed2(df)
    df = dropHousesDestroyedColumns(df)
    df = updatedDamage(df)
    df = updatedDamageAmountOrder(df)
    df = fillUpdatedDamage(df)
    df = fillUpdatedDamage2(df)
    df = dropDamageColumns(df)

    # df.to_csv(f"./demos/NOAA_{country}_{min_year}_{max_year}.csv", index=False)
    df.to_csv(f"./demos/NOAA_{min_year}_{max_year}.csv", index=False)
    print('')

# loadAPI(0, 2023, 0, 'CHILE')
# loadAPI(0, 2023, 0, 'USA')
# loadAPI(0, 2023, 0, 'JAPAN')
loadAPI(0, 2023, 0)