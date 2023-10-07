import streamlit as st
from streamlit_extras.app_logo import add_logo
add_logo("gallery/ResizeWW.png", height=100)

st.markdown("![Alt Text](https://media.giphy.com/media/1whOBHdMW10bAmLybr/giphy.gif)")

st.header("We are the Wage Warriors")

with st.expander("Meet the team"):
    st.write("UTS Master of Data Science and Innovation, partnered with the Australian Payroll Association"
             "\n - Akshaya"
             "\n - Denneya "
             "\n - Shalimar"
             "\n - William")