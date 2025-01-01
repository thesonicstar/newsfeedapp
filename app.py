from flask import Flask, request, jsonify, render_template
import requests
import configparser  # For reading the config file
import logging
from logging.handlers import RotatingFileHandler
import os


# Load configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

try:
    # Extract Plex token and URL from the config
    NEWSAPI_KEY = config["NEWSAPI"]["NEWS_TOKEN"]
    NEWSAPI_URL = config["NEWSAPI"]["NEWS_URL"]
    PORT = config["CONN"]["PORT"]
    LOG_FILE = config.get("LOGGING", "LOG_FILE", fallback="logs/app.log")
    LOG_LEVEL = config.get("LOGGING", "LOG_LEVEL", fallback="INFO").upper()
    MAX_LOG_SIZE = int(config.get("LOGGING", "MAX_LOG_SIZE", fallback="4")) * 1024 * 1024  # Default: 4MB
    BACKUP_COUNT = int(config.get("LOGGING", "BACKUP_COUNT", fallback="5"))  # Default: 5 backup files


except KeyError as e:
    raise RuntimeError(f"Missing configuration for: {e}")

# Ensure the log directory exists
log_dir = os.path.dirname(LOG_FILE)
os.makedirs(log_dir, exist_ok=True)

# Set up RotatingFileHandler
rotating_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
)
rotating_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
rotating_handler.setFormatter(formatter)

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
logger.addHandler(rotating_handler)



app = Flask(__name__)

# API Key and Endpoint
NEWS_API_KEY = NEWSAPI_KEY
NEWS_API_URL = NEWSAPI_URL

@app.route("/")
def home():
    """Render the home page."""
    logger.info("Serving home page")
    return render_template("index.html")

@app.route('/get_news', methods=['GET'])
def get_news():
    category = request.args.get('category', 'technology')
    response = requests.get(NEWS_API_URL, params={
        'category': category,
        'apiKey': NEWS_API_KEY
    })
    logger.debug(response.json())
    #return jsonify(response.json())

    data = response.json()  # Convert response content to a dictionary
    # Filter out articles with "[Removed]" in the 'name' field
    filtered_articles = [
        article for article in data["articles"] if article["source"]["name"] != "[Removed]"
    ]

    # Update the response
    filtered_response = {
        "status": data["status"],
        "totalResults": len(filtered_articles),  # Update count to match filtered articles
        "articles": filtered_articles,
    }

    # Return the filtered response as JSON
    logger.debug(filtered_response)
    return jsonify(filtered_response)




if __name__ == '__main__':
    #app.run(debug=True)
    logger.info("Starting Flask application")
    app.run(host='0.0.0.0', port=PORT, debug=True)
