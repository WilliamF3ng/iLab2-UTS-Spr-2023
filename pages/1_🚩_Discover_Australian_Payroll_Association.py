import streamlit as st
from streamlit_extras.app_logo import add_logo
add_logo("gallery/ResizeWW.png", height=100)

from PIL import Image
image = Image.open("gallery/APA.png")
st.image(image, use_column_width=True)

st.header("Discover Australian Payroll Association", divider="rainbow")

st.markdown('''Welcome to the Australian Payroll Association – your go-to partner for payroll solutions in Australia! 
We're here to support payroll teams of all sizes across the country. 
Our goal is to make payroll management easier for everyone.
\n
\n **Our Mission**
\n At the Australian Payroll Association, we help payroll teams in Australia. We provide training and support to ensure that payroll is done correctly and helps employers effectively.
\n
\n **What We Offer**
\n
\n We offer training and classes for your payroll team. Whether you prefer in-person or online courses, we've got you covered. 
\n We also provide certification programs to enhance your team's skills. Our experts can assess your team's knowledge and help them improve.
\n 
\n **What's next?**
\n Join us at the Australian Payroll Association, where we simplify payroll management for everyone, including those who are learning English. Let's make payroll easier together!
''')

