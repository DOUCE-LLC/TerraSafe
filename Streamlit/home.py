import streamlit as st
from PIL import Image

def Home():
    # Título de la página de inicio
    st.title('TerraSafe')

    image = Image.open("./Img/TerraSafe.png")                       # Carga la imagen
    st.image(image, caption="TerraSafe", use_column_width=True)     # Muestra la imagen en la aplicación

    st.subheader("Welcome to the Terra Safe platform! On this website, you'll discover a collection of powerful tools designed to assist governments worldwide and organizations like the Red Cross. With advanced machine learning systems, interactive dashboards, and automated data extraction, we're here to make a difference!")
    st.write("Our first machine learning model within Terra Safe aims to predict the behaviour of future earthquake cycles in specific regions. This capability allows us to allocate resources efficiently during peak cycles for disaster relief and, during the minimums, invest in infrastructure and early warning systems to mitigate future damages.")
    st.write("Moreover, we offer another machine learning system for earthquake classification. By inputting earthquake characteristics, this system efficiently categorizes them, enabling us to prioritize aid distribution effectively.")
    st.write("Our platform also boasts an interactive dashboard powered by Looker. Continuously updated with new earthquake data, this dashboard offers detailed worldwide seismic analysis, giving valuable insights into earthquake patterns.")
    st.write("Lastly, we've implemented a robust system to control data extraction and transformation for new earthquake records. Our user-friendly interface on Airflow runs seamlessly on Google Cloud Platform (GCP), ensuring updated data feeds into our machine learning systems and dashboards. For added security, we've set up a backup cloud with virtual machines to guarantee access to the most current data, even in unforeseen circumstances.")
    st.subheader("At Terra Safe, we combine cutting-edge technology with a touch of simplicity to make a real impact in earthquake preparedness and response. Together, let's build a safer and resilient world!")

