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

table_name = "bookmark"

def delete_data(db_path, table_name, condition):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Delete data from the specified table based on the condition

    delete_query = f"DELETE FROM {table_name} WHERE id = {condition}"

    #empty table
    #delete_query = f"DELETE FROM {table_name}"

    try:
        cursor.execute(delete_query)
        conn.commit()
        logger.info("Delete Table Data")
        logger.debug(delete_query)
        print(f"Data deleted from table {table_name} where id = {condition}.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    db_path = '../instance/bookmarks.db'  # Replace with the path to your database file
    #table_name = input("Enter the table name: ")
    condition = input("Enter the condition for deleting data (e.g., id=1): ")
    delete_data(db_path, table_name, condition)
