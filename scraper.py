from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from datetime import datetime
import uuid

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "twitter_trends"
COLLECTION_NAME = "trending_topics"

# ProxyMesh Configuration
PROXY_URL = "http://username:password@us-west.proxy.mesh.com:31280"  # Replace with your ProxyMesh details

# WebDriver Configuration
def get_driver(proxy):
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument("--headless")  # Run headless for production
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Fetch Twitter Trends
def fetch_twitter_trends(driver):
    url = "https://twitter.com/home"  # Local Twitter home page URL
    driver.get(url)
    driver.implicitly_wait(10)
    
    # Find trending topics under "What’s Happening"
    trending_section = driver.find_element(By.XPATH, '//section[contains(@aria-labelledby, "accessible-list")]')
    trending_topics = trending_section.find_elements(By.XPATH, './/span')[:5]  # Adjust if structure changes
    
    # Extract text of the trends
    trends = [trend.text for trend in trending_topics if trend.text][:5]
    return trends

# Store Data in MongoDB
def store_data_to_mongodb(trends, ip_address):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    unique_id = str(uuid.uuid4())
    end_time = datetime.now()
    data = {
        "unique_id": unique_id,
        "trend1": trends[0] if len(trends) > 0 else None,
        "trend2": trends[1] if len(trends) > 1 else None,
        "trend3": trends[2] if len(trends) > 2 else None,
        "trend4": trends[3] if len(trends) > 3 else None,
        "trend5": trends[4] if len(trends) > 4 else None,
        "date_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": ip_address
    }
    collection.insert_one(data)
    print(f"Data stored with unique ID: {unique_id}")
    client.close()

# Main Script
if __name__ == "__main__":
    driver = get_driver(PROXY_URL)
    try:
        ip_address = driver.execute_script("return document.URL")  # Replace with IP fetch if needed
        trends = fetch_twitter_trends(driver)
        store_data_to_mongodb(trends, ip_address)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()
