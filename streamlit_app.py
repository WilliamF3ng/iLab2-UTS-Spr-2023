# Goal to create a Streamlit web app that will allow the user to input in hours they've worked and produce a numerical
# payment amount that they can use to compare with their payslip to find underpayment.
# ---------------------------------------------------
# Experimental UI

# Ask the user if they are an employee or employer

# Ask the user which award they fall under:
# - Fast Food Industry Award (MA000003)
# - General Retail Industry Award (MA000004)
# - Hospitality Industry (General) Award (MA000009)

# Ask the user if they are FT, PT or Casual

import streamlit as st
# from googletrans import Translator

#def translate_text(text, target_lang):
#    translator = Translator()
#    translated_text = translator.translate(text, dest=target_lang)
#    return translated_text.text if translated_text is not None else text

def main():
    st.title("Know Your Wages (KYW)")

    # Google Translate toggle
    translate_lang = st.selectbox("Translate to: (Unfortunately need to use a Google Cloud API, new subscribers have $300 credits!)",
                                  ["English", "Chinese", "Hindi"])
    target_lang = "en"
    if translate_lang == "Chinese":
        target_lang = "zh-CN"
    elif translate_lang == "Hindi":
        target_lang = "hi"

    # Ask user if they are an employee or employer
    user_type = st.radio("Are you an employee or employer?", ("Employee", "Employer"))

    # Display pay award options with descriptions
    #st.subheader("Select Your Pay Award:")
    if user_type == "Employee":
        st.radio("Pay Award:", ("Fast Food Industry Award (MA000003) - Description...",
                                "General Retail Industry Award (MA000004) - Description...",
                                "Hospitality Industry (General) Award (MA000009) - Description..."))

    else:
        st.markdown("### Pay Award Descriptions:")
        st.write("Choose the relevant pay award for more information about each award.")
        if st.checkbox("Fast Food Industry Award (MA000003)"):
            st.write("Description for Fast Food Industry Award")
        if st.checkbox("General Retail Industry Award (MA000004)"):
            st.write("Description for General Retail Industry Award")
        if st.checkbox("Hospitality Industry (General) Award (MA000009)"):
            st.write("Description for Hospitality Industry Award")

    # Ask user about employment type
    employment_type = st.radio("Select Employment Type:", ("Full Time", "Part Time", "Casual"))

    # User input for hours worked
    hours_worked = st.number_input("Enter hours worked:", min_value=0.0, step=0.1)

    # Calculate pay
    base_pay_rate = 20  # random value
    overtime_rate = 1.5  # random value

    if hours_worked <= 38:
        total_pay = hours_worked * base_pay_rate
    else:
        overtime_hours = hours_worked - 38
        total_pay = (38 * base_pay_rate) + (overtime_hours * base_pay_rate * overtime_rate)

    st.subheader("Pay Details:")
    st.write(f"Hours Worked: {hours_worked} hours")
    st.write(f"Total Pay: ${total_pay:.2f}")

    st.write(f"According to your chosen award, you should've been paid ____ amount!")

    st.subheader("Next steps")
    st.write("If you have been underpaid, please speak to your employer or refer to the following links for more help.")
    st.write(f"Australian Fair Work Ombudsman - https://www.fairwork.gov.au/ or call 13 13 94, "
             f"open 8am to 5:30pm Monday to Friday, excluding public holidays.")
    st.write(f"For translation services and language assistance, call 13 14 50.")

if __name__ == "__main__":
    main()
