"""
Name: Pushwitha Krishnappa
Course: CS-521
Python3 Version: Python 3.9.6
Description: Module to print the database at any given time.
"""

import sqlite3


def print_db_contents(db_name):
    """
    Prints the contents of all tables in the specified SQLite database.

    Args:
        db_name (str): The name of the SQLite database file.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Fetch all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print("No tables found in the database.")
            return

        # Iterate through each table and print its contents
        for table_name in tables:
            table = table_name[0]
            print(f"\nContents of table '{table}':")
            cursor.execute(f"SELECT * FROM {table};")
            rows = cursor.fetchall()

            if rows:
                # Fetch column names for better formatting
                cursor.execute(f"PRAGMA table_info({table});")
                column_names = [column[1] for column in cursor.fetchall()]
                print(f"{', '.join(column_names)}")
                for row in rows:
                    print(row)
            else:
                print("No data found.")

        # Close the database connection
        conn.close()

    except sqlite3.Error as error:
        print(f"Error accessing the database: {error}")


# Call the function with the .db file
print_db_contents("book_management.db")
