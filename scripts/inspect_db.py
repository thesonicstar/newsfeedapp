import sqlite3



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
        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5;")  # Fetch first 5 rows rows = cursor.fetchall()
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    db_path = '../instance/bookmarks.db'  # Replace with the path to your database file
    inspect_database(db_path)
