import requests
import pandas as pd

# URL of the Excel file
url = "https://www.fwc.gov.au/documents/awards/pay-database/map-award-export-2023.xlsx"

# Send a GET request to download the file
response = requests.get(url)

if response.status_code == 200:
    # Save the Excel file locally
    with open("map_award_export_2023.xlsx", "wb") as file:
        file.write(response.content)

    # Read the Excel file using pandas
    df = pd.read_excel("map_award_export_2023.xlsx")

    # Now you can work with the DataFrame (df) as needed
    print(df.head())  # Print the first few rows of the DataFrame
else:
    print("Failed to download the file")
