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

        # Now you can work with the DataFrame (df) as needed
        print(df.head())  # Print the first few rows of the DataFrame
    else:
        print(f"Failed to download the file for {category} - {year}")


def main():
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

    for url, category in zip(urls, categories):
        download_and_process_excel(url, category, current_year)


if __name__ == "__main__":
    main()
