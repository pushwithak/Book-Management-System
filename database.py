"""
Name: Pushwitha Krishnappa
Course: CS-521
Python3 Version: Python 3.9.6
Description: Module for managing a SQLite database for a Book Management System (BMS). Includes database setup, user management, and book inventory features.
"""

import sqlite3
import os


class DatabaseSetup:
    """
    Handles SQLite database setup and initial data loading(Users and Books table) for the Book Management System.
    """

    def __init__(self, db_name="book_management.db"):
        """
        Initializes the DatabaseSetup object.

        Args:
            db_name (str): The name of the SQLite database file.
        """
        self.db_name = db_name

    def connect_db(self):
        """
        Connects to the SQLite database.

        Returns:
            sqlite3.Connection: A connection object to the SQLite database.
        """
        return sqlite3.connect(self.db_name)

    def setup_database(self):
        """
        Sets up the database by creating necessary tables and loading initial data from text files.
        """
        conn = self.connect_db()
        cursor = conn.cursor()

        # Create Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL CHECK(user_type IN ('admin', 'user'))
            )
            """
        )

        # Create Books table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                isbn TEXT UNIQUE
            )
            """
        )

        conn.commit()
        self.load_initial_data(cursor)
        conn.commit()
        conn.close()

    def load_initial_data(self, cursor):
        """
        Loads initial data for Users and Books tables from text files.

        Args:
            cursor (sqlite3.Cursor): A cursor object for executing SQL commands.
        """
        # Populate Users table from Users.txt
        if os.path.exists("Users.txt"):
            with open("Users.txt", "r", encoding="utf-8") as file:
                for line in file:
                    username, password, user_type = line.strip().split(",")
                    try:
                        cursor.execute(
                            """
                            INSERT INTO Users (username, password, user_type)
                            VALUES (?, ?, ?)
                            """,
                            (username.strip(), password.strip(), user_type.strip()),
                        )
                    except sqlite3.IntegrityError:
                        print(f"User {username} already exists.")

        # Populate Books table from Books.txt
        if os.path.exists("Books.txt"):
            with open("Books.txt", "r", encoding="utf-8") as file:
                for line in file:
                    title, author, year, isbn = line.strip().split(",")
                    try:
                        cursor.execute(
                            """
                            INSERT INTO Books (title, author, year, isbn)
                            VALUES (?, ?, ?, ?)
                            """,
                            (title.strip(), author.strip(), int(year.strip()), isbn.strip()),
                        )
                    except sqlite3.IntegrityError:
                        print(f"Book {title} already exists.")


if __name__ == "__main__":
    db_setup = DatabaseSetup()
    db_setup.setup_database()
    print("Database setup complete.")