from flask import Flask, render_template, request
from script import fetch_trending_topics  
from datetime import datetime 
import json
from dotenv import load_dotenv
from pymongo import MongoClient
import os  

app = Flask(__name__)
load_dotenv()
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
app.secret_key = FLASK_SECRET_KEY
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db_name = "twitter_scraper"
COLLECTION_NAME = "trending_topics" 
db = client[db_name]
collection=db[COLLECTION_NAME]
latest_record = collection.find_one(sort=[("timestamp", -1)])

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/run_script")
def run_script():
    trends, ip_address, timestamp = fetch_trending_topics()
    return render_template(
        "results.html",
        trends=trends,
        ip_address=ip_address,
        timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        json_record=json.dumps(latest_record, indent=4)
    )

if __name__ == "__main__":
    app.run(debug=True)