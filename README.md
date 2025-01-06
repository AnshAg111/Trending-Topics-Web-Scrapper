# Trending Topics Web Scrapper

A Flask-based web application that retrieves and displays top five trending topics from Twitter homepage along with metadata and stores query details in a MongoDB database. This project uses Selenium for scraping, Flask for the web framework, and MongoDB for data storage.

---

## Features

- **Homepage**: Displays a link to run the script.
- **TResultsPage**: Displays the top trending topics, query timestamp, and IP address.
- **MongoDB Integration**: Stores the query details in a MongoDB database and displays the JSON record.
- **Selenium Automation**: Fetches the trending topics dynamically from a target source.

---


## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AnshAg111/Trending-Topics-Web-Scrapper.git
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add the following:

```plaintext
MONGO_URI=your_mongodb_connection_string
CHROMEDRIVER_PATH=/path/to/chromedriver
FLASK_SECRET_KEY=your_secret_key
TWITTER_USER=twitter_username
TWITTER_PASS=twitter_password
```

- **MONGO_URI**: MongoDB connection string (e.g., `mongodb://localhost:27017`)
- **CHROMEDRIVER_PATH**: Full path to the ChromeDriver executable.

### ProxyMesh Integration

1. **Set Up ProxyMesh**
   - Create a ProxyMesh account at [ProxyMesh](https://proxymesh.com).
   - Obtain your ProxyMesh credentials (username and password).

2. **Add ProxyMesh Credentials to `.env`**
   ```env
   PROXY_URL=http://<proxy_username>:<proxy_password>@proxy.proxy-mesh.com:8080 (Replace with your proxymesh url)
   PROXY_USER=<your_proxymesh_username>
   PROXY_PASS=<your_proxymesh_password>
   ```

---

### 5. Run the Application

```bash
python app.py
```

Access the app at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Usage

1. Visit the homepage.
2. Click on **"Click here to run the script"**.
3. View the trending topics, query timestamp, IP address, and JSON extract from MongoDB.

---

