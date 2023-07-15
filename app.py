import streamlit as st

# Título de la página de inicio
st.title('TerraSafe - Machine Learning')

# LSTM dropdown
lstm_expanded = st.expander("LSTM (Long Short-Term Memory)")
with lstm_expanded:
    st.write("LSTM is a type of recurrent neural network (RNN) that is specifically designed to capture and model long-term dependencies in sequential data, such as earthquake time series. Unlike traditional feedforward neural networks, LSTM has the ability to retain and utilize information from previous time steps, making it well-suited for predicting the future cyclic behavior of earthquakes. By training an LSTM model on historical earthquake data, we can estimate the future patterns and cyclic trends in seismic activity, which can be invaluable for understanding earthquake dynamics and aiding in earthquake forecasting and risk assessment.")

# SVM dropdown
svm_expanded = st.expander("SVM (Support Vector Machine)")
with svm_expanded:
    st.write("SVM is a machine learning algorithm used for classification tasks, including earthquake classification. It works by finding an optimal hyperplane that separates different classes of earthquakes based on their features. SVM is particularly useful for earthquake classification because it can handle high-dimensional feature spaces and is effective in handling both linear and non-linear relationships in the data. By using SVM, we can accurately classify earthquakes based on their characteristics and make informed decisions regarding their severity and potential impact.")

# Imagen y enlace para el modelo LSTM
lstm_image = './Img/LSTM.jpeg'
lstm_url = '/lstm'

# Imagen y enlace para el modelo SVM
svm_image = './Img/SVM.png'
svm_url = '/svm'

# Mostrar las imágenes y enlazarlas a las páginas correspondientes
col1, col2 = st.columns(2)

with col1:
    st.image(lstm_image, use_column_width=True,)
    st.markdown(f"""
    <a href={lstm_url} style="color: white; text-decoration: none;">
        <h4 style="text-align: center">LSTM</h4>
    </a>""", unsafe_allow_html=True)

with col2:
    st.image(svm_image, use_column_width=True)
    st.markdown(f"""
    <a href={svm_url} style="color: white; text-decoration: none;">
        <h4 style="text-align:center">SVM</h4>
    </a>""", unsafe_allow_html=True)
