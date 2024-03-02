import requests
from bs4 import BeautifulSoup
import csv
import re

# Function to scrape data from a given URL
def scrape_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract the data you need from the HTML
        # Here you need to identify the specific elements containing the data and extract them
        # For demonstration, let's assume you're extracting the crime statistics table
        crime_table = soup.find('table')
        if crime_table:
            rows = crime_table.find_all('tr')
            data = []
            for row in rows:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                # Exclude header rows
                if cols and len(cols) >= 7 and not re.match(r'^\s*Incident\s*#', cols[0]):
                    # Format date and time if not explicitly given
                    date_reported, time_reported = parse_date_time(cols[3])
                    cols[1] = date_reported if date_reported else ''
                    cols[2] = time_reported if time_reported else ''
                    # Append data
                    data.append(cols[:7])  # Considering first 7 columns
            return data
        else:
            print(f"No data found on {url}")
            return None
    else:
        print(f"Failed to retrieve data from {url}")
        return None

# Function to parse date and time from Date/Time Occurred if Date Reported or Time Reported is not explicitly given
def parse_date_time(date_time_occurred):
    date_reported = ''
    time_reported = ''
    if date_time_occurred:
        datetime_components = date_time_occurred.split()
        if len(datetime_components) >= 2:
            date_reported = datetime_components[0]
            time_reported = datetime_components[1]
    return date_reported, time_reported

# Function to write data to a CSV file
def write_to_csv(data, filename):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

# Main function to iterate through years and months and scrape data
def main():
    base_url = "https://www1.udel.edu/police/crime-stats/"
    years = range(2017, 2025)  # Update the range to include the years you need
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

    filename = "all_crime_data.csv"
    # Write header to CSV
    header = ["Incident #", "Date Reported", "Time Reported", "Date/Time Occurred", "Description", "Location", "Disposition"]
    write_to_csv([header], filename)

    for year in years:
        for month in months:
            # Determine the number of days in the current month
            if month in ['january', 'march', 'may', 'july', 'august', 'october', 'december']:
                num_days = 31
            elif month == 'february':
                # Assuming non-leap years for simplicity
                num_days = 28
            else:
                num_days = 30

            for day in range(1, num_days + 1):
                day_str = str(day).zfill(2)  # Zero-pad the day if necessary
                url = f"{base_url}{year}/{month}/{month}{day_str}{str(year)[2:]}.html"
                data = scrape_data(url)
                if data:
                    write_to_csv(data, filename)

if __name__ == "__main__":
    main()
