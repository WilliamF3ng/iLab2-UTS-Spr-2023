import streamlit as st
import datetime
import pandas as pd
import requests

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

    # Google Translate toggle
    translate_lang = st.selectbox("Translate to: (Unfortunately need to use a Google Cloud API, new subscribers have $300 credits!)",
                                  ["English", "Chinese", "Hindi"])
    target_lang = "en"
    if translate_lang == "Chinese":
        target_lang = "zh-CN"
    elif translate_lang == "Hindi":
        target_lang = "hi"

    download_url = "https://www.fwc.gov.au/documents/awards/pay-database/map-classification-export"
    categories = "classification"

    year = datetime.datetime.now().year
    user_type = st.radio("Are you an employee or employer?", ("Employee", "Employer"))

    if user_type == "Employee":
        awards = ["MA000003", "MA000004", "MA000009"]
        selected_award = st.radio("Select Pay Award:", awards)

        # Add description/info about the selected award
        if selected_award == "MA000003":
            st.write("This award covers employers and employees working in the fast food industry like: "
                     "employees taking orders, including via an app, cooking and selling fast food, "
                     "baristas, delivery drivers, supervisors of these duties and cafes.")
        elif selected_award == "MA000004":
            st.write("This award covers employers and employees working in the general retail industry like: "
                     "check-out operators, sales assistants, stock hands, shelf stackers, salespersons, store managers,"
                     "tradespersons (butchers, bakers, florists) and travel agencies."
            )
        elif selected_award == "MA000009":
            st.write("This award covers employers and employees working in the hospitality industry like: "
                     "waiters/waitresses, kitchen hands, cooks/chefs, housekeepers, concierge/reception staff"
                     "gaming attendants, security officers, casino staff, catering staff and pub owners.")

        # Download and process the dataset
        df = download_and_process_excel(download_url, categories, year)

        if df is not None:
            st.success("Dataset downloaded and processed successfully.")

            # Filter the dataset by the user's selected award
            filtered_df = df[df["awardCode"] == selected_award]

            # Ask user about employment type
            employment_type = st.radio("Select Employment Type:", ("Full Time", "Part Time", "Casual"))

            # Filter further by employment type
            #filtered_df = filtered_df[filtered_df["employmentType"] == employment_type]

            # Ask user which classification level they belong to
            if selected_award == "MA000003":
                award_classification = st.radio("Select award classification:",
                                                ("Fast food employee level 1",
                                                 "Fast food employee level 2",
                                                 "Fast food employee level 3—in charge of one or no person",
                                                 "Fast food employee level 3—in charge of 2 or more people"))
            elif selected_award == "MA000004":
                award_classification = st.radio("Select award classification:",
                                                ("Retail Employee Level 1",
                                                 "Retail Employee Level 2",
                                                 "Retail Employee Level 3",
                                                 "Retail Employee Level 4",
                                                 "Retail Employee Level 5",
                                                 "Retail Employee Level 6",
                                                 "Retail Employee Level 7",
                                                 "Retail Employee Level 8"))

            else:
                award_classification = st.radio("Select award classification:",
                                                ("placeholder1",
                                                 "placeholder2",
                                                 "placeholder3",
                                                 "placeholder4"))

            # Filter further by award classification
            filtered_df = filtered_df[filtered_df["classification"] == award_classification]

            # CURRENT (LAST UPDATED 20.08.2023) prototype assumes user is 21years and over (adult)
            filtered_df = filtered_df[filtered_df["employeeRateTypeCode"] == "AD"]

            # Select only the relevant columns
            selected_columns = ["baseRate", "baseRateType","calculatedRate","calculatedRateType"]
            selected_data = filtered_df[selected_columns]
            st.subheader("Your pay rates are:")
            st.write(selected_data)

        else:
            st.error("Failed to download and process the dataset.")

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
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hours_worked = {}


    st.date_input("Enter date")


    for day in days_of_week:
        hours = st.number_input(f"Enter hours worked on {day}:", min_value=0.0, step=0.1)
        hours_worked[day] = hours

    st.subheader("Hours Worked:")
    hours_df = pd.DataFrame(hours_worked.items(), columns=["Day", "Hours Worked"])
    st.table(hours_df)

    # Calculate total pay based on hours worked
    total_hours = sum(hours_worked.values())

    base_pay_rate = filtered_df.loc[filtered_df["classification"] == award_classification, "calculatedRate"].iloc[0]
    overtime_hours = total_hours - 38
    casual_loading = (1.25 * base_pay_rate) # casual loading is 25% of the base_pay_rate
    overtime_rate = (1.5 * base_pay_rate)
    total_pay = 0.0

    if employment_type == "Full Time":
        # Full Time calculations
        overtime_hours = max(0, total_hours - 38)
        total_pay = (total_hours * base_pay_rate) + (overtime_hours * overtime_rate)

    elif employment_type == "Part Time":
        # Part Time calculations
        if total_hours <= 20:
            total_pay = total_hours * base_pay_rate
        else:
            overtime_hours = max(0, total_hours - 20)
            total_pay = (total_hours * base_pay_rate) + (overtime_hours * overtime_rate)

    elif employment_type == "Casual":
        # Casual calculations
        total_pay = total_hours * casual_loading

    st.subheader("Pay Details:")
    st.write(f"Hours Worked: {total_hours} hours.")
    st.write(f"According to your chosen award and classification level, your total pay is ${total_pay:.2f}.")

    st.subheader("Next steps")
    st.write("If you have been underpaid, please speak to your employer or refer to the following links for more help.")
    st.write(f"Australian Fair Work Ombudsman, visit https://www.fairwork.gov.au/ or call 13 13 94 :telephone: , "
             f"open 8am to 5:30pm Monday to Friday, excluding public holidays.")
    st.write(f":earth_asia: For translation services and language assistance, call 13 14 50.")

if __name__ == "__main__":
    main()