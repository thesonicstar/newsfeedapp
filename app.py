from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import configparser
import logging
from logging.handlers import RotatingFileHandler
import os
from models import db, Bookmark  # Import the database and models
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text


# Load configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

try:
    NEWSAPI_KEY = config["NEWSAPI"]["NEWS_TOKEN"]
    NEWSAPI_URL = config["NEWSAPI"]["NEWS_URL"]
    GOOGLEAPI_NEWS_TOKEN = config["GOOGLEAPI"]["GOOGLEAPI_NEWS_TOKEN"]
    PORT = config["CONN"]["PORT"]
    LOG_FILE = config.get("LOGGING", "LOG_FILE", fallback="logs/app.log")
    LOG_LEVEL = config.get("LOGGING", "LOG_LEVEL", fallback="INFO").upper()
    MAX_LOG_SIZE = int(config.get("LOGGING", "MAX_LOG_SIZE", fallback="4")) * 1024 * 1024
    BACKUP_COUNT = int(config.get("LOGGING", "BACKUP_COUNT", fallback="5"))
except KeyError as e:
    raise RuntimeError(f"Missing configuration for: {e}")

log_dir = os.path.dirname(LOG_FILE)
os.makedirs(log_dir, exist_ok=True)

rotating_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
)
rotating_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
rotating_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
logger.addHandler(rotating_handler)

app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
db.init_app(app)


with app.app_context():
    db.create_all()

def check_db_connection():
    try:
        with app.app_context():
            # Attempt a simple query to check database connection
            db.session.execute(text('SELECT 1'))
        logger.info("Database is up and running")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {e}")
        return False


@app.route("/")
def home():
    logger.info("Serving home page")
    return render_template("index.html")

@app.route('/get_news', methods=['GET'])
def get_news():
    category = request.args.get('category', 'technology')
    response = requests.get(NEWSAPI_URL, params={
        'category': category,
        'apiKey': NEWSAPI_KEY
    })
    data = response.json()
    filtered_articles = [
        article for article in data["articles"] if article["source"]["name"] != "[Removed]"
    ]
    filtered_response = {
        "status": data["status"],
        "totalResults": len(filtered_articles),
        "articles": filtered_articles,
    }
    return jsonify(filtered_response)

@app.route('/bookmark', methods=['POST'])
def bookmark_article():
    data = request.json
    logger.debug(data)

    # Check if the article URL already exists in the database
    existing_bookmark = Bookmark.query.filter_by(url=data.get('url')).first()
    if existing_bookmark:
        return jsonify({"message": "Article has already been bookmarked"}), 200

    new_bookmark = Bookmark(
        title=data.get('title'),
        description=data.get('description'),
        url=data.get('url'),
        source_name=data.get('source_name')
    )
    logger.debug(new_bookmark)
    try:
        db.session.add(new_bookmark)
        db.session.commit()
        return jsonify({"message": "Article bookmarked successfully"}), 201
    except Exception as e:
        return jsonify({"error": "Could not bookmark article"}), 400


@app.route('/bookmarks')
def bookmarks_page():
    """Render the bookmarks page."""
    return render_template('bookmarks.html')

@app.route('/get_bookmarks', methods=['GET'])
def get_bookmarks():
    """Fetch all bookmarked articles from the database."""
    try:
        bookmarks = Bookmark.query.all()
        bookmarks_list = [
            {
                "id": bookmark.id,
                "title": bookmark.title,
                "description": bookmark.description,
                "url": bookmark.url,
                "source_name": bookmark.source_name
            }
            for bookmark in bookmarks
        ]
        logger.debug(bookmarks_list)
        return jsonify(bookmarks_list), 200
    except Exception as e:
        logger.error(f"Error fetching bookmarks: {e}")
        return jsonify({"error": "Failed to fetch bookmarks"}), 500

@app.route('/delete_bookmark/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    """Delete a specific bookmark."""
    try:
        bookmark = Bookmark.query.get(bookmark_id)
        if not bookmark:
            return jsonify({"error": "Bookmark not found"}), 404

        db.session.delete(bookmark)
        db.session.commit()
        logger.debug(bookmark)
        return jsonify({"message": "Bookmark deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting bookmark: {e}")
        return jsonify({"error": "Failed to delete bookmark"}), 500

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        description = request.form.get('description')
        url = request.form.get('url')
        source_name = request.form.get('source')

        # Save to the database
        new_article = Bookmark(title=title, description=description, url=url, source_name=source_name)
        try:
            db.session.add(new_article)
            db.session.commit()
            return jsonify({"message": "Article added successfully!"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Error adding article"}), 400

    # Render the HTML form
    return render_template('add_article.html')

#@app.route('/google_news_page', methods=['GET'])
#def google_news_page():
#   return render_template('google_news.html')


@app.route('/google_news_data', methods=['GET'])
def google_news():
    api_url = f"https://newsapi.org/v2/top-headlines?category=technology&apiKey={GOOGLEAPI_NEWS_TOKEN}"
    response = requests.get(api_url)
    return jsonify(response.json())
    #return render_template('google_news.html')

@app.route('/google_news', methods=['GET'])
def google_news_page():
    return render_template('google_news.html')  # Sends the HTML file to the client



if __name__ == '__main__':
    if check_db_connection():
        print("Database is up and running")
    else:
        print("Database connection error")
    app.run(host='0.0.0.0', port=PORT, debug=True)
