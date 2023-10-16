import streamlit as st
from PIL import Image

from streamlit_extras.app_logo import add_logo
add_logo("gallery/ResizeWW.png", height=100)

st.header("Unfair pay is everywhere!", divider="rainbow")

st.markdown('''
Minimum wage establishes a baseline income for workers of any industry in a given jurisdiction. The idea behind minimum wage is to ensure that one’s basic needs, such as food, housing, and a certain number of bills, are met. However, this may not always be the case.

Generally, developed countries tend to have a higher cost of living and require a minimum wage sufficient for that. As economies around the world succumbed to inflation, this formula was invalid for countries like Argentina and Turkey. However, since 2001, Australia has established itself at the forefront of countries that do pay a significantly high minimum wage.
''')

min_wageOT = Image.open("gallery/australia_minimum_wage.png")
st.image(min_wageOT, caption="Australia's minimum wage rate overtime")

st.markdown('''
While leading economies like America have firmly stuck with its \\$7.25 USD per hour rate, this has not been the case with Australia. From AUD \\$18.99 per hour in 2001 to AUD \\$21.54 per hour as of 2022, Australia is revealed to have the second-highest minimum wage in the world, falling just shy of Luxembourg.
''')

wage_treemap = Image.open("gallery/treemap.png")
st.image(wage_treemap, caption="Minimum wage per hour in USD across the world")

st.markdown('''
A high minimum wage ensures positive impacts in all of society by working to reduce income inequality and improving one’s standard of living. However, growing instances of worker underpayments have left several sectors at risk. Healthcare, social assistance, retail, and fast food service employees are often dragged into an unsavoury and difficult process and often do not have the right resources or means to defend themselves.

As of February 2023, estimates suggest Australians are collectively underpaid a shocking \\$1.35 billion yearly. The Fair Work Ombudsman has recovered \\$532 million in unpaid wages and entitlements for workers in 2021/22, a record sum of money that could’ve been crucial to an employee’s wellbeing. Ultimately, the prevalence of underpayment highlights the urgency of addressing wage theft so that employees are not left vulnerable and rightfully receive what they deserve.

Underpayment acts as a deterrent for a prospering economy. If you or anyone you know is being underpaid, talk to your payroll manager (or appropriate person in charge) to correct the situation. In case of escalations, reach out to Fair Work Ombudsman to help equip you with the right resources to help resolve the issue.
''')
