import streamlit as st
import streamlit_extras
from streamlit_extras.switch_page_button import switch_page

import datetime
from datetime import time

import pandas as pd
import requests
from googletrans import Translator

translator = Translator()
st.set_page_config(layout="wide")

from streamlit_extras.app_logo import add_logo
add_logo("gallery/ResizeWW.png", height=100)

# Exact same app code below
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


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
            st.caption("Adults are considered 21 years or older.")

            filtered_df = filtered_df[filtered_df["clauseDescription"] == user_clauseDescription]

            # Data contains weird values,
            filtered_df = filtered_df[
                ~filtered_df["classification"].isin(
                    ["Retail Employee Level 2*", "Retail Employee Level 3*"])]

            unique_classification = filtered_df["classification"].unique()
            user_classification = st.selectbox(translator.translate("Choose your classification: ",
                                                                    dest=target_lang).text,
                                               unique_classification)
            #st.caption(
            #    "Don't know your classification level? [Click here!](https://www.fairwork.gov.au/employment-conditions/awards/award-classifications)")

            # New page switcher
            find_classification = st.button("I don't know my classification level")
            if find_classification:
                switch_page("Find_my_award_level")


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
                    styled_df = st.data_editor(breakdown_df, hide_index=True, key="b")

                # Download button to export breakdown table
                csv = convert_df(breakdown_df)
                st.download_button(label="Download my wage calculations",
                                    data=csv,
                                    file_name="my_wage_calculations.csv",
                                    mime="text/csv")

        # END OF CALCULATOR MODULE

        # START OF CLOCK IN/CLOCK OUT SECONDARY MODULE
        with clock_hours:
            with st.form("clock_hours_form"):
                clock_day_data = {day: {"start_time": time(),
                                        "end_time": time(),
                                        "hours_worked":0.0,
                                        "is_evening_shift": False,
                                        "is_public_holiday": False,
                                        "time_difference": time()} for day in days_of_week}

                for index, day in enumerate(days_of_week):
                    clock_col1, clock_col2, clock_col3 = st.columns(3)

                    with clock_col1:
                        start_time = st.time_input(f"Enter start time on {day}: ",
                                                   value=time(9,0))

                        clock_day_data[day]["start_time"] = start_time

                    with clock_col2:
                        end_time = st.time_input(f"Enter end time on {day}: ",
                                                 value=time(18,0))

                        clock_day_data[day]["end_time"] = end_time

                    with clock_col3:
                        clock_day_data[day]["is_evening_shift"] = st.checkbox(f"Evening shift on {day}",
                                                                              help="Tick if your shift started or ended after 6pm")
                        clock_day_data[day]["is_public_holiday"] = st.checkbox(f"Public holiday on {day}")

                        if index < len(days_of_week) - 1:
                            st.markdown("---")

                # Superannuation slider
                clock_superannuation_rate = st.slider("Superannuation rate", min_value=11.0, max_value=15.0,
                                                value=11.0, step=0.5,
                                                format="%f%%")

                clock_submitted = st.form_submit_button("Calculate", use_container_width=True)

        if clock_submitted:
                st.success(translator.translate("We've done the maths for you.", dest=target_lang).text, icon="✅")

                st.header("This is your pay", divider="rainbow")

                # Check if end time is earlier than start time
                if start_time and end_time and end_time < start_time:
                    st.error("End time cannot be earlier than start time.")

                clock_table_data = {"Day": [], "Hours Worked": [], "Evening Shift": [], "Overtime": [],
                                    "Rate Description": [],
                                    "Rate": [], "Pay": []}

                for day, data in clock_day_data.items():
                    start_time = data["start_time"]
                    end_time = data["end_time"]
                    is_evening_shift = data["is_evening_shift"]
                    is_public_holiday = data["is_public_holiday"]

                # Check if end time is earlier than start time
                    if start_time and end_time and end_time < start_time:
                        st.error(f"End time cannot be earlier than start time on {day}.")
                    else:
                        start_datetime = datetime.datetime.combine(datetime.datetime.today(), start_time)
                        end_datetime = datetime.datetime.combine(datetime.datetime.today(), end_time)
                        time_difference = end_datetime - start_datetime

                        # Calculate hours and minutes
                        hours_worked = time_difference.seconds // 3600
                        minutes_worked = (time_difference.seconds // 60) % 60

                        # For hours x rate calculation per day
                        total_minutes_worked = time_difference.seconds // 60  # Total minutes worked
                        hours_worked_decimal = total_minutes_worked / 60  # Convert total minutes to decimal hours

                    # DUPLICATE THE PAY RATES CALCULATION AND DECLARE RATES

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

                    # SPECIAL CALCULATION
                    evening_penalty = filtered_df_penalty[
                    (filtered_df_penalty["clauseDescription"].str.contains("ordinary and penalty rates", case=False)) &
                    (filtered_df_penalty["penaltyDescription"].str.contains("Monday to Friday", case=False)) &
                    (filtered_df_penalty["rate"].notna())]["penaltyCalculatedValue"].iloc[0]

                    # MA000003 = 10PM TO MIDNIGHT, MIDNIGHT TO 6AM
                    # MA000004 = AFTER 6PM

                    # ABOVE CODE ONLY ACCOUNTS FOR 10PM TO MIDNIGHT AND AFTER 6PM -- still WIP

                    # END OF RATE DECLARATIONS

                    clock_total_pay = 0.0
                    days_with_evening_shifts = []
                    days_with_more_4hs = []
                    rolling_total_hours_worked = 0.0
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

                    clock_day_pay = hours_worked_decimal * rate

                    # Append data to the clock_table_data dictionary
                    clock_table_data["Day"].append(day)
                    clock_table_data["Hours Worked"].append(f"{hours_worked}h {minutes_worked}min")
                    clock_table_data["Evening Shift"].append("Yes" if is_evening_shift else "No")
                    clock_table_data["Overtime"].append(is_overtime)
                    clock_table_data["Rate Description"].append(rate_description)
                    clock_table_data["Rate"].append(f"${rate:.2f}")
                    clock_table_data["Pay"].append(f"${clock_day_pay:.2f}")

                    clock_total_pay += clock_day_pay

                    # is_under_18 = user_classification.lower().strip() in [
                    #     "under 16 years",
                    #     "16 years",
                    #     "17 years",
                    #     "15 years of age and under",
                    #     "16 years of age",
                    #     "17 years of age",
                    #     "16 years of age and under"
                    # ]
                    # if is_under_18 and total_hours_worked < 30:
                    #     superannuation_per_week = 0.00
                    # else:
                    #     superannuation_per_week = (clock_total_pay * clock_superannuation_rate) / 100
                    #
                    # st.write(
                    #     f"You have worked {total_hours_worked:.1f} hours! Your total gross pay is ${total_pay:.2f}.")
                    # st.caption(
                    #     ":bulb: Gross pay is the total amount of money you earn before taxes or deductions are removed.",
                    #     help="Your employer may deduct taxes if you've provided your Australian Tax File Number.")
                    # st.write(f"Your superannuation this week is ${superannuation_per_week:.2f}. "
                    #          f"If you think this is :red[wrong], please double check you've entered the correct hours above or look at the Next Steps below.")
                    #
                    # if days_with_more_4hs:
                    #     st.write(
                    #         f"- :hamburger: On {', '.join(days_with_more_4hs)}, you should've been allowed to take a lunch break. "
                    #         "Usually this break can be between 30 minutes to 1 hour depending on your shift and your employer.")
                    #
                    # if days_with_evening_shifts:
                    #     st.write(
                    #         f"- :crescent_moon: On {', '.join(days_with_evening_shifts)}, you worked evening shift(s). You may be entitled to additional pay.")
                    # if selected_award == "MA000003":
                    #     st.write(
                    #         "Your evening rate is 110% of your ordinary pay from Monday to Friday 10pm to midnight OR 115% from midnight to 6am.")
                    # elif selected_award == "MA000004":
                    #     st.write(
                    #         "Your evening rate is 125% of your ordinary pay from Monday to Friday after 6pm.")
                    # else:
                    #     st.write(
                    #         "Your evening rate is \$ 2.62 per hr extra from 7pm to midnight OR $ 3.93 per hr from midnight to 7am.")

                # Create a DataFrame for the clock_table_data
                clock_breakdown_df = pd.DataFrame(clock_table_data)
                with st.expander("Show hours calculation"):
                    clock_styled_df = st.data_editor(clock_breakdown_df, hide_index=True)

                # Download button to export breakdown table
                csv = convert_df(clock_breakdown_df)
                st.download_button(label="Download my wage calculations",
                                   data=csv,
                                   file_name="my_wage_calculations.csv",
                                   mime="text/csv")

    else:
        st.header("Understanding the Pay Award", divider="rainbow")
        employer_selected = st.radio("Choose the relevant pay award for more information.",
                                     ("Fast Food Industry Award",
                                      "General Retail Industry Award",
                                      "Hospitality Industry (General) Award"))

        if employer_selected == "Fast Food Industry Award":
            st.write('''
            **Fast Food Award**
            
           \n  1. Who Does the Fast Food Award Cover?
           \n The Fast Food Award encompasses a wide spectrum of roles within the fast food industry. 
           This includes businesses involved in order-taking, food preparation, sales, and delivery of fast food designed for take-away consumption. 
           Employees within this award category include order takers, cooks, baristas, delivery drivers, and supervisors in fast food establishments. 
           Furthermore, the award extends its coverage to labor hire businesses and their employees placed within the fast food sector.
           \n 2. What Qualifies as Fast Food?
           \n Fast foods, as defined under this award, are meals, snacks, and beverages intended for consumption away from the point of sale. 
           These items are packaged to facilitate consumption in alternate locations and are commonly found in food courts, shopping centers, and retail complexes. 
           Businesses engaged in the preparation and sale of fast food, even if delivered by third parties, fall within the purview of this award.
           \n 3. Who Isn’t Covered by the Fast Food Award?
           \n It's crucial to recognize the exceptions. The Fast Food Award does not apply to businesses such as cafes, restaurants, coffee shops, or bars where food and beverages are primarily intended for on-premises consumption. 
           Additionally, employers and employees falling under the Restaurant Award, Hospitality Award, or Retail Award are not covered. 
           Employees delivering goods prepared by fast food businesses but not directly employed by them are also exempt from this award's provisions.
           \n For detailed information on the classifications and coverage, please refer to [clauses 2, 4, and 12 of the Fast Food Industry Award [MA000003]](https://library.fairwork.gov.au/award/?krn=ma000003).
            ''')

        if employer_selected == "General Retail Industry Award":
            st.write('''
            **General Retail Award**
            
            \n 1. Who Does the Retail Award Cover?
            \n The Retail Award extends its coverage to employers operating in the general retail industry and their employees who fall within the specified classifications. 
            The general retail industry encompasses the sale or hire of goods and services for personal, household, or business use. 
            \n This includes a diverse range of products and services such as clothing, food, furniture, household goods, bakery products, repair services, and even the delivery of newspapers.
            Employees covered under the Retail Award include a broad spectrum of roles, such as check-out operators, sales assistants, stock hands, door-to-door salespersons, trolley collectors, service supervisors, department and store managers, tradespersons like butchers, bakers, and florists, employees selling travel packages, back-office clerical staff in retail shops, and electrical device repairers.
            \n Additionally, labour hire businesses and their employees placed within organizations in the retail industry are also included under the award's coverage.
            \n For detailed information on classifications and coverage, please refer to [clauses 2, 4, and Schedule A of the General Retail Industry Award [MA000004]](https://library.fairwork.gov.au/award/?krn=MA000004).
            
            \n 2. Who Isn’t Covered by the Retail Award?
            \n The Retail Award does not apply to specific establishments and activities within the retail sector. Employers and employees engaged in the following are exempt from the Retail Award:
            \n - Retail sale or hire of goods or services by community pharmacies, pharmacies in hospitals or other in-patient institutions, hair and beauty establishments, stand-alone butcher shops, and nurseries.
            \n - Manufacturing or processing establishments (excluding seafood processing establishments).
            \n - Hair and beauty work undertaken in the theatrical, amusement, or entertainment industries.
            \n - Clerical functions performed away from retail establishments, warehousing, and distribution.
            \n - Motor vehicle retailing and motor vehicle fuel and parts retailing.
            \n - Restaurants, cafes, hotels, motels, and fast food operations.
            \n - Building, construction, installation, repair, or maintenance contractors engaged to perform work at a retail establishment.
            \n Additionally, employers and employees covered by specific awards such as the Fast Food Award, Hair and Beauty Award, Meat Award, and Pharmacy Award are not subject to the Retail Award's provisions.
            \n Understanding these exemptions is crucial for employers to ensure compliance with applicable regulations and standards.
            ''')

        if employer_selected == "Hospitality Industry (General) Award":
            st.write('''
            **Hospitality Industry (General) Award**
            
            \n 1. Who Does the Hospitality Award Cover?
            \n The Hospitality Award extends its coverage to employers in various sectors of the hospitality industry, including tourist accommodations, wine saloons, caterers, casinos, nightclubs, convention facilities, and restaurants associated with covered employers. 
            \n Examples of roles covered include waiters, kitchen hands, cooks, housekeepers, clerical staff, gaming attendants, security officers, managerial staff (excluding senior management), and catering employees, among others. 
            Labour hire businesses and their employees placed within the hospitality industry also fall under the award's coverage.
            \n For detailed information on specific classifications, please refer to [clauses 2, 4, and Schedule A of the Hospitality Industry (General) Award [MA000009]](https://library.fairwork.gov.au/award/?krn=MA000009).
            
            \n 2. Who Isn’t Covered by the Hospitality Award?
            \n Certain employers and employees are exempt from the Hospitality Award. These include:
            \n - Clubs: Clubs registered or recognized under state or territory legislation.
            \n - In-flight Catering: Employees engaged in in-flight catering for airlines.
            \n - Educational Institutions: Employees in boarding schools and residential colleges.
            \n - Healthcare Institutions: Employees in hospitals.
            \n - Local Councils: Employees of local councils.
            \n - Catering in Certain Facilities: Catering employees in restaurant businesses or aged care facilities.
            \n - Theme Parks: Employees in theme parks, except for those exclusively operating in the hospitality industry.
            \n - Contract Cleaning Businesses: Employees in contract cleaning businesses not exclusively in the hospitality industry.
            \n - Senior Management: Senior management personnel responsible for significant areas of the business, including company secretaries, chief accountants, and venue managers.
            \n - Contract Services: Contract security, gardening, or maintenance provided by businesses not primarily in the hospitality industry.
            \n - Strata Management: Employees in strata management businesses.
            \n - Entertainers: Musicians and dancers performing in hotels.
            \n Additionally, employers and employees falling under specific awards like the Registered Clubs Award, Restaurant Award, Fast Food Award, and Alpine Resorts Award are not subject to the Hospitality Award's provisions.
            ''')

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
        st.subheader(translator.translate("Want more info?", dest=target_lang).text)
        retail_to_home = st.button("Take me to some Helpful Resources :arrow_forward:")
        if retail_to_home:
            switch_page("Helpful resources")

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
