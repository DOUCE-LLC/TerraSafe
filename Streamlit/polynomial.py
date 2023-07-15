import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression

def PolynomialRegression():
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

#     # Extract the last value from the DataFrame
#     last_value = df.iloc[-1]

#     # Create a new DataFrame with 30 dates
#     date_range = pd.date_range(start=last_value['time'], periods=30, freq='D')
#     new_df = pd.DataFrame({'time': date_range})

#     ''' Polynomial Regression '''

#     df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S')
#     new_df['time'] = pd.to_datetime(new_df['time'], format='%d/%m/%Y %H:%M:%S')

#     df = df.iloc[:, 0:2]

#     """ Normalización del set de entrenamiento (valores entre 0 y 1). """
#     sc = MinMaxScaler(feature_range=(0,1))
#     # Exclude the 'time' column from scaling
#     df_scaled = sc.fit_transform(df.drop('time', axis=1))

#     """ Vamos a entrenar a la Regresión Proporcionando 5 datos de entrada y 1 de salida en cada iteración """
#     timeSteps = 10
#     xTrain = []
#     yTrain = []

#     """ xTrain = lista de conjuntos de 100 datos.
#         yTrain = lista de valores """
#     for i in range(0, len(df_scaled)-timeSteps):
#         xTrain.append(df_scaled[i:i+timeSteps, 0])
#         yTrain.append(df_scaled[i+timeSteps, 0])

#     xTrain, yTrain = np.array(xTrain), np.array(yTrain)

#     """ Hay que añadir una dimensión a xTrain para que funcione con Polynomial Regression """
#     xTrain = np.reshape(xTrain, (xTrain.shape[0], xTrain.shape[1]))

#     # Fit the Polynomial Regression model
#     poly_features = PolynomialFeatures(degree=3)
#     xTrain_poly = poly_features.fit_transform(xTrain)

#     regressor = LinearRegression()
#     regressor.fit(xTrain_poly, yTrain)

#     """ Preparing data for prediction """
#     xTest = []

#     # Use the last 'timeSteps' rows from the training set as input for prediction
#     xTest.append(df_scaled[-timeSteps:, 0])

#     xTest = np.array(xTest)
#     xTest = np.reshape(xTest, (xTest.shape[0], xTest.shape[1]))

#     # Transform test data using Polynomial Features
#     xTest_poly = poly_features.transform(xTest)

#     """ Realizamos la Predicción """
#     prediccion = regressor.predict(xTest_poly)

#     """ Desnormalizamos la Predicción para que se encuentre entre valores normales. """
#     prediccion = sc.inverse_transform(prediccion.reshape(-1, 1))

#     # Generate the x-axis values for the prediction
#     prediction_dates = pd.date_range(start=new_df['time'].iloc[0], periods=len(prediccion), freq='D')

#     # Create a DataFrame for the prediction data
#     prediction_data = pd.DataFrame({'time': prediction_dates, 'Prediction': prediccion.flatten()})

#     # Display the line chart of the prediction
#     st.line_chart(prediction_data.set_index('time'))

    # Convert the 'Date' column to Unix timestamp
    df['time'] = df['time'].apply(lambda x: pd.Timestamp(x).timestamp())

    X = df.iloc[:, 1:2].values
    y = df.iloc[:, 1:2].values

    poly_reg = PolynomialFeatures(degree = 4)
    X_poly = poly_reg.fit_transform(X)
    lin_reg = LinearRegression()
    lin_reg.fit(X_poly, y)

    y_pred = lin_reg.predict(X_poly)

    df = pd.DataFrame({'Real Values':y, 'Predicted Values':y_pred})
    print(df)

    # Generate the x-axis values for the prediction
    prediction_dates = pd.date_range(start=df['time'].iloc[0], periods=len(y_pred), freq='D')

    # Create a DataFrame for the prediction data
    prediction_data = pd.DataFrame({'time': prediction_dates, 'Prediction': y_pred.flatten()})

    # Display the line chart of the prediction
    st.line_chart(prediction_data.set_index('time'))
