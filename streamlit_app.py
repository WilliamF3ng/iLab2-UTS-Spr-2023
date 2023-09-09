# INSTALLING REQUIRED LIBRARIES

import streamlit as st # upgraded to 1.26.0 (released Aug 24th 2023)
import datetime
#from datetime import time, timedelta # new timedelta (updated 09/09/2023)
import pandas as pd
import requests

#from streamlit_lottie import st_lottie
from streamlit_extras.stoggle import stoggle

# Translation feature
from googletrans import Translator
translator = Translator()

# Download datasets from FWC website

# Update 09/09/2023 Solved constant reloading through st.cache
@st.cache_data
def download_and_process_excel(url, categories, year):
    full_url = f"{url}-{year}.xlsx"
    response = requests.get(full_url)

    if response.status_code == 200:
        file_name = f"map_{categories}_export_{year}.xlsx"
        with open(file_name, "wb") as file:
            file.write(response.content)

        df = pd.read_excel(file_name)
        return df
    else:
        st.error(f"Failed to download the file for {categories} - {year}")
        return None

# MAIN CODE

def main():
    st.title(":money_with_wings:  Know Your Wages (KYW)")

    # Based on top international student countries supported languages are:
    # English, Chinese, Hindi, Arabic, Indonesian, Nepali, Portuguese, Spanish, Thai, Urdu, Vietnamese.

    # Supported languages are: :flag-cn: :flag-in: have all countries but which country is for Arabic? the Arab league flag?
    translate_lang = st.selectbox(" :globe_with_meridians: "
                                  "Currently supporting 10 languages. Choose your language: ",
                                  ["English", "简体中文", "हिंदी", "العربية", "Bahasa Indonesia",
                                   "नेपाली", "Português", "Español", "ภาษาไทย","اردو " , "Tiếng Việt"])
    # Default language English
    target_lang = "en"

    if translate_lang == "简体中文":
        target_lang = "zh-CN"
    elif translate_lang == "हिंदी":
        target_lang = "hi"
    elif translate_lang == "العربية":
        target_lang = "ar"
    elif translate_lang == "Bahasa Indonesia":
        target_lang = "id"
    elif translate_lang == "नेपाली":
        target_lang = "ne"
    elif translate_lang == "Português":
        target_lang = "pt"
    elif translate_lang == "Español":
        target_lang = "es"
    elif translate_lang == "ภาษาไทย":
        target_lang = "th"
    elif translate_lang == "اردو":
        target_lang = "ur"
    elif translate_lang == "Tiếng Việt":
        target_lang = "vi"

    download_classification = "https://www.fwc.gov.au/documents/awards/pay-database/map-classification-export"
    categories_classification = "classification"

    download_penalty = "https://www.fwc.gov.au/documents/awards/pay-database/map-penalty-export"
    categories_penalty = "penalty"

    year = datetime.datetime.now().year

    st.header("Your details", divider="rainbow")

    user_type = st.radio(translator.translate("Are you an Employee or Employer?",dest=target_lang).text,
                         ("Employee", "Employer"),
                         captions=("Also known as a worker", "Also known as a boss"))
    if user_type == "Employee":
        awards = ["MA000003", "MA000004", "MA000009"]
        selected_award = st.radio(translator.translate("What's your pay award?", dest=target_lang).text, awards,
                                  captions=("Fast Food Industry Award",
                                            "General Retail Industry Award",
                                            "Hospitality Industry (General) Award"))

        if selected_award == "MA000003":
            st.write(translator.translate("This pay award covers employers and employees working in the fast food industry like: "
                     "employees taking orders, including via an app, cooking and selling fast food, "
                     "baristas, delivery drivers, and supervisors.", dest=target_lang).text)

        elif selected_award == "MA000004":
            st.write(translator.translate("This award covers employers and employees working in the general retail industry like: "
                     "check-out operators, sales assistants, stock hands, shelf stackers, salespersons, store managers,"
                     "tradespersons (butchers, bakers, florists) and travel agencies.", dest=target_lang).text)

        elif selected_award == "MA000009":
            st.write(translator.translate("This award covers employers and employees working in the hospitality industry like: "
                                          "waiters/waitresses, kitchen hands, cooks/chefs, housekeepers, concierge/reception staff"
                                          "gaming attendants, security officers, casino staff, catering staff and pub owners.",dest=target_lang).text)

        # Download and process the dataset
        df = download_and_process_excel(download_classification, categories_classification, year) # classification data
        df_penalty = download_and_process_excel(download_penalty, categories_penalty, year) # penalty rates data

        if df is not None:
            st.success(translator.translate("Ready for use.", dest=target_lang).text, icon = "✅")

            # Filter the dataset by the user's selected award
            filtered_df = df[df["awardCode"] == selected_award]
            filtered_df_penalty = df_penalty[df_penalty["awardCode"] == selected_award]

            # Ask user about employment type
            employment_type = st.radio(translator.translate("What's your Employment Type?",dest=target_lang).text,
                                       ("Full Time", "Part Time", "Casual"),
                                       captions=("Average 38 hours per week",
                                                 "Less than 38 hours per work, but hours are regular",
                                                 "No agreed pattern of work"))

            # What if you filter the dataset by parentClassification and then ask the user to select their classification
            filtered_df = filtered_df[(filtered_df["employeeRateTypeCode"] == "AD") | (filtered_df["employeeRateTypeCode"] == "JN")]
            filtered_df_penalty = filtered_df_penalty[(filtered_df_penalty["employeeRateTypeCode"] == "AD") | (filtered_df_penalty["employeeRateTypeCode"] == "JN")]

            # Data file contains weird values For penalty table I.5.2 and For penalty table I.5.3
            filtered_df = filtered_df[
                ~filtered_df["clauseDescription"].isin(["For penalty table I.5.3", "For penalty table I.5.2"])]

            unique_clauseDescription = filtered_df["clauseDescription"].unique()
            user_clauseDescription = st.selectbox(translator.translate("Choose the best job description from the options below: ",
                                                                       dest=target_lang).text, unique_clauseDescription)

            filtered_df = filtered_df[filtered_df["clauseDescription"] == user_clauseDescription]

            # Data contains weird values,
            filtered_df = filtered_df[
                ~filtered_df["classification"].isin(["Retail Employee Level 2*", "Retail Employee Level 3*"])]

            unique_classification = filtered_df["classification"].unique()
            user_classification = st.selectbox(translator.translate("Choose your classification: ",
                                                                    dest=target_lang).text, unique_classification)

            filtered_df = filtered_df[filtered_df["classification"] == user_classification]
            filtered_df_penalty = filtered_df_penalty[filtered_df_penalty["classification"] == user_classification]

            employment_level = None
            # If user selected junior rate, ask for their employee level
            unique_level = filtered_df["parentClassificationName"].unique()
            if "junior" in user_clauseDescription.lower():
                employment_level = st.selectbox(translator.translate("Choose your employment level: ", dest=target_lang).text,
                                                    unique_level)
            else:
                pass

            if employment_level is not None:
                filtered_df = filtered_df[filtered_df["parentClassificationName"] == employment_level]
                filtered_df_penalty = filtered_df_penalty[filtered_df_penalty["parentClassificationName"] == employment_level]

            if employment_type == "Casual":
                filtered_df_penalty = filtered_df_penalty[
                    filtered_df_penalty["clauseDescription"].str.contains("casual", case=False)]
            else:
                filtered_df_penalty = filtered_df_penalty[
                    ~filtered_df_penalty["clauseDescription"].str.contains("casual", case=False)]

            # Making some large assumptions like excluding baking employees in 004 due to odd start hours
            filtered_df_penalty = filtered_df_penalty[~filtered_df_penalty["penaltyDescription"].
            str.contains("Early morning shifts", case=False)]

            # DISPLAY THE PAY RATES BELOW

            # Select only the relevant columns
            selected_col_classification = ["baseRate", "baseRateType"] # add penalty rate calculations to this table too
            selected_data_class = filtered_df[selected_col_classification]

            selected_col_penalty = ["clauseDescription","penaltyDescription","rate","penaltyCalculatedValue"]
            selected_data_penalty = filtered_df_penalty[selected_col_penalty]

            st.header("Your pay rates", divider="rainbow")

            # Store the user selections in separate lists - IDEA TO GIVE A USER SUMMARY, BUT NOT WORKING YET
            # user_selected_type = []
            # user_selected_award = []
            # user_selected_employment = []
            # user_selected_employment_level = []
            #
            # user_selected_type = ", ".join(user_type)
            #
            # st.subheader("What you've told us")
            #
            # st.write("User Type:", ", ".join(user_selected_type))
            # st.write("Employment Types:", user_selected_employment_level)

            st.data_editor(selected_data_class,
                           column_config={
                               "baseRate": "Base Rate",
                               "baseRateType": "Frequency",
                           },
                           hide_index=True)

            st.data_editor(selected_data_penalty,
                           column_config={
                               "clauseDescription": "Category",
                               "penaltyDescription": "Eligible Entitlements",
                               "rate": "Wage Multipliers",
                               "penaltyCalculatedValue": "Penalty Amount"
                           },
                           hide_index=True)

        else:
            st.error("Oops something went wrong. Please retry again later.", icon="❌")

    # START OF THE HOURS INPUT MODULE

    # Update 09/09/2023, CHANGE TO FORM LAYOUT TO PREVENT CONSTANT LOADING, WITH SUBMIT BUTTON

        st.header("Your hours", divider="rainbow")
        # Create a Streamlit form
        with st.form("hour_entry_form"):

            days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day_data = {day: {"hours_worked": 0.0, "break_taken": False, "is_public_holiday": False} for day in
                        days_of_week}

            for index, day in enumerate(days_of_week):
                col1, col2 = st.columns(2)

                with col1:
                    hours = st.number_input(f"Enter hours worked on {day}:", min_value=0.0, step=0.1)
                    day_data[day]["hours_worked"] = round(hours, 1)

                with col2:
                    day_data[day]["break_taken"] = st.checkbox(f"Break taken on {day}")
                    day_data[day]["is_public_holiday"] = st.checkbox(f"Public holiday on {day}")

                    if index < len(days_of_week) - 1:
                        st.markdown("---")

            submitted = st.form_submit_button("Submit")

        # Check if the form was submitted
        if submitted:
            st.subheader("Summary")
            hours_df = pd.DataFrame(day_data).T

            column_mapping = {
                "hours_worked": "Hours Worked",
                "break_taken": "Was a break taken?",
                "is_public_holiday": "Was it a public holiday?"
            }
            boolean_mapping = {True: "Yes", False: "No"}
            columns_to_map = ["break_taken", "is_public_holiday"]

            hours_df[columns_to_map] = hours_df[columns_to_map].applymap(lambda x: boolean_mapping.get(x, x))
            hours_df["hours_worked"] = hours_df["hours_worked"].apply(lambda x: round(x, 1))

            styled_df = hours_df.rename(columns=column_mapping).style.set_table_styles([{
                'selector': 'table',
                'props': [('user-select', 'none')]
            }]).set_properties(**{'text-align': 'center'})
            st.table(styled_df)

        # START OF THE CALCULATION MODULE
        st.header("This is your pay", divider="rainbow")
        
        # Extract public holiday rates from the penalty dataset
        public_holiday_rates = filtered_df_penalty[
            (filtered_df_penalty["penaltyDescription"].str.contains("public holiday", case=False)) &
            (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

        # Define the default rates (non-public holiday rates)
        default_rate = filtered_df_penalty[
            (filtered_df_penalty["penaltyDescription"].str.contains("ordinary hours", case=False)) &
            (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

        # Weekend penalty rates
        saturday_rate = filtered_df_penalty[
            (filtered_df_penalty["clauseDescription"].str.contains("ordinary and penalty rates", case=False))&
            (filtered_df_penalty["penaltyDescription"].str.contains("saturday", case=False))&
            (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

        sunday_rate = filtered_df_penalty[
            (filtered_df_penalty["clauseDescription"].str.contains("ordinary and penalty rates", case=False))&
            (filtered_df_penalty["penaltyDescription"].str.contains("sunday", case=False))&
            (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

        total_pay = 0.0
        #total_hours_worked = 0.0  # Initialize total hours worked to 0
        days_with_breaks = []

        for day, data in day_data.items():
            hours_worked = data["hours_worked"]
            is_public_holiday = data["is_public_holiday"]
            break_taken = data["break_taken"]  # Add break_taken information from the data

            if break_taken:
                hours_worked -= 0.5  # Deduct 0.5 hours if a break was taken
                days_with_breaks.append(day)

            if is_public_holiday:
                total_pay += hours_worked * public_holiday_rates
            elif day == "Saturday":
                total_pay += hours_worked * saturday_rate
            elif day == "Sunday":
                total_pay += hours_worked * sunday_rate
            else:
                total_pay += hours_worked * default_rate

        # Calculate the total hours worked after considering breaks
        total_hours_worked = sum([day["hours_worked"] for day in day_data.values()])
        if any(day["break_taken"] for day in day_data.values()):
           total_hours_worked -= 0.5  # 30 minutes for lunch usually

        st.subheader(f"Total Hours Worked: {total_hours_worked:.1f} hours")

        # Display a message for days with breaks
        if days_with_breaks:
            st.write(f"On {', '.join(days_with_breaks)}, you took a break.")

        st.write(
            "Your total pay is $ {:.2f}. If you think this is wrong, please look at the Next Steps below".format(total_pay))
        stoggle(
            "Show calculations",
            """Total Pay = (Ordinary Rate x Hours Worked) + (Penalty Rates x Hours Worked for Sat/Sun/Public Holiday) + (Overtime rates x Hours overtime)""")

        # Add a "Show Calculation" dropdown
        # show_calculation = st.selectbox("Show Calculation", ["Simplified Equation", "Detailed Calculation"])
        #
        # if show_calculation == "Simplified Equation":
        #     st.subheader("Simplified Calculation:")
        #     st.write(
        #         f"Total Pay = (Ordinary Rate x Hours Worked) + (Penalty Rates x Hours Worked for Sat/Sun/Public Holiday)")
        # else:
        #     st.subheader("Detailed Calculation:")
        #     st.write(f"Total Pay = ({default_rate} x Hours Worked for Mon-Fri) + "
        #              f"({saturday_rate} x Hours Worked for Saturday) + "
        #              f"({sunday_rate} x Hours Worked for Sunday) + "
        #              f"({public_holiday_rates} x Hours Worked for Public Holidays)")
            if is_public_holiday:
              total_pay += hours_worked * public_holiday_rates
            else:
              total_pay += hours_worked * default_rate
              
        st.write("According to your chosen award and classification level, your total pay is $ {:.2f}.".format(total_pay))

        # END OF CALCULATOR MODULE

    else:
        st.header("Pay Award Descriptions", divider="rainbow")
        employer_selected = st.radio("Choose the relevant pay award for more information.",
                 ("Fast Food Industry Award (MA000003)",
                 "General Retail Industry Award (MA000004)",
                 "Hospitality Industry (General) Award (MA000009)"))

        if employer_selected == "Fast Food Industry Award (MA000003)":
            st.write("This award covers employers and employees working in the fast food industry like: "
             "employees taking orders, including via an app, cooking and selling fast food, "
             "baristas, delivery drivers, supervisors of these duties and cafes. "
             "For more info, visit https://www.fairwork.gov.au/employment-conditions/awards/awards-summary/ma000003-summary")

        if employer_selected == "General Retail Industry Award (MA000004)":
            st.write("This award covers employers and employees working in the general retail industry like: "
             "check-out operators, sales assistants, stock hands, shelf stackers, salespersons, store managers,"
             "tradespersons (butchers, bakers, florists) and travel agencies. "
             "For more info, visit https://www.fairwork.gov.au/employment-conditions/awards/awards-summary/ma000004-summary")

        if employer_selected == "Hospitality Industry (General) Award (MA000009)":
            st.write("This award covers employers and employees working in the hospitality industry like: "
             "waiters/waitresses, kitchen hands, cooks/chefs, housekeepers, concierge/reception staff"
             "gaming attendants, security officers, casino staff, catering staff and pub owners. "
             "For more info, visit https://www.fairwork.gov.au/employment-conditions/awards/awards-summary/ma000009-summary")

    # USEFUL INFORMATION

    if user_type == "Employee":
        st.header("Your next steps", divider="rainbow")
        st.write("If you have been underpaid, please speak to your employer or refer to the following links for more help.")
        st.write(f"Australian Fair Work Ombudsman, visit https://www.fairwork.gov.au/ or call 13 13 94 :telephone: , "
             f"open 8am to 5:30pm Monday to Friday, excluding public holidays.")
        st.write(f":earth_asia: For translation services and language assistance, call 13 14 50.")
    else:
        st.header("Employer Resources", divider="rainbow")
        st.write('''Please refer to the following links:
        \n Fair Work Ombudsman Definitions - https://www.fairwork.gov.au/dictionary
        \n Fair Work Ombudsman Online Learning Centre - https://www.fairwork.gov.au/tools-and-resources/online-learning-centre
        \n Fair Work Ombudsman Downloaded Templates - https://www.fairwork.gov.au/tools-and-resources/templates
        \n Need more help? - https://services.fairwork.gov.au/get-help
        ''')

    # DISCLAIMER SECTION

    st.header(":red[DISCLAIMER]", divider="rainbow")
    st.markdown('''This Pay Calculator is an :orange[unofficial] tool.
    It's only for information, not exact pay. It might have mistakes.
    \n Please use the official Australian Fair Work Ombudsman's guidelines for correct pay rates and rules.
    This calculator can't replace professional help. If you rely on it, it's your risk.
    \nThe people who made this are not responsible for mistakes. Check its results with official sources.
    Get legal or professional help if needed.
    \n If you use this Pay Calculator, you know it's :orange[unofficial].
    You're responsible for what you do with its results.''')

    # CLOSING NOTES

    st.header("Creators note", divider="rainbow")
    st.markdown('''
    :rainbow[Created and designed by the Wage Warriors for UTS iLab2 Spring 2023 in association with the Australian Payroll Association.
    Data obtained from the Fair Work Commission and Fair Work Ombudsman websites.]
    ''')

if __name__ == "__main__":
    main()
