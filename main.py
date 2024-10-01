import time
import re
import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Function to get the price from the Roblox page
def get_roblox_price(driver, item_id):
    try:
        driver.get(f"https://www.roblox.com/catalog/{item_id}/Bluesteel-Bathysphere")
        time.sleep(0.25)  # Wait for the page to load
        
        try:
            price_element = driver.find_element(By.CLASS_NAME, 'text-price')
        except Exception:
            price_element = driver.find_element(By.XPATH, "//div[contains(@class, 'price')]")
        
        price_text = price_element.text.strip()
        price_match = re.search(r'\d{1,3}(?:\s?\d{3})*', price_text)
        
        if price_match:
            price = int(price_match.group(0).replace(" ", ""))
            print(f"The price of item {item_id} is: {price}")
            return price

    except Exception as e:
        print(f"Error fetching price for item {item_id}: {e}")
    return None

# Function to set cookies for Roblox login
def set_roblox_cookie(driver, cookie_value):
    cookie = {
        'name': '.ROBLOSECURITY',
        'value': cookie_value,
        'domain': '.roblox.com',
        'path': '/',
        'secure': True,
        'httpOnly': True,
    }
    
    driver.get("https://www.roblox.com")
    driver.add_cookie(cookie)

# Function to purchase an item
def purchase_item(driver, item_id):
    try:
        buy_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Buy')]")
        buy_button.click()

        time.sleep(1)

        buy_now_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Buy Now')]")
        buy_now_button.click()
        
        print(f"Successfully purchased item {item_id}!")
    except Exception as e:
        print(f"Error purchasing item {item_id}: {e}")

# Main function to run the script
def main():
  with open("cookies.json") as c:
    cookies = cookies = [line.strip() for line in c.readlines()]
    with open('config.json') as f:
        config = json.load(f)

    items = config["Items"]  # List of items with their max prices
      # List of cookies for different accounts

    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--silent")

    for cookie_value in cookies:
        print(f"Running script for cookie: {cookie_value}")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            set_roblox_cookie(driver, cookie_value)
          def balance():
        robux = requests.get(f'https://economy.roblox.com/v1/user/currency', cookies={'.ROBLOSECURITY': cookie_value}).json()['robux']
        return robux

            for item in items:
                item_id, max_price = item[0], item[1]

                current_price = get_roblox_price(driver, item_id)

                if balance >= max_price:
                    purchase_item(driver, item_id)

                time.sleep(1)  # Small delay between checks

        except KeyboardInterrupt:
            print("Stopping the price checker.")
        finally:
            driver.quit()

# Run the main function
if __name__ == "__main__":
    main()
