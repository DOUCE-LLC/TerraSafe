import json
import pandas as pd
import numpy as np
import os
from google.cloud import pubsub_v1
from google.cloud import bigquery
from google.api_core.exceptions import AlreadyExists, InvalidArgument
from google.cloud.pubsub import PublisherClient, SchemaServiceClient
from google.pubsub_v1.types import Encoding
from google.pubsub_v1.types import Schema
from google.oauth2 import service_account
import schedule
import time
from datetime import datetime, timedelta
import logging
from concurrent.futures import TimeoutError

# -------------- Constants ----------------
project_id = 'terra-safe-391718'
topic_id = 'USGS-USA_ETL_data'
subscription_id = 'USGS-USA_data-sub'
timeout = 20  #Time the subscriber client awaits for a message
topic_bq_id = "To_USGS-USA_Big_Query"
schema_id = "USGS_schema"
message_encoding = "JSON"
Dataset_id = "AIRFLOW"
Table_CHI_id = "USGS_USA"


# ------------- Remove columns --------------
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
    #logging.info("TIMESTAMP: %s", str(df['time']))
    df['time'] = df['time'].apply(lambda x: datetime.fromtimestamp(int(x) / 1000).strftime('%Y-%m-%d'))
    #logging.info("DATE: %s", str(df['time']))
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

def process_message(df):
    
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
                    
    return (df)

# ------------- Deleting duplicate records on Big Query table ----------------
def delete_duplicates():
    client = bigquery.Client()                                                      # Create a Google Cloud Storage client 
    table_ref = 'terra-safe-391718.AIRFLOW.USGS_CHI'                                # Specify your BigQuery table ID

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
    logging.info("Executing deduplication query")
    query_job = client.query(deduplication_query)
    query_job.result()





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
    #Reformatting time field data type from Timestamp to string
    for dicc in dicc_list:
        for key, value in dicc.items():
            dicc['time'] = str(dicc['time'])
     
    #Formatting each record inside received message and publishing to Big Query topic
    for records in dicc_list:
        logging.info("Records time %s", records)
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
    transformed_df.to_csv("USGS-CHI_ETL.csv", mode='a', header=True, index=False)
    #transformed_df = df
    publishMessage_to_Big_Query(transformed_df)
    


#--------- MAIN -------------------------------------------------------------------------------------

# File log config
logging.basicConfig(filename='/home/santiagomartearena6/USGS-USA_ETL_Task.log', level=logging.DEBUG) 
logging.info("Initiating USGS-CHI_ETL_Task...")

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
            streaming_pull_future.result(timeout=timeout)
            logging.info("Going out streaming_pull_future")
        except TimeoutError:
            logging.info("Inside TimeoutError")
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete
            logging.info("Shutdown is completed")
    logging.info("Going to sleep for a while")
    # Delay until the next message check
    time.sleep(5) 
    
