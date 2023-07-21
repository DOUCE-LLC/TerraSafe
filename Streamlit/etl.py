import streamlit as st
from PIL import Image

def Etl():
    st.title('TerraSafe - ETL')

    st.subheader("Airflow🚀")

    st.write("Notice those delightful dark green buttons scattered across the screen? When they're all glowing in that rich shade of green, you can rest assured that our data extraction and transformation are purring along perfectly, just like a well-oiled machine!")

    image = Image.open("./Img/Airflow.png")                                               # Carga la imagen
    st.image(image, caption="Airflow interface", use_column_width=True)                             # Muestra la imagen en la aplicación
    st.markdown("[View Airflow here...]()")

    st.write("But hold on, we've got more in store for you! We know flexibility is crucial, so we've added nifty sliders that give you control. If you ever need to conserve cloud resources, simply slide those buttons to the left, and voilà! Your data extraction takes a little break, keeping everything in check.")
    st.write("Now, let's talk about speed. We've got you covered! Each task on our platform comes with its very own 'Play' button. If you're eager for immediate updates, go ahead and hit 'Play' – it's like pressing the refresh button on your browser but for our data.")

    st.subheader("Virtual Machine")

    st.write("Picture this: the ultimate guardian angel for your data – the Virtual Machine! 🦸‍♀️🔮")
    st.write("Meet our trusty backup hero, the Virtual Machine (VM). When our star performer, Airflow, is running the show on its home server in Google Cloud Platform (GCP), the VM stands ready in the wings, ever vigilant.")
    st.write("Now, imagine a rare situation where our main server faces a hiccup. It's the tech equivalent of a rainy day, but fret not! The VM swoops in with a swish of its cape to save the day. In a blink of an eye, it steps up, flawlessly taking over Airflow's role, ensuring our data processing never skips a beat.")
    st.write("The VM acts like a safety net, ready to catch and carry the torch if anything goes awry. It's our trusty backup buddy, ensuring we're never caught off guard and always on top of our data game.")
    st.write("So rest easy, dear user. Our duo – Airflow and the Virtual Machine – have got your back, ensuring a smooth and seamless data journey in the magical world of GCP! 🌟🌈")
