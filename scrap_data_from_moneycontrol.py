import requests
from bs4 import BeautifulSoup
import flask
import json
from flask_cors import CORS

app = flask.Flask(__name__)
# Serve frontend files statically
@app.route('/<path:path>', methods=['GET'])
def get_frontend_file(path):
    return flask.send_from_directory('./frontend', path)
# Enable CORS
CORS(app)

@app.route('/get-data', methods=['GET'])
def get_data():
    # Initialize variables
    months = []
    raw_data = []
    data = {
        "months": months,
        "holdings": []
    }

    # URL of the mutual fund portfolio overview page
    url = 'https://www.moneycontrol.com/mutual-funds/hdfc-flexi-cap-fund-direct-plan-/portfolio-overview/MHD1144'

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

    # Return the JSON response
    return flask.jsonify(data)

@app.route('/', methods=['GET'])
def serve_main():
    return flask.send_file('./frontend/index.html')

if __name__ == '__main__':
    app.run(debug=True)

