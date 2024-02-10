from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

def scrape_amazon(asin):
    # Specify the path to your ChromeDriver here
    driver_path = 'chromedriver'  # Update this with the path to your chromedriver executable
    options = Options()
    options.add_argument('--headless')  # Run without graphical interface (optional)

    # Initialize the Chrome browser with the WebDriver
    driver = webdriver.Chrome(options=options)

    # Visit Amazon product page
    url = f"https://www.amazon.com/dp/{asin}"
    driver.get(url)
    time.sleep(2)  # Add a delay to allow page to load

    # Scrape product details
    try:
        product_name = driver.find_element(By.ID, "productTitle").text.strip()
        brand_name = driver.find_element(By.ID, "bylineInfo").text.strip()
        num_reviews = driver.find_element(By.ID, "acrCustomerReviewText").text.split(" ")[0]
        average_rating = driver.find_element(By.CSS_SELECTOR, ".a-icon-star-small > .a-icon-alt").get_attribute("innerHTML").split(" ")[0]
        category = driver.find_element(By.CSS_SELECTOR,"#wayfinding-breadcrumbs_container ul li:nth-last-child(2)").text.strip()
        sub_category = driver.find_element(By.CSS_SELECTOR,"#wayfinding-breadcrumbs_container ul li:last-child").text.strip()
        price_element = driver.find_element(By.CSS_SELECTOR, ".a-price .a-price-whole")
        price_fraction_element = driver.find_element(By.CSS_SELECTOR, ".a-price .a-price-fraction")
        price = f"${price_element.text.strip()}.{price_fraction_element.text.strip()}"

        prod_det_attr_values = driver.find_elements(By.CLASS_NAME, "prodDetAttrValue")
        date_first_available = prod_det_attr_values[-1].text.strip()

        product_dimensions = driver.find_element(By.CSS_SELECTOR, ".prodDetAttrValue").text.strip()
        elements = driver.find_elements(By.CSS_SELECTOR, ".prodDetAttrValue")

        # Extract the text of the second element (index 1)
        weight = elements[1].text.strip()
        # Find all elements with the class name "prodDetAttrValue"



        # Construct JSON
        product_details = {
            "Product Name": product_name,
            "Brand Name": brand_name,
            "Price": price,
            "date_first_available_element" : date_first_available,
            "Number of Reviews": num_reviews,
            "Average Rating": average_rating,
            "Category": category,
            "Sub Category": sub_category,
            "product_dimensions": product_dimensions,
            "weight" : weight,
            #"best_sellers_rank" :best_sellers_rank,

        }

        # Close the WebDriver
        driver.quit()

        return json.dumps(product_details, indent=4)
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
if __name__ == "__main__":


    asin = "B0CMTY9SJ1"  # Example ASIN
    print(scrape_amazon(asin))
