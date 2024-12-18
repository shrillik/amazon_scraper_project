from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import json

# Constants
BEST_SELLER_URL = "https://www.amazon.in/gp/bestsellers/"
CATEGORIES = [
    "https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_nav_kitchen_0",
    "https://www.amazon.in/gp/bestsellers/shoes/ref=zg_bs_nav_shoes_0",
    "https://www.amazon.in/gp/bestsellers/computers/ref=zg_bs_nav_computers_0",
    "https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0"
    # Add more category URLs as needed
]
OUTPUT_FILE = "amazon_best_sellers.json"

# Initialize Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)


def login_to_amazon(email, password):
    try:
        driver.get("https://www.amazon.in/ap/signin")

        # Enter email
        email_field = wait.until(EC.presence_of_element_located((By.ID, "ap_email")))
        email_field.send_keys(email)
        email_field.send_keys(Keys.RETURN)

        # Enter password
        password_field = wait.until(EC.presence_of_element_located((By.ID, "ap_password")))
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # Verify login success
        wait.until(EC.presence_of_element_located((By.ID, "nav-link-accountList")))
        print("Login successful!")

    except TimeoutException:
        print("Login failed. Please check your credentials.")
        driver.quit()
        exit()


def scrape_category(category_url):
    driver.get(category_url)
    scraped_data = []

    try:
        products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.zg-grid-general-faceout")))

        for product in products[:1500]:
            try:
                name = product.find_element(By.CSS_SELECTOR, "div.p13n-sc-truncate-desktop-type2").text
                price = product.find_element(By.CSS_SELECTOR, "span.p13n-sc-price").text
                discount = product.find_element(By.CSS_SELECTOR, "span.zg-badge-text").text if product.find_element(By.CSS_SELECTOR, "span.zg-badge-text") else ""
                rating = product.find_element(By.CSS_SELECTOR, "span.a-icon-alt").text if product.find_element(By.CSS_SELECTOR, "span.a-icon-alt") else ""
                seller = "Amazon"  # Placeholder for ship from and sold by; needs dynamic identification
                ship_from = "Amazon"
                description = "N/A"  # Needs further inspection
                num_bought = "N/A"  # Needs further inspection
                images = [img.get_attribute("src") for img in product.find_elements(By.CSS_SELECTOR, "img")]

                # Filter for discounts > 50%
                if discount and int(discount.strip('%')) > 50:
                    scraped_data.append({
                        "Product Name": name,
                        "Product Price": price,
                        "Sale Discount": discount,
                        "Best Seller Rating": rating,
                        "Ship From": ship_from,
                        "Sold By": seller,
                        "Rating": rating,
                        "Product Description": description,
                        "Number Bought in the Past Month": num_bought,
                        "Category Name": category_url.split("/")[-2],
                        "All Available Images": images
                    })

            except NoSuchElementException:
                print("A product element was missing details.")

    except TimeoutException:
        print("Could not load products for category: ", category_url)

    return scraped_data


def main():
    email = input("Enter your Amazon email: ")
    password = input("Enter your Amazon password: ")
    login_to_amazon(email, password)

    all_data = []
    for category in CATEGORIES:
        print(f"Scraping category: {category}")
        category_data = scrape_category(category)
        all_data.extend(category_data)

    # Save data to JSON file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)

    print(f"Data saved to {OUTPUT_FILE}")
    driver.quit()


if __name__ == "__main__":
    main()
