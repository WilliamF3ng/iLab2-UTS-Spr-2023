import streamlit as st
from PIL import Image

from streamlit_extras.app_logo import add_logo
add_logo("gallery/ResizeWW.png", height=100)

st.header("Meet the brains behind Know Your Wages", divider="rainbow")
st.markdown('''UTS Master of Data Science and Innovation (MDSI) students, partnered with Australian Payroll Association.''')


image = Image.open("gallery/WW.png")
st.image(image)

col1, col2, col3, col4 = st.columns(4, gap="medium")
with col1:
    st.image("gallery/LI-Logo.png")
    st.caption(
       "[Connect with Askhaya](https://www.linkedin.com/in/iaks23/)")
    st.markdown('''Background in Computer Science. Personal interest in projects with a cause and understanding the payroll industry.''')
with col2:
    st.image("gallery/LI-Logo.png")
    st.caption(
        "[Connect with Denneya](https://www.linkedin.com/in/denneya/)")
    st.markdown('''Background in Mathematics and Statistics. Personal interest in developing resources to educate people.''')
with col3:
    st.image("gallery/LI-Logo.png")
    st.caption(
        "[Connect with Shalimar](https://www.linkedin.com/in/shalimar-chalhoub-1690b0200/)")
    st.markdown('''Background in Computer Engineering. Personal interest in solving real world problems with data.''')
with col4:
    st.image("gallery/LI-Logo.png")
    st.caption(
        "[Connect with William](https://www.linkedin.com/in/williamf97/)")
    st.markdown('''Background in Business Analytics and Compliance Auditing. 
    Personal interest in ensuring that employers are compliant with Fair Work’s regulations.''')
