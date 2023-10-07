import streamlit as st
from PIL import Image

from streamlit_extras.app_logo import add_logo
add_logo("gallery/ResizeWW.png", height=100)

st.header("Exploring unfair pay", divider="rainbow")

fairpay = Image.open("gallery/Fair Pay.jpg")
st.image(fairpay, caption="Photo by Ehimetalor Akhere Unuabona, from Unsplash")


