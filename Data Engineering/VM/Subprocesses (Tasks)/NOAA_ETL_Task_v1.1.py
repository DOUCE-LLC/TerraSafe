import json
import pandas as pd
import numpy as np
import os
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists, InvalidArgument
from google.cloud.pubsub import PublisherClient, SchemaServiceClient
from google.pubsub_v1.types import Encoding
from google.pubsub_v1.types import Schema
from google.oauth2 import service_account
import schedule
import time
import logging
from concurrent.futures import TimeoutError

# -------------- Constants ----------------
project_id = 'terra-safe-391718'
topic_id = 'ETL_data'
subscription_id = 'NOAA_data-sub'
timeout = 20  #Time the subscriber client awaits for a message
topic_bq_id = "To_Big_Query"
schema_id = "NOAA_schema"
message_encoding = "JSON"
Dataset_id = "VIRTUAL_MACHINE"
Table_id = "NOAA_VM"


#Dataframe columns normalization
def df_cols_norm(df):
    columns_names_list = ['id', 'year', 'month', 'day', 'hour', 'minute', 'second',
     'locationName', 'latitude', 'longitude', 'eqDepth', 'eqMagnitude', 
     'deaths', 'deathsAmountOrder', 'injuriesAmountOrder', 'damageAmountOrder', 
     'tsunamiEventId', 'volcanoEventId', 'eqMagMw', 'eqMagMs', 'eqMagMb', 'publish',
     'deathsTotal', 'deathsAmountOrderTotal', 'injuriesAmountOrderTotal', 'damageAmountOrderTotal',
     'country', 'regionCode', 'intensity', 'housesDestroyedAmountOrder', 'housesDamagedAmountOrder',
     'housesDestroyedTotal', 'housesDestroyedAmountOrderTotal', 'housesDamagedAmountOrderTotal', 
     'housesDestroyed', 'injuries', 'housesDamaged', 'injuriesTotal', 'housesDamagedTotal', 'eqMagMl',
     'damageMillionsDollars', 'damageMillionsDollarsTotal', 'area', 'missingAmountOrderTotal', 
     'eqMagUnk', 'missing', 'missingAmountOrder', 'missingTotal', 'eqMagMfa']

    # Reindexing the dataframe including every column with their right position
    df = df.reindex(columns=columns_names_list, fill_value=0)
    logging.info("Normalized dataframe")
    return(df)


def dropUnnecessaryColumns(df):
    logging.info("dropUnnessaryColumns %s", df)
    columns_to_drop = ['id', 'publish', 'regionCode', 'eqMagMw', 'eqMagMb', 'eqMagUnk', 'eqMagMl', 'eqMagMfa', 'eqMagMs', 'hour', 'second', 'minute', 'missing', 'missingAmountOrder', 'missingTotal', 'missingAmountOrderTotal', 'area']
    df.drop(columns=columns_to_drop, inplace=True)
    return df

def eqDepthColumn(df):
    df['eqDepth'] = df['eqDepth'].astype(float)
    return df

def dateColumn(df):
    df['year'].fillna(3000, inplace=True)
    df['month'].fillna(0, inplace=True)
    df['day'].fillna(0, inplace=True)

    # Convertir las columnas 'year', 'month' y 'day' a tipo entero
    df[['year', 'month', 'day']] = df[['year', 'month', 'day']].astype(int)

    # Ordenar el DataFrame por la columna 'year' de forma ascendente
    df.sort_values(by='year', ascending=True, inplace=True)

    df[['year', 'month', 'day']] = df[['year', 'month', 'day']].astype(str)

    # Agregar ceros a las columnas 'month' y 'day' si tienen un solo dígito o son null/vacíos
    df['month'] = df['month'].fillna('').apply(lambda x: str(x).zfill(2))
    df['day'] = df['day'].fillna('').apply(lambda x: str(x).zfill(2))
    df['year'] = df['year'].fillna('').apply(lambda x: str(x).zfill(4))

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

def tsunamisAndVolcanos(df):
    columns = ['volcanoEventId', 'tsunamiEventId']
    df[columns] = df[columns].fillna(0).astype(bool).astype(int)
    df.rename(columns={'volcanoEventId': 'volcano', 'tsunamiEventId': 'tsunami'}, inplace=True)
    return df


# Function to process the received messages
def process_message(df):

    # Transformations...
    logging.info("df_cols_norm")
    df = df_cols_norm(df)
    logging.info("dropUnnecesaryColumns") 
    df = dropUnnecessaryColumns(df)
    logging.info("dateColumn")
    df = dateColumn(df)
    logging.info("dropDateColumns")
    df = dropDateColumns(df)
    logging.info("updatedDeaths")
    df = updatedDeaths(df)
    logging.info("updatedDeathsAmountOrder")
    df = updatedDeathsAmountOrder(df)
    logging.info("fillUpdateDeaths")
    df = fillUpdatedDeaths(df)
    logging.info("fillUpdatedDeaths2")
    df = fillUpdatedDeaths2(df)
    logging.info("dropDeathsColumns")
    df = dropDeathsColumns(df)
    logging.info("updatedInjuries")
    df = updatedInjuries(df)
    logging.info("updatedInjuriesAmountOrder")
    df = updatedInjuriesAmountOrder(df)
    logging.info("fillUpdatedInjuries")
    df = fillUpdatedInjuries(df)
    logging.info("fillUpdatedInjuries2")
    df = fillUpdatedInjuries2(df)
    logging.info("dropInjuriesColumns")
    df = dropInjuriesColumns(df)
    logging.info("updatedHousesDamaged")
    df = updatedHousesDamaged(df)
    logging.info("updatedHousesDamagedAmountOrder")
    df = updatedHousesDamagedAmountOrder(df)
    logging.info("fillUpdatedHousesDamaged")
    df = fillUpdatedHousesDamaged(df)
    logging.info("fillUpdatedHousesDamaged2")
    df = fillUpdatedHousesDamaged2(df)
    logging.info("dropHousesDamagedColumns")
    df = dropHousesDamagedColumns(df)
    logging.info("updatedHousesDestroyed")
    df = updatedHousesDestroyed(df)
    logging.info("updatedHousesDestroyedAmountOrder")
    df = updatedHousesDestroyedAmountOrder(df)
    logging.info("fillUpdatedHousesDestroyed")
    df = fillUpdatedHousesDestroyed(df)
    logging.info("fillUpdatedHousesDestroyed2")
    df = fillUpdatedHousesDestroyed2(df)
    logging.info("dropHousesDestroyedColumns")
    df = dropHousesDestroyedColumns(df)
    logging.info("updatedDamage")
    df = updatedDamage(df)
    logging.info("updatedDamageAmountOrder")
    df = updatedDamageAmountOrder(df)
    logging.info("fillUpdatedDamage")
    df = fillUpdatedDamage(df)
    logging.info("fillUpdatedDamage2")
    df = fillUpdatedDamage2(df)
    logging.info("dropDamageColumns")
    df = dropDamageColumns(df)
    logging.info("tsunamisAndVolcanos")
    df = tsunamisAndVolcanos(df)

    return (df)



# -------------------- Publish Message to Big Query -----------------------
def publishMessage_to_Big_Query(df):
    logging.info("DF:%s", df)
    logging.debug("Getting a publisher client")
    # Publish the JSON as message on Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    logging.debug("Getting the topic_path")
    topic_path = publisher.topic_path(project_id, topic_bq_id)
    #Serialize the transformed dataframe as a diccionary list
    dicc_list = df.to_dict(orient='records')
    #Replacing NaN values for "NaN" (protocol-buffer schema compatibility)
    for dicc in dicc_list:
        for key, value in dicc.items():
            if value != value:  # Checking if value is NaN
                dicc[key] = "NaN"
    #Formatting each record inside received message and publishing to Big Query topic
    for records in dicc_list:
        etl_message = json.dumps(records).encode('utf-8')
        logging.info("message to be published: %s", etl_message)
        logging.debug("Publishing the message")
        future = publisher.publish(topic_path, data=etl_message)
        logging.debug("Waiting confirmation")
        # Waiting until message publication be informed
        pub_status = future.result()
        logging.debug('Publishing message status %s', pub_status)
  

# ------------------- Callback Function --------------------
def callback(api_message: pubsub_v1.subscriber.message.Message) -> None:
    logging.debug("Message received")
    api_message.ack()
    logging.debug("Message; %s", api_message)
     # Decoding the message
    message_data = api_message.data.decode('utf-8')
    logging.info("Message data: %s", message_data)
    # Parsing the string as JSON
    json_data = json.loads(message_data)
    logging.info("JSON data: %s", json_data)
    # Build the dataframe
    df = pd.DataFrame(json_data)
    #Making the transformations
    transformed_df = process_message(df)
    logging.info("DF Transformed")
    #transformed_df = df
    publishMessage_to_Big_Query(transformed_df)
    


#--------- MAIN -------------------------------------------------------------------------------------

# File log config
logging.basicConfig(filename='/home/santiagomartearena6/NOAA_ETL_Task.log', level=logging.DEBUG) 
logging.info("Initiating NOAA_ETL_Task...")

# Configure the authentication credentials
credentials_path = "./terra-safe-391718-ed256dd5a716.json"
logging.info("Getting the credentials...")
credentials = service_account.Credentials.from_service_account_file(credentials_path)
logging.info("Credentials created %s", credentials)
# Forever loop
while True:
    logging.info("Getting a subscriber client")
    subscriber = pubsub_v1.SubscriberClient()
    # Define the subscription from messages will be received
    logging.info("Getting the subscription path")
    subscription_path = subscriber.subscription_path(project_id, subscription_id)    
    logging.info("Asking if there are messages for me")
    # Receiving messages
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    logging.info(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with pubsub_v1.SubscriberClient() as subscriber:
        logging.info("Inside with pubsub struct")
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=None)
            logging.info("Going out streaming_pull_future")
        except TimeoutError:
            logging.info("Inside TimeoutError")
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete
            logging.info("Shutdown is completed")
    logging.info("Going to sleep for a while")
    # Delay until the next message check
    time.sleep(5) 
    
