import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

import os
import pandas as pd
import numpy as np
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns


# def Svm():
#     # Título de la página de inicio
#     st.title('TerraSafe - SVM')

#     st.write("The Support Vector Machine (SVM) is a supervised learning algorithm that aims to find the optimal hyperplane to separate data into different classes. Support vectors are data points that are closest to the hyperplane and play a crucial role in constructing the classifier. The goal of SVM is to find the hyperplane that maximizes the margin between classes, providing good generalization ability and resistance to noisy data.")
#     st.write("In the context of seismic data processing, SVM can be used to classify earthquakes into different categories or levels of intensity (e.g. 'Low', 'Moderate', 'Strong', 'Major') based on relevant features such as earthquake magnitude, the amount of destroyed houses, and the number of registered deaths.")
#     st.write("SVM is a powerful tool for classifying data into different categories and can be used in the context of seismic data processing to predict the intensity of future earthquakes based on the provided features. By identifying cyclic patterns and relationships among the features, SVM can provide valuable information for earthquake forecasting and seismic risk assessment.")

#     # Configurar las credenciales de autenticación para BigQuery
#     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './Streamlit/terrasafe-2-a2b1cdf482ec.json'

#     # Crear un cliente de BigQuery con las credenciales
#     bq_client = bigquery.Client()

#     # Consultar tu tabla en BigQuery
#     query = f"""
#                 SELECT eqMagnitude, updatedDeathsAmountOrder, updatedHousesDestroyedAmountOrder
#                 FROM `terrasafe-2.AIRFLOW.NOAA`
#                 WHERE eqMagnitude IS NOT NULL AND updatedHousesDestroyedAmountOrder IS NOT NULL AND updatedDeathsAmountOrder IS NOT NULL
#                 ORDER BY date ASC;
#             """
#     df = bq_client.query(query).to_dataframe()

#     # Llenar los valores faltantes con 0
#     df.fillna(0, inplace=True)

#     # Separar las características (X) y el objetivo (y)
#     X = df[['eqMagnitude', 'updatedHousesDestroyedAmountOrder',
#             'updatedDeathsAmountOrder']].values
#     y = df['eqMagnitude'].apply(
#         lambda x: 'Bajo' if x < 5 else 'Moderado' if x < 6 else 'Fuerte' if x < 7 else 'Mayor').values

#     # Dividir los datos en conjuntos de entrenamiento y prueba
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=0.2, random_state=1)

#     # Escalar las características para tener una mejor convergencia en el modelo SVM
#     scaler = StandardScaler()
#     X_train_scaled = scaler.fit_transform(X_train)
#     X_test_scaled = scaler.transform(X_test)

#     # Entrenar el modelo SVM
#     svm_model = SVC(kernel='linear', C=1)
#     svm_model.fit(X_train_scaled, y_train)

#     st.write('Ingrese las características del sismo para predecir la etiqueta:')

#     feature1 = st.slider('eqMagnitude', min_value=0.0,
#                          max_value=10.0, step=0.1)
#     feature2 = st.slider('updatedHousesDestroyedAmountOrder',
#                          min_value=0.0, max_value=10.0, step=0.1)
#     feature3 = st.slider('updatedDeathsAmountOrder',
#                          min_value=0.0, max_value=10.0, step=0.1)
#     prediction = svm_model.predict([[feature1, feature2, feature3]])

#     st.write(
#         'La etiqueta predicha para las características proporcionadas es:', prediction)


import streamlit as st
import pandas as pd
import numpy as np
from sklearn.svm import SVC

def Svm():
    # Título de la página de inicio
    st.title('TerraSafe - SVM')

    # data_st = pd.read_csv('./Machine Learning/noaa_ml.csv')  # Reemplaza 'datos_sismos.csv' con la ruta a tu archivo de datos

        # Configurar las credenciales de autenticación para BigQuery
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './Streamlit/terrasafe-2-a2b1cdf482ec.json'

    # Crear un cliente de BigQuery con las credenciales
    bq_client = bigquery.Client()

    # Consultar tu tabla en BigQuery
    query = f"""
                SELECT *
                FROM `terrasafe-2.AIRFLOW.NOAA`
                ORDER BY date ASC;
            """
    data_st = bq_client.query(query).to_dataframe()

    # Llenar los valores faltantes con 0
    data_st.fillna(0, inplace=True)

    # Multiply 'tsunami' and 'volcano' by 10
    data_st['tsunami'] *= 10
    data_st['volcano'] *= 10

    # Multiply 'updatedDeathsAmountOrder', 'updatedInjuriesAmountOrder', 'updatedHousesDamagedAmountOrder', and 'updatedHousesDestroyedAmountOrder' by 2
    data_st['updatedDeathsAmountOrder'] *= 2
    data_st['updatedInjuriesAmountOrder'] *= 2
    data_st['updatedHousesDamagedAmountOrder'] *= 2
    data_st['updatedHousesDestroyedAmountOrder'] *= 2

    # Calculate the mean of the modified features and store it in a new column 'mean_features'
    data_st['mean_features'] = data_st[['eqMagnitude', 'updatedDeathsAmountOrder', 'updatedInjuriesAmountOrder', 'updatedHousesDamagedAmountOrder', 'updatedHousesDestroyedAmountOrder', 'tsunami', 'volcano']].mean(axis=1)


    # Separate the features (X) and the target (y)
    X = data_st[['eqMagnitude', 'updatedDeathsAmountOrder', 'updatedInjuriesAmountOrder', 'updatedHousesDamagedAmountOrder', 'updatedHousesDestroyedAmountOrder', 'tsunami', 'volcano']].values
    y = data_st['mean_features'].apply(lambda x: 'Low' if x < 5 else 'Moderate' if x < 6 else 'Significant' if x < 7 else 'Strong').values

    # Divide the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    # Scale the features for better convergence in the SVM model
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train the SVM model
    svm_model = SVC(kernel='linear', C=1)
    svm_model.fit(X_train_scaled, y_train)

    st.write('Enter the earthquake characteristics to predict the label:')

    feature1 = st.slider('Magnitude', min_value=0.0, max_value=10.0, step=0.1)
    feature2 = st.slider('Deaths', min_value=0.0, max_value=4.0, step=1.0)
    feature3 = st.slider('Injuries', min_value=0.0, max_value=4.0, step=1.0)
    feature4 = st.slider('Houses Damaged', min_value=0.0, max_value=4.0, step=1.0)
    feature5 = st.slider('Houses Destroyed', min_value=0.0, max_value=4.0, step=1.0)
    feature6 = st.slider('tsunami', min_value=0.0, max_value=1.0, step=1.0)
    feature7 = st.slider('volcano', min_value=0.0, max_value=1.0, step=1.0)

    prediction = svm_model.predict([[feature1, feature2, feature3, feature4, feature5, feature6, feature7]])

    st.write('The predicted label for the provided features is:', prediction)