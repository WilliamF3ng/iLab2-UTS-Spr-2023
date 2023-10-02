import streamlit as st
import bcrypt
import datetime
import pandas as pd
import requests
from googletrans import Translator

translator = Translator()

# Exact same app code below
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

def main():
    st.title(":money_with_wings:  Know Your Wages (KYW)")

    # Based on top international student countries supported languages are:
    # English, Chinese, Hindi, Arabic, Indonesian, Nepali, Portuguese, Spanish, Thai, Urdu, Vietnamese.
    translate_lang = st.selectbox(" :globe_with_meridians: "
                                  "Currently supporting 10 languages. Choose your language: ",
                                  ["English", "简体中文", "हिंदी", "العربية", "Bahasa Indonesia",
                                   "नेपाली", "Português", "Español", "ภาษาไทย", "اردو ", "Tiếng Việt"])
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

    user_type = st.radio(translator.translate("Are you an Employee or Employer?", dest=target_lang).text,
                         ("Employee", "Employer"),
                         captions=("Also known as a worker", "Also known as a boss"))
    if user_type == "Employee":
        awards = ["MA000003", "MA000004", "MA000009"]
        selected_award = st.radio(translator.translate("What's your pay award?", dest=target_lang).text,
                                  awards,
                                  captions=("Fast Food Industry Award",
                                            "General Retail Industry Award",
                                            "Hospitality Industry (General) Award"))

        if selected_award == "MA000003":
            st.write(translator.translate(
                "This pay award covers employers and employees working in the fast food industry. "
                "Including jobs such as taking orders (including via an app), cooking and selling fast food, baristas, "
                "delivery drivers and supervisors. ", dest=target_lang).text)

        elif selected_award == "MA000004":
            st.write(translator.translate(
                "This pay award covers employers and employees working in the general retail industry. "
                "Including jobs such as check-out operators, sales assistants, stock hands, shelf stackers, salespersons, "
                "store managers, tradespersons (butchers, bakers, florists) and travel agents.",
                dest=target_lang).text)

        elif selected_award == "MA000009":
            st.write(translator.translate(
                "This pay award covers employers and employees working in the hospitality industry. "
                "Including jobs such as waiters/waitresses, kitchen hands, cooks/chefs, housekeepers, concierge/reception staff, "
                "gaming attendants, security officers, casino staff, catering staff and pub owners.",
                dest=target_lang).text)

        # Download and process the dataset
        df = download_and_process_excel(download_classification, categories_classification,
                                        year)  # classification data
        df_penalty = download_and_process_excel(download_penalty, categories_penalty,
                                                year)  # penalty rates data

        if df is not None:
            st.success(translator.translate("Ready for use.", dest=target_lang).text, icon="✅")

            # Filter the dataset by the user's selected award
            filtered_df = df[df["awardCode"] == selected_award]
            filtered_df_penalty = df_penalty[df_penalty["awardCode"] == selected_award]

            # Ask user about employment type
            employment_type = st.radio(
                translator.translate("What's your Employment Type?", dest=target_lang).text,
                ("Full Time", "Part Time", "Casual"),
                captions=("Average 38 hours per week",
                          "Less than 38 hours per work, but hours are regular",
                          "No agreed pattern of work"))

            # Filter the dataset by parentClassification and then ask the user to select their classification
            filtered_df = filtered_df[
                (filtered_df["employeeRateTypeCode"] == "AD") | (
                        filtered_df["employeeRateTypeCode"] == "JN")]
            filtered_df_penalty = filtered_df_penalty[
                (filtered_df_penalty["employeeRateTypeCode"] == "AD") | (
                        filtered_df_penalty["employeeRateTypeCode"] == "JN")]

            # DUE TO ISSUES AROUND CASINO OVERTIME RATES, INTERIM TO EXCLUDE CASINO WORKERS
            filtered_df = filtered_df[~filtered_df["clauseDescription"].isin(["Casino Gaming Employees"])]

            # Data file contains weird values For penalty table I.5.2 and For penalty table I.5.3
            filtered_df = filtered_df[
                ~filtered_df["clauseDescription"].isin(
                    ["For penalty table I.5.3", "For penalty table I.5.2"])]

            unique_clauseDescription = filtered_df["clauseDescription"].unique()
            user_clauseDescription = st.selectbox(
                translator.translate("Choose the best job description from the options below: ",
                                     dest=target_lang).text, unique_clauseDescription)

            filtered_df = filtered_df[filtered_df["clauseDescription"] == user_clauseDescription]

            # Data contains weird values,
            filtered_df = filtered_df[
                ~filtered_df["classification"].isin(
                    ["Retail Employee Level 2*", "Retail Employee Level 3*"])]

            unique_classification = filtered_df["classification"].unique()
            user_classification = st.selectbox(translator.translate("Choose your classification: ",
                                                                    dest=target_lang).text,
                                               unique_classification)
            st.caption(
                "Don't know your classification level? [Click here!](https://www.fairwork.gov.au/employment-conditions/awards/award-classifications)")

            filtered_df = filtered_df[filtered_df["classification"] == user_classification]
            filtered_df_penalty = filtered_df_penalty[
                filtered_df_penalty["classification"] == user_classification]

            employment_level = None
            # If user selected junior rate, ask for their employee level
            unique_level = filtered_df["parentClassificationName"].unique()
            if "junior" in user_clauseDescription.lower():
                employment_level = st.selectbox(
                    translator.translate("Choose your employment level: ", dest=target_lang).text,
                    unique_level)
            else:
                pass

            if employment_level is not None:
                filtered_df = filtered_df[filtered_df["parentClassificationName"] == employment_level]
                filtered_df_penalty = filtered_df_penalty[
                    filtered_df_penalty["parentClassificationName"] == employment_level]

            if employment_type == "Casual":
                filtered_df_penalty = filtered_df_penalty[
                    filtered_df_penalty["clauseDescription"].str.contains("casual", case=False)]
            else:
                filtered_df_penalty = filtered_df_penalty[
                    ~filtered_df_penalty["clauseDescription"].str.contains("casual", case=False)]

            # Removed baking employees
            filtered_df_penalty = filtered_df_penalty[~(filtered_df_penalty["penaltyDescription"]
                                                        .str.contains("Early morning shifts",
                                                                      case=False) == True)]

            # CONTINUED INTERIM REMOVAL OF CASINO GAMING EMPLOYEE
            filtered_df_penalty = filtered_df_penalty[~(filtered_df_penalty["clauseDescription"]
                                                        .str.contains("casino gaming employees",
                                                                      case=False) == True)]

            # DISPLAY THE PAY RATES BELOW

            # Select only the relevant columns
            selected_col_classification = ["baseRate", "baseRateType"]
            selected_data_class = filtered_df[selected_col_classification]

            selected_col_penalty = ["clauseDescription", "penaltyDescription", "rate",
                                    "penaltyCalculatedValue"]
            selected_data_penalty = filtered_df_penalty[selected_col_penalty]

            st.header("Your pay rates", divider="rainbow")

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
            st.error(
                translator.translate("Oops something went wrong. Please retry again later.",
                                     dest=target_lang).text,
                icon="❌")

        # START OF THE HOURS INPUT MODULE

        st.header("Your hours", divider="rainbow")

        # Experiment using tabs

        standard_hours, clock_hours = st.tabs(["Standard Input", "Clock in/out Input"])

        with standard_hours:
            with st.form("hour_entry_form"):
                days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                day_data = {day: {"hours_worked": 0.0, "is_evening_shift": False, "is_overtime": False,
                                  "is_public_holiday": False} for day in
                            days_of_week}

                for index, day in enumerate(days_of_week):
                    col1, col2 = st.columns(2)

                    with col1:
                        hours = st.number_input(f"Enter hours worked on {day}, excluding breaks:",
                                                min_value=0.0, max_value=24.0, step=0.1)
                        day_data[day]["hours_worked"] = round(hours, 1)

                    with col2:
                        day_data[day]["is_evening_shift"] = st.checkbox(f"Evening shift on {day}",
                                                                        help="Tick if your shift started or ended after 6pm")
                        day_data[day]["is_public_holiday"] = st.checkbox(f"Public holiday on {day}")

                        if index < len(days_of_week) - 1:
                            st.markdown("---")

                # Superannuation slider
                superannuation_rate = st.slider("Superannuation rate", min_value=11.0, max_value=15.0,
                                                value=11.0, step=0.5,
                                                format="%f%%")

                submitted = st.form_submit_button("Calculate", use_container_width=True)

            # Check if the form was submitted
            if submitted:
                st.success(translator.translate("We've done the maths for you.", dest=target_lang).text,
                           icon="✅")

                # START OF THE CALCULATION MODULE
                st.header("This is your pay", divider="rainbow")

                public_holiday_rates = filtered_df_penalty[
                    (filtered_df_penalty["penaltyDescription"].str.contains("public holiday", case=False)) &
                    (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

                # Define the default rates (non-public holiday rates)
                ordinary_rate = filtered_df_penalty[
                    (filtered_df_penalty["penaltyDescription"].str.contains("ordinary hours", case=False)) &
                    (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

                # Weekend penalty rates
                saturday_rate = filtered_df_penalty[
                    (filtered_df_penalty["clauseDescription"].str.contains("ordinary and penalty rates",
                                                                           case=False)) &
                    (filtered_df_penalty["penaltyDescription"].str.contains("saturday", case=False)) &
                    (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

                sunday_rate = filtered_df_penalty[
                    (filtered_df_penalty["clauseDescription"].str.contains("ordinary and penalty rates",
                                                                           case=False)) &
                    (filtered_df_penalty["penaltyDescription"].str.contains("sunday", case=False)) &
                    (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

                overtime_first_x_hrs = filtered_df_penalty[
                    (filtered_df_penalty["clauseDescription"].str.contains("overtime rates", case=False)) &
                    (filtered_df_penalty["penaltyDescription"].str.contains("first", case=False)) &
                    (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

                overtime_after_x_hrs = filtered_df_penalty[
                    (filtered_df_penalty["clauseDescription"].str.contains("overtime rates", case=False)) &
                    (filtered_df_penalty["penaltyDescription"].str.contains("after", case=False)) &
                    (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

                overtime_sunday_and_hospo_weekends = filtered_df_penalty[
                    (filtered_df_penalty["clauseDescription"].str.contains("overtime rates", case=False)) &
                    ((filtered_df_penalty["penaltyDescription"].str.contains("sunday", case=False)) |
                     (filtered_df_penalty["penaltyDescription"].str.contains("weekends", case=False))) &
                    (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

                overtime_public_holiday = filtered_df_penalty[
                    (filtered_df_penalty["clauseDescription"].str.contains("overtime rates", case=False)) &
                    (filtered_df_penalty["penaltyDescription"].str.contains("public holiday", case=False)) &
                    (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

                total_pay = 0.0
                days_with_evening_shifts = []
                days_with_more_4hs = []

                table_data = {"Day": [], "Hours Worked": [], "Evening Shift": [], "Overtime": [],
                              "Rate Description": [],
                              "Rate": [], "Pay": []}

                # Using a rolling total hours instead
                rolling_total_hours_worked = 0.0

                for day, data in day_data.items():
                    hours_worked = data["hours_worked"]
                    is_public_holiday = data["is_public_holiday"]
                    is_evening_shift = data["is_evening_shift"]

                    rolling_total_hours_worked += hours_worked

                    if is_evening_shift:
                        days_with_evening_shifts.append(day)

                    if hours_worked >= 4:
                        days_with_more_4hs.append(day)

                    if hours_worked > 11 or rolling_total_hours_worked > 38:
                        is_overtime = "Yes"
                        if selected_award == "MA000003":
                            if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
                                if hours_worked <= 2:
                                    rate = overtime_first_x_hrs
                                    rate_description = "Overtime First 2 Hours"
                                elif hours_worked > 2:
                                    rate = overtime_after_x_hrs
                                    rate_description = "Overtime After 2 Hours"
                                if is_public_holiday:
                                    rate = overtime_public_holiday
                                    rate_description = "Overtime PH"
                            elif day == "Sunday":
                                if is_public_holiday:
                                    rate = overtime_public_holiday
                                    rate_description = "Overtime PH"
                                else:
                                    rate = overtime_sunday_and_hospo_weekends
                                    rate_description = "Overtime Sunday"
                        elif selected_award == "MA000004":
                            if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
                                if hours_worked <= 3:
                                    rate = overtime_first_x_hrs
                                    rate_description = "Overtime First 3 Hours"
                                elif hours_worked > 3:
                                    rate = overtime_after_x_hrs
                                    rate_description = "Overtime After 3 Hours"
                                if is_public_holiday:
                                    rate = overtime_public_holiday
                                    rate_description = "Overtime PH"
                        elif selected_award == "MA000009":
                            if day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                                if hours_worked <= 2:
                                    rate = overtime_first_x_hrs
                                    rate_description = "Overtime First 2 Hours"
                                elif hours_worked > 2:
                                    rate = overtime_after_x_hrs
                                    rate_description = "Overtime After 2 Hours"
                                if is_public_holiday:
                                    rate = overtime_public_holiday
                                    rate_description = "Overtime PH"
                            elif day in ["Saturday", "Sunday"]:
                                if is_public_holiday:
                                    rate = overtime_public_holiday
                                    rate_description = "Overtime PH"
                                else:
                                    rate = overtime_sunday_and_hospo_weekends
                                    rate_description = "Overtime Sunday"
                    else:
                        is_overtime = "No"
                        if selected_award in ["MA000003", "MA000004", "MA000009"]:
                            if is_public_holiday:
                                rate = public_holiday_rates
                                rate_description = "Penalty PH Rate"
                            elif day == "Saturday":
                                rate = saturday_rate
                                rate_description = "Penalty Saturday Rate"
                            elif day == "Sunday":
                                rate = sunday_rate
                                rate_description = "Penalty Sunday Rate"
                            else:
                                rate = ordinary_rate
                                rate_description = "Ordinary Rate"

                    # Calculate pay for this day
                    day_pay = hours_worked * rate

                    # Append data to the table_data dictionary
                    table_data["Day"].append(day)
                    table_data["Hours Worked"].append(f"{hours_worked:.1f} hours")
                    table_data["Evening Shift"].append("Yes" if is_evening_shift else "No")
                    table_data["Overtime"].append(is_overtime)
                    table_data["Rate Description"].append(rate_description)
                    table_data["Rate"].append(f"${rate:.2f}")
                    table_data["Pay"].append(f"${day_pay:.2f}")

                    total_pay += day_pay

                total_hours_worked = rolling_total_hours_worked

                is_under_18 = user_classification.lower().strip() in [
                    "under 16 years",
                    "16 years",
                    "17 years",
                    "15 years of age and under",
                    "16 years of age",
                    "17 years of age",
                    "16 years of age and under"
                ]
                if is_under_18 and total_hours_worked < 30:
                    superannuation_per_week = 0.00
                else:
                    superannuation_per_week = (total_pay * superannuation_rate) / 100

                st.write(
                    f"You have worked {total_hours_worked:.1f} hours! Your total gross pay is ${total_pay:.2f}.")
                st.caption(
                    ":bulb: Gross pay is the total amount of money you earn before taxes or deductions are removed.",
                    help="Your employer may deduct taxes if you've provided your Australian Tax File Number.")
                st.write(f"Your superannuation this week is ${superannuation_per_week:.2f}. "
                         f"If you think this is :red[wrong], please double check you've entered the correct hours above or look at the Next Steps below.")

                if days_with_more_4hs:
                    st.write(
                        f"- :hamburger: On {', '.join(days_with_more_4hs)}, you should've been allowed to take a lunch break. "
                        "Usually this break can be between 30 minutes to 1 hour depending on your shift and your employer.")

                if days_with_evening_shifts:
                    st.write(
                        f"- :crescent_moon: On {', '.join(days_with_evening_shifts)}, you worked evening shift(s). You may be entitled to additional pay.")
                if selected_award == "MA000003":
                    st.write(
                        "Your evening rate is 110% of your ordinary pay from Monday to Friday 10pm to midnight OR 115% from midnight to 6am.")
                elif selected_award == "MA000004":
                    st.write(
                        "Your evening rate is 125% of your ordinary pay from Monday to Friday after 6pm.")
                else:
                    st.write(
                        "Your evening rate is \$ 2.62 per hr extra from 7pm to midnight OR $ 3.93 per hr from midnight to 7am.")

                # Breakdown table
                breakdown_df = pd.DataFrame(table_data)
                with st.expander("Show hours calculation"):
                    styled_df = st.data_editor(breakdown_df, hide_index=True)

        # END OF CALCULATOR MODULE

        with clock_hours:
            with st.form("clock_hours_form"):
                clock_day_data = {day: {"start_time": None, "end_time": None, "is_evening_shift": None, "is_public_holiday": False} for day in days_of_week}

                for index, day in enumerate(days_of_week):
                    clock_col1, clock_col2, clock_col3 = st.columns(3)

                    with clock_col1:
                        start_time = st.time_input(f"Enter start time on {day}: ", value=None)
                        clock_day_data[day]["start_time"] = start_time

                    with clock_col2:
                        end_time = st.time_input(f"Enter end time on {day}: ", value=None)
                        clock_day_data[day]["end_time"] = end_time

                    with clock_col3:
                        day_data[day]["is_evening_shift"] = st.checkbox(f"Evening shift on {day}",
                                                                        help="Tick if your shift started or ended after 6pm")
                        day_data[day]["is_public_holiday"] = st.checkbox(f"Public holiday on {day}")

                        if index < len(days_of_week) - 1:
                            st.markdown("---")

                clock_submitted = st.form_submit_button("Calculate", use_container_width=True)

            if clock_submitted:
                st.success(translator.translate("We've done the maths for you.", dest=target_lang).text, icon="✅")




    else:
        st.header("Pay Award Descriptions", divider="rainbow")
        employer_selected = st.radio("Choose the relevant pay award for more information.",
                                     ("Fast Food Industry Award (MA000003)",
                                      "General Retail Industry Award (MA000004)",
                                      "Hospitality Industry (General) Award (MA000009)"))

        if employer_selected == "Fast Food Industry Award (MA000003)":
            st.write("This pay award covers employers and employees working in the fast food industry. "
                     "Including jobs such as taking orders (including via an app), cooking and selling fast food, baristas, delivery drivers and supervisors.  "
                     "For more info, visit https://www.fairwork.gov.au/employment-conditions/awards/awards-summary/ma000003-summary")

        if employer_selected == "General Retail Industry Award (MA000004)":
            st.write(
                "This pay award covers employers and employees working in the general retail industry. "
                "Including jobs such as check-out operators, sales assistants, stock hands, shelf stackers, salespersons, store managers, "
                "tradespersons (butchers, bakers, florists) and travel agents."
                "For more info, visit https://www.fairwork.gov.au/employment-conditions/awards/awards-summary/ma000004-summary")

        if employer_selected == "Hospitality Industry (General) Award (MA000009)":
            st.write("This pay award covers employers and employees working in the hospitality industry. "
                     "Including jobs such as waiters/waitresses, kitchen hands, cooks/chefs, housekeepers, concierge/reception staff, gaming attendants, "
                     "security officers, casino staff, catering staff and pub owners. "
                     "For more info, visit https://www.fairwork.gov.au/employment-conditions/awards/awards-summary/ma000009-summary")

    # NEXT STEPS

    if user_type == "Employee":
        st.header("Your next steps", divider="rainbow")
        st.write(translator.translate("Don't worry, this tool will try to help you. "
                                      "Please select which scenario best fits your situation:",
                                      dest=target_lang).text)

        with st.expander(translator.translate("I have been underpaid!", dest=target_lang).text):

            st.write(translator.translate('''1. Take a screenshot of the calculations. 
                                            \n 2. Prepare what you would like to say to your boss, making sure you have the payslip you want to talk about and the screenshot of calculations. 
                                            \n 3. Arrange a time to talk to your boss. Show them the gathered information. Sometimes it’s helpful to take a friend or your manager for support. 
                                            \n 4. Discuss the problem with your boss. Stay calm and listen. If you're boss is unsure, refer them to the [Australian Fair Work Ombudsman](https://www.fairwork.gov.au/) website.
                                            \n 5. Together with your boss, work out the next steps and write down what you both agreed to. This documentation is very important. Include a date when it is expected for your pay to be correctly adjusted. . 
                                            \n 6. If your pay hasn’t been corrected by the date decided, follow up with your boss and ask for an update.''',
                                          dest=target_lang).text)

        with st.expander(translator.translate(
                "I’m a student on a temporary or working rights visa. I’m scared of my visa being cancelled!",
                dest=target_lang).text):
            st.write(translator.translate('''Your boss :red[DOES NOT] have any power to cancel your Visa. Ignore any threats or bullying!
                                            Only the Australian Department of Home Affairs can cancel visas, not your boss. 
                                            \n Did you know that the Fair Work Ombudsman supports visa holders even if you've already breached your work-related visa conditions? 
                                            \n This is called the [Assurance Protocol](https://www.fairwork.gov.au/find-help-for/visa-holders-migrants) which protects you against visa cancellations.
                                            \n Remember only Home Affairs can grant, refuse or cancel visas. Not your boss. 
                                            ''', dest=target_lang).text)

        with st.expander(
                translator.translate(
                    "After speaking to my boss, I have been dismissed or threatened with dismissal!",
                    dest=target_lang).text):
            st.write(translator.translate('''This is illegal. There are Australian laws in place to protect people from 
                                            being dismissed when discussing a problem at work or asking for the correct pay. 
                                            ''', dest=target_lang).text)

        st.write(translator.translate('''Sometimes things don't resolve peacefully, if you need more support reach out to the Australian Fair Work Ombudsman:
                                                                      \n - Visit https://www.fairwork.gov.au/
                                                                      \n - Call 13 13 94, 8am to 5:30pm Monday to Friday, excluding public holidays.''',
                                      dest=target_lang).text)

        st.write(f":earth_asia: For translation services and language assistance, call 13 14 50.")

    else:
        st.header("Employer Resources", divider="rainbow")
        st.write('''Please refer to the following links:
                                        \n - [Fair Work Ombudsman Definitions](https://www.fairwork.gov.au/dictionary)
                                        \n - [Fair Work Ombudsman Online Learning Centre](https://www.fairwork.gov.au/tools-and-resources/online-learning-centre)
                                        \n - [Fair Work Ombudsman Downloaded Templates](https://www.fairwork.gov.au/tools-and-resources/templates)
                                        \n - [Need more help? Click here](https://services.fairwork.gov.au/get-help)
                                        ''')

    # DISCLAIMER SECTION

    st.header(":red[Disclaimer]", divider="rainbow")
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
    st.markdown(''':rainbow[Created and designed by the Wage Warriors for UTS iLab2 Spring 2023 in association with the Australian Payroll Association.
                                    Data obtained from the Fair Work Commission and Fair Work Ombudsman websites.]''')


if __name__ == '__main__':
    main()
