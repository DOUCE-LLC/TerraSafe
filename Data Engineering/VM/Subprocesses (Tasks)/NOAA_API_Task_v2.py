import json
import pandas as pd
from google.cloud import pubsub_v1
import requests
import schedule
import time
import logging

#Logging control
DEBUG = True

#Global variable definition
project_id = 'terra-safe-391718'
topic_id = 'NOAA_data'
subscription_id = 'start_delta_NOAA-sub'
timeout = 10  #Time the subscriber client awaits for a message

# NOAA API call function
def loadAPI(min_year, max_year, min_eq_magnitude):

    api = "https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/earthquakes"

    payload = {
        'minYear': str(min_year),
        'maxYear': str(max_year),
        'minEqMagnitude': str(min_eq_magnitude)
        }

    data = []
    with requests.Session() as s:
        download = s.get(api, params=payload)
        data = download.json()
        logging.info("DOWNLOAD URL %s", download.url)

    return(data)


# Callback function
def read_api_and_publish(pubsub_message: pubsub_v1.subscriber.message.Message) -> None:
    logging.debug("Message received")
    pubsub_message.ack()
    logging.debug("Message; %s", pubsub_message)
    logging.info("Inside read_api_and_publish")
     # API query 
    noaa_data = loadAPI(2022, 2023, 0)
    logging.info("API raw data: %s", noaa_data)
    #noaa_data = {'NOAA API Data':'Data Received'}
    # Get the result "items" key
    dicc = noaa_data.get('items')
    logging.info("DICC: %s", dicc)
    #Create a dataframe with data received
    df_noaa = pd.DataFrame(dicc)
    logging.info("Data delivered: %s", df_noaa)
    #logging.info("DF INFO %s", df_noaa.info())
    # Serialize the DataFrame with JSON format
    json_data = df_noaa.to_json(orient='records')
    #json_data = {'NOAA API message': 'Payload'}
    # Create a Pub/Sub client
    logging.info("Getting a pubsub client")
    publisher = pubsub_v1.PublisherClient()
    # Define the destination topic 
    logging.info("getting a topic_path")
    topic_path = publisher.topic_path(project_id, topic_id)
    # Publish the payload message
    logging.info("formatting message")
    #message = json.dumps(json_data).encode('utf-8')
    message = json_data.encode('utf-8')
    logging.info('JSON formatted')
    logging.info("Publishing message %s", message)
    future = publisher.publish(topic_path, data=message)
    # Waiting until message publication be informed
    logging.info("Waiting for confirmation")
    result = future.result()
    logging.info('Successful publishing message %s', result)


#------------- MAIN -------------------
# File log config
logging.basicConfig(filename='/home/santiagomartearena6/NOAA_API_Task.log', level=logging.DEBUG) 
logging.info("Initiating NOAA API Task..")
logging.info("Getting a subscriber client")
subscriber = pubsub_v1.SubscriberClient()
# Define the subscription from messages will be received
logging.info("Getting the subscription path")
subscription_path = subscriber.subscription_path(project_id, subscription_id)    

    # Forever loop
while True:
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
