import streamlit as st
from streamlit_extras.app_logo import add_logo
add_logo("gallery/ResizeWW.png", height=100)

from PIL import Image
st.image("gallery/fwo.png", use_column_width=True)
st.header(":female-teacher: Helpful resources", divider="rainbow")

st.write('''
The Australian Fair Work Ombudsman maintains a large collection of helpful resources, designed to support both employees and employers. 

\n [Templates](https://www.fairwork.gov.au/tools-and-resources/templates)
- Includes both interactive and downloadable templates like letters to help you manage workplace obligations. Topics include employing and terminating staff, pay slips and recording keeping.

\n [Best Practice Guides](https://www.fairwork.gov.au/tools-and-resources/best-practice-guides)
- In-depth guides covering industry best practices, to help small businesses and employees handle workplace issues better.

\n [Fact Sheets](https://www.fairwork.gov.au/tools-and-resources/fact-sheets)
- Easy to understand fact sheets about Australian labour laws, employee rights and entitlements. 

\n [Calculators](https://calculate.fairwork.gov.au/)
- Additional tools to calculate pay, shift, annual leave, notice and redundancy. 

\n [Online Learning Centre with Videos](https://www.fairwork.gov.au/tools-and-resources/online-learning-centre)
- Interactive online courses and video tutorials covering a wide range of topics including how to have difficult conversations, record keeping and managing performance.

\n [Find My Award](https://services.fairwork.gov.au/find-my-award)
- Search tool to find your modern award, ensuring you understand your rights and entitlements, with detailed information on award conditions and provisions.

\n [Workplace Basics Quiz](https://services.fairwork.gov.au/workplace-basics)
- Fun and educational quizzes to test your knowledge of workplace rights, ethics, and regulations.

\n [Record My Hours App](https://www.fairwork.gov.au/tools-and-resources/record-my-hours-app)
- User-friendly app for accurately recording your work hours and breaks. Automated features to calculate overtime, ensuring you are compensated correctly for your time.

\n [Multi-language Translation](https://www.fairwork.gov.au/tools-and-resources/language-help)
- Fair Work Ombudsman website supports over 30 languages. 
- If you need to speak to someone in your own language, call the Translating and Interpreting Service on 131 450. Ask the operator to call Fair Work Ombudsman on 13 13 94.

''')