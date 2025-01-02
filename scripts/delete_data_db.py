import sqlite3

table_name = "bookmark"

def delete_data(db_path, table_name, condition):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Delete data from the specified table based on the condition

    delete_query = f"DELETE FROM {table_name} WHERE id = {condition}"
    try:
        cursor.execute(delete_query)
        conn.commit()
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
