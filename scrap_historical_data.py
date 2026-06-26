import requests
import time
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import json
import re


# def make_slug(input_string):
#     # Convert the input string to lowercase, replace spaces with hyphens, and remove non-alphanumeric characters
#     slug = re.sub(r'[^a-zA-Z0-9\s]', '', input_string.lower())  # remove non-alphanumeric characters
#     slug = slug.replace(" ", "-")  # replace spaces with hyphens
#     return slug

# Example: Scraping a mutual fund's fact sheet from a website (e.g., BSE, Morningstar)
url = f"https://www.moneycontrol.com/mutual-funds/bank-of-india-flexi-cap-fund-direct-plan-growth/portfolio-overview/MBA215"

response = requests.get(url)
time.sleep(2)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table containing the holdings (you will need to inspect the website's HTML structure)
holdings_table = soup.find('div', {'id': 'equity_tab5'}).find('table')  # Adjust class name based on the HTML structure
# Example parsing of the holdings table
rows = holdings_table.find_all('tr')[1:]  # Exclude header row

data = []
header_row = [th.get_text(strip=True) for th in holdings_table.find_all('th')]
data = [header_row]
for row in rows:
    new_row = [span.get_text(strip=True) for td in BeautifulSoup(str(row), 'html.parser').find_all('td') for span in td.find_all('span', class_='port_right')] + [a.get_text(strip=True) for td in BeautifulSoup(str(row), 'html.parser').find_all('td', class_='robo_medium') for a in td.find_all('a')] + [td.get_text(strip=True) for td in BeautifulSoup(str(row), 'html.parser').find_all('td', class_=lambda x: x is None)]
    data.append(new_row)

# with open('./data-1.json', 'w') as fp:
#     json.dump(data, fp)
# Extract data for plotting
# months = header_row[1:]  # Exclude the first column which is 'Stock'
# stock_data = {row[0]: row[1:] for row in data[1:]}
names = []
percentage = []
i = 0
for row in data:
    if i > 1 and row.__len__() > 1:
        names.append(row[0])
        percentage.append(row[3])
        print(row[0], row[3])
    i += 1

# Plot bar chart for each stock

# Convert percentages to float, replacing '-' with 0
values = [float(x.strip('%')) if x != '-' else 0 for x in percentage]

# Create the bar chart
plt.figure(figsize=(15, 8))
bars = plt.bar(names, values, color='skyblue')

# Customize the chart
plt.xlabel('Stocks')
plt.ylabel('Holding Percentage (%)')
plt.title('Portfolio Holdings - October 2024')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add percentage labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}%',
             ha='center', va='bottom')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Show the plot
plt.show()