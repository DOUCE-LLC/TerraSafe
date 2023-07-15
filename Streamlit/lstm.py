import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import os

def Lstm():
    # Título de la página de inicio
    st.title('TerraSafe - LSTM')

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './Streamlit/terra-safe.json'

    # Create a BigQuery client with the credentials
    bq_client = bigquery.Client()

    # Query your table
    query = "SELECT * FROM `terra-safe-391718.AIRFLOW.USGS_CHI` LIMIT 100"
    df = bq_client.query(query).to_dataframe()

    # Display the table in Streamlit
    st.dataframe(df)
