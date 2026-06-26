from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def scrape_groww_data_selenium(search_query):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    try:
        # Path to your ChromeDriver
        service = Service(r"C:\Users\mohammad nizaamuddin\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")  # Update with your ChromeDriver path
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open the Groww website
        driver.get("https://www.moneycontrol.com/")

        # Wait for the search input field to be visible
        driver.implicitly_wait(5)
        
        # Locate the search input field
        search_box = driver.find_elements(By.CSS_SELECTOR, "li")
        print(search_box)
    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Replace 'Tata' with any search term you want
    scrape_groww_data_selenium("Tata")
