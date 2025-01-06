from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import requests
import pymongo
import uuid
from datetime import datetime
from dotenv import load_dotenv
import os  
from app import db_name, COLLECTION_NAME

load_dotenv()
MONGO_URI=os.getenv('MONGO_URI')
TWITTER_USER=os.getenv('TWITTER_USER')
TWITTER_PASS=os.getenv('TWITTER_PASS')
PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASS = os.getenv('PROXY_PASS')
PROXY_URL = os.getenv('PROXY_URL')

# Selenium setup with Proxy
def setup_driver():
    options = Options()
    options.add_argument('--proxy-server=%s' % PROXY_URL)
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu') 
    driver = webdriver.Chrome(options=options)
    return driver

def fetch_trending_topics():
    driver = setup_driver()
    driver.get("https://twitter.com/login")
    driver.maximize_window()
    time.sleep(3)
    email=driver.find_element(By.XPATH, "//input[@name='text']")
    email.send_keys(TWITTER_USER)
    driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]").click()
    time.sleep(3)
    password=driver.find_element(By.XPATH, "//input[@name='password']")
    password.send_keys(TWITTER_PASS)
    log_in=driver.find_element(By.XPATH, "//span[contains(text(), 'Log in')]")
    log_in.click()
    time.sleep(3)
    trending_section = driver.find_element(By.XPATH, '//section[contains(@aria-labelledby,"accessible-list")]')
    trends = trending_section.find_elements(By.XPATH, "//div[@data-testid='trend']")
    top_trends = [trend.text.split('\n')[0] for trend in trends[:5]] 
    ip_address = requests.get('https://api64.ipify.org?format=json', proxies={"http": PROXY_URL}).json()['ip']
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now()
    
    client = pymongo.MongoClient(MONGO_URI)
    db = client[db_name]
    collection = db[COLLECTION_NAME]
    collection.insert_one({
        "unique_id": unique_id,
        "trends": top_trends,
        "timestamp": timestamp,
        "ip_address": ip_address
    })

    driver.quit()
    return top_trends, ip_address, timestamp

if __name__ == "__main__":
    trends, ip, timestamp = fetch_trending_topics()
    print(f"Trends: {trends}")
    print(f"IP: {ip}")
    print(f"Timestamp: {timestamp}")
