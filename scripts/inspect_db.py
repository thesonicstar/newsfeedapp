import sqlite3
import configparser
import logging
from logging.handlers import RotatingFileHandler
import os

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read("../config.ini")

try:
    LOG_FILE = config.get("LOGGING", "DB_LOG_FILE", fallback="../logs/db-app.log")
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

def inspect_database(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # List all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(f"- {table[0]}")

    # Print the schema for each table
    for table in tables:
        print(f"\nSchema for table {table[0]}:")
        cursor.execute(f"PRAGMA table_info({table[0]});")
        schema = cursor.fetchall()
        for column in schema:
            print(f"  {column[1]} ({column[2]})")

        print(f"\nData in table {table[0]}:")
        #logger.info(f"\nData in table {table[0]}:")
        cursor.execute(f"SELECT * FROM {table[0]}")  # Fetch first 5 rows rows = cursor.fetchall()
        #cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5;")  # Fetch first 5 rows rows = cursor.fetchall()
        logger.info("Query Table Data")
        rows = cursor.fetchall()
        for row in rows:
            logger.info(row)
            print(row)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    db_path = '../instance/bookmarks.db'  # Replace with the path to your database file
    inspect_database(db_path)
