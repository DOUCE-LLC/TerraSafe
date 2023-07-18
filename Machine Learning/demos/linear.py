import datetime
import time

import altair as alt
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression

def LiearRegression():
    # Título de la página de inicio
    st.title('TerraSafe - Polynomial Regression')

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './Streamlit/terra-safe.json'

    # Create a BigQuery client with the credentials
    bq_client = bigquery.Client()

    # Query your table
    query = "SELECT * FROM `terra-safe-391718.AIRFLOW.USGS_CHI` ORDER BY time ASC LIMIT 10000"
    df = bq_client.query(query).to_dataframe()

    # Display the table in Streamlit
    st.dataframe(df)

    # Crear un modelo de regresión lineal
    model = LinearRegression()

    # Entrenar el modelo con los datos históricos
    X = df[['year']]
    y = df['job_title_count']
    model.fit(X, y)