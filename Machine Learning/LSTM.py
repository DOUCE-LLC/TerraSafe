import numpy as np
np.random.seed(4)
import matplotlib.pyplot as plt
import pandas as pd

from keras.models import Sequential
from keras.layers import LSTM, Dense

#----- Start coding... ------------------------------------------------------------------------------------------------------------------------------------------

df = pd.read_csv('./jpn - USGS_JPN.csv')
print(df.head())

df['time'] = pd.to_datetime(df['time'])                                         # Convert the 'time' column to datetime format
df = df.set_index('time')                                                       # Set the 'time' column as the index

#----- Pre-procesamiento de los datos -----------------------------------------------------------------------------------------------------------

set_entrenamiento = df['2023-01':'2023-05'].iloc[:,0:1]                         # Filter the data for the specified months
set_validacion = df['2023-06'].iloc[:,0:1]                                      # Filter the data for the specified months

#----- Normalización de los datos ------------------------------------------------------------------------------------------------------------

sc = MinMaxScaler(feature_range=(0,1))
set_entrenamiento_escalado = sc.fit_transform(set_entrenamiento)

#----- Ajuste de los sets de entrenamiento y validación ------------------------------------------------------------------------------------------

time_step = 60
X_train = []
Y_train = []
m = len(set_entrenamiento_escalado)

for i in range(time_step,m):
    X_train.append(set_entrenamiento_escalado[i-time_step:i,0])                 # X: bloques de "time_step" datos: 0-time_step, 1-time_step+1, 2-time_step+2, etc
    Y_train.append(set_entrenamiento_escalado[i,0])                             # Y: el siguiente dato
X_train, Y_train = np.array(X_train), np.array(Y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

#----- Creación y entrenamiento de la Red LSTM --------------------------------------------------------------------------------------------------

dim_entrada = (X_train.shape[1],1)                                              # datos de entrada
dim_salida = 1                                                                  # dato de salida
na = 100                                                                        # número total de neuronas 

modelo = Sequential()                                                           # crear un contenedor para crear la Red LSTM

modelo.add(LSTM(units=na, input_shape=dim_entrada))                             # Añadimos la Red LSTM usando la función add, especificando el número de neuronas a usar (parámetro units) y el tamaño de cada dato de entrada (parámetro input_shape)
modelo.add(Dense(units=dim_salida))                                             # Especificamos que el dato de salida tendrá un tamaño igual a 1
modelo.compile(optimizer='rmsprop', loss='mse')                                 # compilar el modelo
modelo.fit(X_train,Y_train,epochs=20,batch_size=32)                             # Entrenamiento

#----- Predicción del valor de la magnitud -------------------------------------------------------------------------------------------------------------

x_test = set_validacion.values
x_test = sc.transform(x_test)

X_test = []
for i in range(time_step,len(x_test)):
    X_test.append(x_test[i-time_step:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))

prediccion = modelo.predict(X_test)
prediccion = sc.inverse_transform(prediccion)