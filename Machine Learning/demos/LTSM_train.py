import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

def visualizar(real, prediccion):
    plt.plot(real,color='red', label='Real Mag')
    plt.plot(prediccion, color='blue', label='Mag Prediction')
    plt.xlabel('time')
    plt.ylabel('mag')
    plt.legend()
    plt.show()

my_dataset = pd.read_csv('./jpn.csv')
dataset = my_dataset[::-1]

dataset['time'] = pd.to_datetime(dataset['time'], format='%d/%m/%Y %H:%M:%S')

trainingSet = dataset[(dataset['time'].dt.year != 2023) & (dataset['time'].dt.month != 6)].iloc[:, 1:2]
testSet = dataset[(dataset['time'].dt.year == 2023) & (dataset['time'].dt.month == 6)].iloc[:, 1:2]

""" Normalización del set de entrenamiento (valores entre 0 y 1). """
sc = MinMaxScaler(feature_range=(0,1))
trainingSetScaled = sc.fit_transform(trainingSet)

""" Vamos a entrenar a la Red proporcionando 5 datos de entrada y 1 de salida en cada iteración """
timeSteps = 5
xTrain = []
yTrain = []

""" xTrain = lista de conjuntos de 100 datos.
    yTrain = lista de valores """
for i in range(0, len(trainingSetScaled)-timeSteps):
    xTrain.append(trainingSetScaled[i:i+timeSteps, 0])
    yTrain.append(trainingSetScaled[i+timeSteps,0])

""" Preferiblemente usar numpy ya que:
    1. Deberemos transformar xTrain (actualmente de dos dimensiones) a tres dimensiones.
    2. Los programas que usan Numpy generalmente son más rápidos (sobretodo en IA).
"""
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
regresor.fit(xTrain,yTrain,epochs=5, batch_size=32)

""" Normalizar el conjunto de Test y relizamos las mismas operaciones que anteriormente """
auxTest = sc.transform(testSet.values)
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

# Graficar resultados
visualizar(testSet.values,prediccion)

