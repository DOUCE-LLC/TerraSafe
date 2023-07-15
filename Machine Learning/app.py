import streamlit as st
import pandas as pd
import numpy as np
from sklearn.svm import SVC

data_st = pd.read_csv('./Machine Learning/noaa_ml.csv')  # Reemplaza 'datos_sismos.csv' con la ruta a tu archivo de datos

data_st['clase_sismo'] = pd.qcut(data_st['magnitudSismo'], q=5, labels=['Muy Leve', 'Leve', 'Medio', "Fuerte", "Muy Fuerte"])

X_train = data_st[['magnitudSismo', 'ordenCantidadMuertesActualizadas','ordenCantidadCasasDestruidasActualizadas','ordenCantidadDanosActualizados']]  # Selecciona las características relevantes
y_train = data_st['clase_sismo']  # Selecciona la etiqueta/clase a predecir

model = SVC()  # Crea una instancia del modelo SVM
model.fit(X_train, y_train)  # Entrena el modelo SVM

st.title('Proyecto de Sismos con Modelo SVM')
st.write('Ingrese las características del sismo para predecir la etiqueta:')

feature1 = st.slider('magnitudSismo', min_value=0.0, max_value=10.0, step=0.1)
feature2 = st.slider('ordenCantidadMuertesActualizadas', min_value=0.0, max_value=10.0, step=0.1)
feature3 = st.slider('ordenCantidadCasasDestruidasActualizadas', min_value=0.0, max_value=10.0, step=0.1)
feature4 = st.slider('ordenCantidadDanosActualizados', min_value=0.0, max_value=10.0, step=0.1)
prediction = model.predict([[feature1, feature2, feature3, feature4]])

st.write('La etiqueta predicha para las características proporcionadas es:', prediction)
