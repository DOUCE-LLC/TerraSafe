import json
import pandas as pd
from google.cloud import pubsub_v1
from google.cloud import bigquery
import requests
import schedule
import time
from datetime import datetime, timedelta
import logging

#Logging control
DEBUG = True

#Global variable definition
project_id = 'terra-safe-391718'
topic_id = 'USGS-JPN_data'
subscription_id = 'start_delta_USGS-JPN-sub'
pubsub_client = None
topic_path = None
http_timeout = 10

# Checking if Pub/Sub client is active
def is_pubsub_client_active():
    global pubsub_client
    return pubsub_client is not None

# Getting or creating a Pub/Sub client
def get_pubsub_client():
    global pubsub_client
    global topic_path
    if not is_pubsub_client_active():
        pubsub_client = pubsub_v1.PublisherClient()
        topic_path = pubsub_client.topic_path(project_id, topic_id)

    return pubsub_client


# USGS-CHI API call function
def loadAPI(start_year, end_year):
    for year in range(start_year, end_year+1):
        for month in range(1, 13):
            logging.info("YEAR: %s - MONTH: %s", str(year), str(month))
            url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={year}-{month}-01&endtime={year}-{month}-31&minlatitude=24.396308&maxlatitude=45.551483&minlongitude=122.934570&maxlongitude=154.003906'
            logging.info("USGS URL: %s", url)
            df = pd.DataFrame()

            data = []
            
            with requests.Session() as s:
                response = requests.get(url)

                try:
                    data = response.json()
                    # Manejar la respuesta de la API
                    logging.info("HTTP STATUS: %s", str(response.status_code))
                    if response.status_code == 200:
                        # Procesar la respuesta exitosa
                        api_processing(data)
                    else:
                        # Manejar errores de respuesta
                        logging.info(f'Query Error: {response.status_code}')
                    
                except json.decoder.JSONDecodeError:
                    logging.info(f"Error en: {year}-{month}")

# ----------------- Processing API response --------------------
def api_processing(data):
    records = []                                                   # Creat a list to store registries in the adequate format
    logging.info("RECORD: %s", data)
    for feature in data["features"]:                               # Iterating over each feature
                            
        properties = feature["properties"]                         # Getting earthquake properties
        #logging.info("PROPERTIES: %s", properties)
        geometry = feature["geometry"]                             # Getting earthquake geometry
        #logging.info("GEOMETRY: %s", geometry)
        time = properties["time"]                                  # Extracting the individual values
        mag = properties["mag"]
        cdi = properties["cdi"]
        mmi = properties["mmi"]
        place = properties["place"]
        dmin = properties["dmin"]
        earthquakeType = properties["type"]
        tsunami = properties["tsunami"]
        sig = properties["sig"]
        coordinates = geometry["coordinates"]
                        
        records.append((time, mag, cdi, mmi, dmin, place, earthquakeType, coordinates, sig, tsunami)) # Adding the individual values to the records list
        #logging.info("RECORDS: %s", records)
    if records:    # Checking if records list is not empty
        df = pd.DataFrame(records, columns=["time", "mag", "cdi", "mmi", "dmin", "place", "earthquakeType", "coordinates", "sig", "tsunami"])
    # Checking if month has data
        publish_msg(df)
        df.to_csv("USGS-CHI.csv", mode='a', header=True, index=False)    


# ---------- Get Start and end Year for USGS-JPN API Query ------------    
def get_date_params():    
    client = bigquery.Client()                                                      # Create a Google Cloud Storage client 
    table_ref = 'terra-safe-391718.AIRFLOW.USGS_JPN'                                # Specify your BigQuery table ID        
    client.get_table(table_ref)                                                 # Check if the table exists
    query = f"""
    SELECT EXTRACT(YEAR FROM time) AS max_year
    FROM `{table_ref}`
    ORDER BY time DESC
    LIMIT 1
    """
    query_job = client.query(query)
    result = query_job.result()
    has_rows = False
    for row in result:
       has_rows = True
       last_row = row
    if (has_rows == True):
        start_year = int(last_row['max_year'])
    else:
       start_year = 2023
        
    logging.info("START YEAR: %s", start_year)
    end_year = datetime.now().year
    logging.info("END YEAR: %s", end_year)
    loadAPI(start_year, end_year)
    

# ----------------- Publishing message corresponding to monthly events  -------------------
def publish_msg(data):
    logging.info("Serializing dataframe")
    json_data = data.to_json(orient='records')
    # Formatting message
    logging.info("formatting message")
    #message = json.dumps(json_data).encode('utf-8')
    message = json_data.encode('utf-8')
    logging.info('JSON formatted')
    logging.info("Message to be published %s", message)
    logging.info("Getting Pub/Sub client")   
    pubsub_client = get_pubsub_client()
    if pubsub_client:
        # Publishing the message
        future = pubsub_client.publish(topic_path, data=message)
        # Waiting until message publication be informed
        logging.info("Waiting for confirmation")
        result = future.result()
        logging.info('Successful publishing message %s', result)
    else:
        # Manage in case of Pub/Sub is not available
        logging.info("Unsuccessful Pub/Sub client adquisition. Check configuration")



# Callback function
def read_api_and_publish(pubsub_message: pubsub_v1.subscriber.message.Message) -> None:
    logging.debug("Message received")
    pubsub_message.ack()
    logging.debug("Message; %s", pubsub_message)
    logging.info("Inside read_api_and_publish")
     # API query 
    get_date_params()
    logging.info("Finishing query")
    
    

#------------- MAIN -------------------
# File log config
logging.basicConfig(filename='/home/santiagomartearena6/USGS-JPN_API_Task.log', level=logging.DEBUG) 
logging.info("Initiating USGS-CHI API Task..")

#Creating a Pub/Sub client
logging.info("Creating a Pub/Sub client")
pubsub_client = pubsub_v1.PublisherClient()
logging.info("getting a topic_path")
topic_path = pubsub_client.topic_path(project_id, topic_id)

# Forever loop
while True:
    logging.info("Getting a subscriber client")
    subscriber = pubsub_v1.SubscriberClient()
    # Define the subscription from messages will be received
    logging.info("Getting the subscription path")
    subscription_path = subscriber.subscription_path(project_id, subscription_id)    
    logging.info("Asking if there are messages for me")
    # Receiving messages
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=read_api_and_publish)
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
