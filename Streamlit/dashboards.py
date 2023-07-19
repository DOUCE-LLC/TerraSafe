import streamlit as st
from PIL import Image

def Dashboards():
    # Título de la página de inicio
    st.title('TerraSafe - Dashboard')

    image = Image.open("./Img/dash_1.jpeg")                       # Carga la imagen
    st.image(image, caption="", use_column_width=True)            # Muestra la imagen en la aplicación

    st.markdown("[View Dashboard here...](https://lookerstudio.google.com/reporting/e5be3890-c51c-4a2f-9878-47130bde0271)")

    st.write("The TerraSafe Control Panel is an exceptional tool designed for decision-making in the management and planning of natural disasters caused by seismic movements. Its functionality and precision make it the perfect ally to face these challenges with efficiency and confidence.")
    st.write("This powerful system features real-time visualizations that allow you to observe the latest earthquakes recorded in Chile, the United States, Japan, and worldwide. Through a rapid identification system based on the magnitude of events, it provides valuable and up-to-date information instantly.")
    st.write("Furthermore, the TerraSafe Control Panel offers dynamic tables, charts, and various types of visualizations. These tools can be applied to different countries and customized according to the needs and required timeframe for thorough work. The available filters ensure precise and comprehensive analysis.")
    st.write("With two Key Performance Indicator (KPI) panels, this dashboard allows you to make optimal decisions in resource allocation both globally and within each country. These panels provide a clear and detailed view for effective and strategic resource designation in each territory and facilitate decision-making at the national level, optimizing resource deployment within each nation.")
    
    image2 = Image.open("./Img/dash_2.jpeg")                       # Carga la imagen
    st.image(image2, caption="", use_column_width=True)            # Muestra la imagen en la aplicación

    st.write("Likewise, the TerraSafe Control Panel includes two tabs dedicated to secondary disasters, such as tsunamis and volcanic eruptions. This ensures a comprehensive and complete response to various adverse scenarios.")
    st.write("All these features are at your fingertips from the dashboard homepage, which offers shortcuts to each of the required characteristics. Tables, bar charts, satellite maps, and performance indicators with clear objectives are just some of the tools you'll find in this comprehensive control panel.")
    st.write("The product has been specifically designed to meet the needs of personnel responsible for planning, logistics, and resource management of the International Red Cross, as well as any organization dedicated to natural disaster relief. While it primarily focuses on countries highly affected by seismic movements such as the United States, Chile, and Japan, it also includes a global data source for relevant magnitude earthquakes.")
    st.write("Don't risk uncertainty in the face of natural disasters. The TerraSafe Control Panel provides you with the confidence and capability to make informed and strategic decisions in critical situations. Contact us today and discover how this tool can make a difference in your response to natural disasters.")

    # Add a link
    st.markdown("[View Dashboard here...](https://lookerstudio.google.com/reporting/e5be3890-c51c-4a2f-9878-47130bde0271)")

    image3 = Image.open("./Img/dash_3.jpeg")                       # Carga la imagen
    st.image(image3, caption="", use_column_width=True)            # Muestra la imagen en la aplicación