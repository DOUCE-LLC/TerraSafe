import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

def Lstm():
    # Título de la página de inicio
    st.title('TerraSafe - LSTM')

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './Streamlit/terra-safe.json'

    # Create a BigQuery client with the credentials
    bq_client = bigquery.Client()

    # Query your table
    query = "SELECT * FROM `terra-safe-391718.AIRFLOW.USGS_CHI` ORDER BY time ASC LIMIT 10000"
    df = bq_client.query(query).to_dataframe()

    # Display the table in Streamlit
    st.dataframe(df)

    # Extract the last value from the DataFrame
    last_value = df.iloc[-1]

    # Create a new DataFrame with 30 dates
    date_range = pd.date_range(start=last_value['time'], periods=30, freq='D')
    new_df = pd.DataFrame({'time': date_range})

    # Display the new DataFrame in Streamlit
    st.dataframe(new_df)


    ''' LSTM '''

    df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S')
    # new_df['time'] = pd.to_datetime(new_df['time'], format='%d/%m/%Y %H:%M:%S')
    new_df['time'] = pd.to_numeric(pd.to_datetime(new_df['time']))

    df = df.iloc[:, 0:2]
    new_df = new_df.iloc[:, 0:2]

    """ Normalización del set de entrenamiento (valores entre 0 y 1). """
    sc = MinMaxScaler(feature_range=(0,1))
    trainingSetScaled = sc.fit_transform(df)

    """ Vamos a entrenar a la Red proporcionando 5 datos de entrada y 1 de salida en cada iteración """
    timeSteps = 10
    xTrain = []
    yTrain = []

    """ xTrain = lista de conjuntos de 100 datos.
        yTrain = lista de valores """
    for i in range(0, len(trainingSetScaled)-timeSteps):
        xTrain.append(trainingSetScaled[i:i+timeSteps, 0])
        yTrain.append(trainingSetScaled[i+timeSteps,0])

    xTrain, yTrain = np.array(xTrain), np.array(yTrain)

    """ Hay que añadir una dimensión a xTrain, nos lo pide la libreria Keras """
    xTrain = np.reshape(xTrain, (xTrain.shape[0], xTrain.shape[1], 1))

    """ Parámetros que deberemos proporcionar a Keras (Sequential()). """
    dim_entrada = (xTrain.shape[1],1) # No hace falta la primera.
    dim_salida = 1
    na = 10

    """ units = neuronas de la capa | return_sequences = hay más capas? | input_shape = dimensión entrada | 
        Dropout(%) = Número de neuronas que queremos ignorar en la capa de regularización (normalmente es de un 20%). """
    regresor = Sequential() # Inicializa el modelo


    """ capa 1 """
    regresor.add(LSTM(units=na, input_shape=dim_entrada))

    """ capa output """
    regresor.add(Dense(units=dim_salida))

    regresor.compile(optimizer='rmsprop', loss='mse') # mse = mean_squared_error

    """ Encajar Red Neuronal en Set Entrenamiento """
    """ epochs = iteraciones para entrenar tu modelo | 
    batch_size = numero ejemplos entrenamiento (cuanto más alto, más memoria necesitarás).  """
    regresor.fit(xTrain,yTrain,epochs=20, batch_size=32)

        
    """ Normalizar el conjunto de Test y relizamos las mismas operaciones que anteriormente """
    auxTest = sc.transform(new_df.values)
    xTest = []

    for i in range(0, len(auxTest) - timeSteps):
        xTest.append(auxTest[i:i + timeSteps, 0])
        
    xTest = np.array(xTest)

    print('Shape: ', xTest.shape)

    xTest = np.reshape(xTest, (xTest.shape[0],xTest.shape[1], 1))

    """ Realizamos la Predicción """
    prediccion = regresor.predict(xTest)

    """ Desnormalizamos la Predicción para que se encuentre entre valores normales. """
    prediccion = sc.inverse_transform(prediccion)


    # # Generate some example data
    # x = np.linspace(0, 10, 100)
    # y = np.sin(x)

    # # Create a DataFrame from the data
    # data = pd.DataFrame({'x': x, 'y': y})

    # # Display the line chart in Streamlit
    # st.line_chart(data['y'])

    # Generate the x-axis values for the prediction
    prediction_dates = pd.date_range(start=new_df['time'].iloc[0], periods=len(prediccion), freq='D')

    # Create a DataFrame for the prediction data
    prediction_data = pd.DataFrame({'time': prediction_dates, 'Prediction': prediccion.flatten()})

    # Display the line chart of the prediction
    st.line_chart(prediction_data['Prediction'])