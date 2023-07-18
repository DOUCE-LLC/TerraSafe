import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

import os
import pandas as pd
import numpy as np
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns


def Svm():
    # Título de la página de inicio
    st.title('TerraSafe - SVM')

    # Configurar las credenciales de autenticación para BigQuery
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../Streamlit/terra-safe.json'
    

    # Crear un cliente de BigQuery con las credenciales
    bq_client = bigquery.Client()

    # Consultar tu tabla en BigQuery
    query = f"""
                SELECT eqMagnitude, updatedDeathsAmountOrder, updatedHousesDestroyedAmountOrder
                FROM `terrasafe-2.AIRFLOW.NOAA`
                WHERE eqMagnitude IS NOT NULL AND updatedHousesDestroyedAmountOrder IS NOT NULL AND updatedDeathsAmountOrder IS NOT NULL
                ORDER BY time ASC;
            """
    df = bq_client.query(query).to_dataframe()

    # Llenar los valores faltantes con 0
    df.fillna(0, inplace=True)

    # Separar las características (X) y el objetivo (y)
    X = df[['eqMagnitude', 'updatedHousesDestroyedAmountOrder',
            'updatedDeathsAmountOrder']].values
    y = df['eqMagnitude'].apply(
        lambda x: 'Bajo' if x < 5 else 'Moderado' if x < 6 else 'Fuerte' if x < 7 else 'Mayor').values

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=1)

    # Escalar las características para tener una mejor convergencia en el modelo SVM
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Entrenar el modelo SVM
    svm_model = SVC(kernel='linear', C=1)
    svm_model.fit(X_train_scaled, y_train)

    st.write('Ingrese las características del sismo para predecir la etiqueta:')

    feature1 = st.slider('eqMagnitude', min_value=0.0,
                         max_value=10.0, step=0.1)
    feature2 = st.slider('updatedHousesDestroyedAmountOrder',
                         min_value=0.0, max_value=10.0, step=0.1)
    feature3 = st.slider('updatedDeathsAmountOrder',
                         min_value=0.0, max_value=10.0, step=0.1)
    prediction = svm_model.predict([[feature1, feature2, feature3]])

    st.write(
        'La etiqueta predicha para las características proporcionadas es:', prediction)
