import json
from prettytable import PrettyTable
import urllib.request
from datetime import datetime

# URL to fetch JSON data
url = 'https://data.gov.au/data/api/3/action/datastore_search?resource_id=33673aca-0857-42e5-b8f0-9981b4755686&limit=5'
response = urllib.request.urlopen(url)
json_data = response.read()

# Parse the JSON data
data = json.loads(json_data)["result"]["records"]

# Create a table
table = PrettyTable()
table.field_names = ["_id", "Date", "Holiday Name", "Information", "More Information", "Jurisdiction"]

# Get the current year
current_year = datetime.now().year
current_year_prefix = str(current_year)[:4]

print("Current Year:", current_year)
print("Current Year Prefix:", current_year_prefix)

# Populate the table with data
for record in data:
    original_date = record["Date"]
    print("Original Date:", original_date)


    # Doesn't work yet, showing blank rows, meaninng original date is not a string.
    if original_date.startswith(current_year_prefix):
        formatted_date = f"{original_date[:4]}/{original_date[4:6]}/{original_date[6:8]}"
        table.add_row([record["_id"], formatted_date, record["Holiday Name"],
                       record["Information"], record["More Information"], record["Jurisdiction"]])
# Print the table
print(table)

