# News Feed App

This is a Flask-based web application that allows users to fetch news articles, bookmark their favorites, and manage the bookmarks.

## Features

- **Fetch News Articles**: Users can fetch articles by category using the News API.
- **Bookmark Articles**: Save articles for later reading.
- **Manage Bookmarks**: View and delete bookmarked articles.
- **Dark Mode**: Toggle between light and dark themes.
- **Toast Notifications**: User-friendly toast notifications for feedback.

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- Virtual environment (optional but recommended)
- SQLite (default database)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/bookmark-manager.git
   cd bookmark-manager
   ```

2. **Set Up a Virtual Environment** (optional):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Configuration**:
   Create a `config.ini` file in the root directory with the following content:
   ```ini
   [NEWSAPI]
   NEWS_TOKEN=your_newsapi_key
   NEWS_URL=https://newsapi.org/v2/top-headlines

   [CONN]
   PORT=5000

   [LOGGING]
   LOG_FILE=logs/app.log
   LOG_LEVEL=INFO
   MAX_LOG_SIZE=4  # in MB
   BACKUP_COUNT=5
   ```
   Replace `your_newsapi_key` with your [NewsAPI](https://newsapi.org/) key.

5. **Initialize the Database**:
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

6. **Run the Application**:
   ```bash
   python app.py
   ```
   Access the app at `http://127.0.0.1:5000/`.

## Folder Structure

```
bookmark-manager/
├── static/
│   ├── images/        # Default and favicon images
│   ├── styles.css     # Custom CSS for styling
│   ├── script.js      # JavaScript for main page
│   └── bookmarks.js   # JavaScript for bookmarks page
├── templates/
│   ├── index.html     # Main page template
│   └── bookmarks.html # Bookmarks page template
├── app.py             # Flask application
├── models.py          # Database models
├── requirements.txt   # Python dependencies
└── README.md          # Documentation (this file)
```

## Usage

### Fetch News
1. Open the app and select a category (e.g., Technology, Sports, Politics).
2. Click `Get News` to fetch articles from the News API.

### Bookmark an Article
1. Click the `Bookmark` button on any article.
2. A toast notification confirms the action.

### View Bookmarked Articles
1. Navigate to the "Bookmarks" tab or page.
2. View all saved articles.

### Delete a Bookmark
1. Click the `Delete` button on a bookmarked article.
2. The article will be removed from the list.

## Logging

Logs are stored in the `logs/app.log` file and rotate based on the configuration in `config.ini`.

## Known Issues

- Ensure the News API key is valid to fetch articles.
- Bookmarked articles with the same URL cannot be saved multiple times.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
