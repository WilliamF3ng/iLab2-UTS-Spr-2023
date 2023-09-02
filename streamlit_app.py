# INSTALLING REQUIRED LIBRARIES

import streamlit as st # upgraded to 1.26.0 (released Aug 24th 2023)

#from streamlit_extras.grid import grid
# Playing around with pip install streamlit-extras

import datetime
import pandas as pd
import requests

# Translation feature
from googletrans import Translator
translator = Translator()

# Download datasets from the FWC website
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
                                  "Currently supporting 10 languages (more coming soon!). Click here to translate to: ",
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

    user_type = st.radio(translator.translate("Are you an Employee or Employer?",dest=target_lang).text,
                         ("Employee", "Employer"))
    if user_type == "Employee":
        awards = ["MA000003", "MA000004", "MA000009"]
        selected_award = st.radio(translator.translate("What's your pay award?", dest=target_lang).text, awards)

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
            st.success(translator.translate("Download successful.", dest=target_lang).text)

            # Filter the dataset by the user's selected award
            filtered_df = df[df["awardCode"] == selected_award]
            filtered_df_penalty = df_penalty[df_penalty["awardCode"] == selected_award]

            # Ask user about employment type
            employment_type = st.radio(translator.translate("What's your Employment Type?",dest=target_lang).text,
                                       ("Full Time", "Part Time", "Casual"))

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

            # Making some large assumptions like
            # excluding baking employees in 004

            # Try to exclude shiftwork, but cannot as most migrants could be shiftworkers
            # filtered_df_penalty = filtered_df_penalty[~filtered_df_penalty["clauseDescription"].
            # str.contains("shiftwork and penalty rates", case=False)]
            #st.write(filtered_df_penalty)

################################################# 2nd Sept Progress

            # Version 1.9

            # Exclude baking employees who start work at odd hours like 2am start.
            # Filter by "Early morning shifts"


            # Select only the relevant columns
            selected_col_classification = ["baseRate", "baseRateType"] # add penalty rate calculations to this table too
            selected_data_class = filtered_df[selected_col_classification]

            selected_col_penalty = ["clauseDescription","penaltyDescription","rate","penaltyCalculatedValue"]
            selected_data_penalty = filtered_df_penalty[selected_col_penalty]

            st.header("Your pay rates are:", divider="rainbow")

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
            st.error("Error failed to download. Please retry again later.")

    else:
        st.markdown("### Pay Award Descriptions:")
        st.write("Choose the relevant pay award for more information about each award.")

        if st.checkbox("Fast Food Industry Award (MA000003)"):
            st.write("This award covers employers and employees working in the fast food industry like: "
                     "employees taking orders, including via an app, cooking and selling fast food, "
                     "baristas, delivery drivers, supervisors of these duties and cafes. "
                     "For more info, visit https://www.fairwork.gov.au/employment-conditions/awards/awards-summary/ma000003-summary")

        if st.checkbox("General Retail Industry Award (MA000004)"):
            st.write("This award covers employers and employees working in the general retail industry like: "
                     "check-out operators, sales assistants, stock hands, shelf stackers, salespersons, store managers,"
                     "tradespersons (butchers, bakers, florists) and travel agencies. "
                     "For more info, visit https://www.fairwork.gov.au/employment-conditions/awards/awards-summary/ma000004-summary")

        if st.checkbox("Hospitality Industry (General) Award (MA000009)"):
            st.write("This award covers employers and employees working in the hospitality industry like: "
                     "waiters/waitresses, kitchen hands, cooks/chefs, housekeepers, concierge/reception staff"
                     "gaming attendants, security officers, casino staff, catering staff and pub owners. "
                     "For more info, visit https://www.fairwork.gov.au/employment-conditions/awards/awards-summary/ma000009-summary")

    # Collect hours worked for each day of the week
    # days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # hours_worked = {}

    on = st.toggle("I didn't take a break")
    if on:
        st.write("30 mins lunch break will be deducted!")

    on1 = st.toggle("Tick if today was a public holiday")
    if on1: st.write("You have indicated that today is a public holiday!")

    # for day in days_of_week:
    #     hours = st.number_input(f"Enter hours worked on {day}:", min_value=0.0, step=0.1)
    #     hours_worked[day] = hours
    #
    # st.subheader("Hours Worked:")
    # hours_df = pd.DataFrame(hours_worked.items(), columns=["Day", "Hours Worked"])
    # st.table(hours_df)
    #
    # # Calculate total pay based on hours worked
    # total_hours = sum(hours_worked.values())
    #
    # base_pay_rate = filtered_df.loc[filtered_df["classification"] == parent_classification, "calculatedRate"].iloc[0]
    # overtime_hours = max(0, total_hours - 38)
    # casual_loading = (1.25 * base_pay_rate) # casual loading is 25% of the base_pay_rate
    # overtime_rate = (1.5 * base_pay_rate)
    #
    # # Casual penalty rates
    # casual_saturday_rate = (1.5 * base_pay_rate) # casual loading 25%, sat penalty 25%
    #
    # casual_sunday_rate_OT_before_3hrs = (1.75 * base_pay_rate) # casual loading 25%, sun penalty 50% and OT before 3hrs Mon to Sat
    # casual_OT_after_3hrs = (2.25 * base_pay_rate) # casual loading, OT after 3hrs Mon to Sat
    # # Disclaimer, both casual before and after 3hrs only relies on Monday to Saturday period, FWO has no mention of Sunday OT at of writing this note.
    #
    # casual_public_rate = (2.5 * base_pay_rate) # casual loading 25%, public 225%
    #
    # # Permanent FT/PT rates
    # permanent_saturday_rate = (1.25 * base_pay_rate)
    # permanent_sunday_rate_OT_before_3hrs = (1.5 * base_pay_rate)
    # permanent_OT_after_3hrs = (2 * base_pay_rate)
    # permanent_public_rate = (2.25 * base_pay_rate)

# THIS CODE LOGIC HAS BEEN TEST AND IS INCORRECT.

    # total_pay = 0.0
    # for day, hours in hours_worked.items():
    #     if employment_type == "Full Time":
    #     # Full Time calculations
    #         if day == "Saturday":
    #             total_pay += total_hours * permanent_saturday_rate
    #         elif day == "Sunday":
    #             total_pay += total_hours * permanent_sunday_rate_OT_before_3hrs
    #         else:
    #             total_pay = (total_hours * base_pay_rate) + (overtime_hours * overtime_rate)
    #
    #     elif employment_type == "Part Time":
    #     # Part Time calculations
    #         if total_hours <= 20:
    #             total_pay = total_hours * base_pay_rate
    #         else:
    #             total_pay = (total_hours * base_pay_rate) + (overtime_hours * overtime_rate)
    #
    #     elif employment_type == "Casual":
    #     # Casual calculations
    #         if day == "Saturday":
    #             total_pay += total_hours * casual_saturday_rate
    #         elif day == "Sunday":
    #             if hours <= 3:
    #                 total_pay += hours * casual_sunday_rate_OT_before_3hrs
    #         else:
    #             total_pay += total_hours * casual_loading
    # else:
    #     total_pay += total_hours * base_pay_rate

    st.header("Pay Details:", divider="rainbow")
    # st.write(f"Hours Worked: {total_hours} hours.")
    # st.write(f"According to your chosen award and classification level, your total pay is ${total_pay:.2f}.")

    st.header("Next steps", divider="rainbow")
    st.write("If you have been underpaid, please speak to your employer or refer to the following links for more help.")
    st.write(f"Australian Fair Work Ombudsman, visit https://www.fairwork.gov.au/ or call 13 13 94 :telephone: , "
             f"open 8am to 5:30pm Monday to Friday, excluding public holidays.")
    st.write(f":earth_asia: For translation services and language assistance, call 13 14 50.")


    # st.markdown(''':red[DISCLAIMER:] This Pay Calculator is an :orange[unofficial] tool.
    # It's only for information, not exact pay. It might have mistakes.
    # \n Please use the official Australian Fair Work Ombudsman's guidelines for correct pay rates and rules.
    # This calculator can't replace professional help. If you rely on it, it's your risk.
    # \nThe people who made this are not responsible for mistakes. Check its results with official sources.
    # Get legal or professional help if needed.
    # \n If you use this Pay Calculator, you know it's :orange[unofficial].
    # You're responsible for what you do with its results.''')

if __name__ == "__main__":
    main()