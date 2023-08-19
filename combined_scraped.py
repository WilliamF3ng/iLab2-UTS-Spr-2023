import streamlit as st
import requests
import pandas as pd
import datetime


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

        # Add a category column to the DataFrame
        df['Category'] = category

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

    categories = [
        "award",
        "classification",
        "wage_allowance",
        "expense_allowance",
        "penalty"
    ]

    st.write("Click the button to download and display all categories:")

    if st.button("Download and Display All Categories"):
        progress_bar = st.progress(0)

        dataframes = []

        for idx, (url, category) in enumerate(zip(urls, categories)):
            df = download_and_process_excel(url, category, current_year)
            if df is not None:
                dataframes.append(df)

            # Update the progress bar
            progress_bar.progress((idx + 1) / len(urls))

        # Perform a left join (merge) on the DataFrames using awardId, awardFixedId, and awardCode as the primary key
        combined_df = dataframes[0]
        for df in dataframes[1:]:
            combined_df = pd.merge(combined_df, df,
                                   on=["awardID", "awardFixedID", "awardCode"],
                                   how="left",
                                   suffixes=('', f'_{df["Category"].iloc[0]}'))

        # Remove the lastModifiedDateTime column
        combined_df = combined_df.drop(columns=["operativeFrom","operativeTo","lastModifiedDateTime"])


        st.write("Combined DataFrame for all categories:")
        st.write(combined_df)


if __name__ == "__main__":
    main()
