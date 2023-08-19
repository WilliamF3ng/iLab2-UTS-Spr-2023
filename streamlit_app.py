import streamlit as st
import requests
import pandas as pd
import datetime

# The end product will be a streamlit app.
# We will ensure the data will always be the latest file at the time of the user access, by using the user computer's
# datetime to get the current year. Meaning this functionality should persist, unless the user's computer does not have
# the correct time or not connected to the internet.

#

# Create a function that will use the URL, category (award, classifications, wage allowances, expense allowances,
# penalty rates
def download_and_process_excel(url, category, year):
    # Construct the URL based on the provided category and year
    full_url = f"{url}-{year}.xlsx"

    # Send a GET request to download the file
    response = requests.get(full_url)

    if response.status_code == 200:
        # Save the Excel file locally
        file_name = f"{category}_export_{year}.xlsx"
        with open(file_name, "wb") as file:
            file.write(response.content)

        # Read the Excel file using pandas
        df = pd.read_excel(file_name)

        # Now you can work with the DataFrame (df) as needed
        return df
    else:
        st.error(f"Failed to download the file for {category} - {year}")
        return None


def main():
    st.title("Web Scraping and Displaying Excel Data with Streamlit")

    current_year = datetime.datetime.now().year

    urls = [
        "https://www.fwc.gov.au/documents/awards/pay-database/map-award-export",
        "https://www.fwc.gov.au/documents/awards/pay-database/map-classification-export",
        "https://www.fwc.gov.au/documents/awards/pay-database/map-wage-allowance-export",
        "https://www.fwc.gov.au/documents/awards/pay-database/map-expense-allowance-export",
        "https://www.fwc.gov.au/documents/awards/pay-database/map-penalty-export"
    ]
# Using an index here to determine which category to substitute into the scraper
    categories = [
        "award",
        "classification",
        "wage_allowance",
        "expense_allowance",
        "penalty"
    ]

    st.write("Select a category to download and display data:")

    selected_category = st.selectbox("Category", categories)

    if st.button("Download and Display"):
        index = categories.index(selected_category)
        df = download_and_process_excel(urls[index], selected_category, current_year)
        if df is not None:
            st.write("Displaying data for:", selected_category)
            st.write(df)


if __name__ == "__main__":
    main()
