# librerias
import streamlit as st
from streamlit_option_menu import option_menu

# paginas
from Streamlit.home import Home
from Streamlit.sinusoidal import Sinusoidal
from Streamlit.svm import Svm
from Streamlit.dashboards import Dashboards
from Streamlit.etl import Etl

import os

# link necesario para bootstrap
st.markdown("""<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>""",
            unsafe_allow_html=True)

# Menu horizontal
selected = option_menu(None, ["Home", "Dash", "Predict", "SVM", "ETL"],
                        icons=['house', 'bi-bar-chart', "bi-graph-up-arrow", "bi-globe-americas", "bi-hammer"],
                        menu_icon="cast",
                        default_index=0,
                        orientation="horizontal",
                        )

# Home
if selected == "Home":
    Home()

# Análisis
elif selected == "Dash":
    Dashboards()

# Predictions
elif selected == "Predict":
    Sinusoidal()

# SVM
elif selected == "SVM":
    Svm()

# ETL
elif selected == "ETL":
    Etl()