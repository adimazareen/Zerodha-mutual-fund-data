import requests
from bs4 import BeautifulSoup
import json

def get_data():
    # URL of the mutual fund portfolio overview page
    url = 'https://www.moneycontrol.com/mutual-funds/sbi-large-midcap-fund/portfolio-holdings/MSB003'

    # Initialize empty lists to store the raw data
    months = []
    raw_data = []
    data = {"name":"sbi-large-midcap-fund","holdings": []}

    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the data container by ID
        data_container = soup.find(id='equity_tab5')
        if data_container:
            # Extract table headers (months)
            headers = data_container.find_all('th')
            for header in headers[1:]:  # Start from the second element
                months.append(header.text.strip())

            # Extract rows (holdings data)
            rows = data_container.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 1:  # Ensure it's not an empty row
                    # Extract the holding name and monthly percentages
                    holding_name = cells[0].text.strip()
                    values = [cell.text.strip().replace('%', '') for cell in cells[1:]]
                    raw_data.append([holding_name] + values)
        else:
            print("Data container not found on the webpage.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    # Transform raw data into the desired format
    for row in raw_data:
        name = row[0]
        values = [float(val) if val != '-' else None for val in row[1:]]
        data["holdings"].append({
            "name": name,
            "data": values
        })

    # Write the data to a JSON file
    with open('./data/sbi-large-midcap-fund-regular-plan.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("Data has been written to 'sbi-large-midcap-fund-regular-plan.json'.")

# Call the function to fetch the data and save it as a JSON file
get_data()
