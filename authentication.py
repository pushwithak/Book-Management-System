"""
Name: Pushwitha Krishnappa
Course: CS-521
Python3 Version: Python 3.9.6
Description: Module for user authentication in the Book Management System (BMS). Includes login, logout, and role-checking functionalities.
"""

import sqlite3

class Authentication:
    """
    Handles user authentication, including login, logout, and role-based access control for the Book Management System.
    """

    def __init__(self, db_name="book_management.db"):
        """
        Initializes the Authentication object.

        Args:
            db_name (str): The name of the SQLite database file.
        """
        self.db_name = db_name
        self.current_user = None

    def connect_db(self):
        """
        Connects to the SQLite database.

        Returns:
            sqlite3.Connection: A connection object to the SQLite database.
        """
        return sqlite3.connect(self.db_name)

    def login(self, user_name, user_password):
        """
        Logs in a user by validating their credentials.

        Args:
            user_name (str): The username of the user.
            user_password (str): The password of the user.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT username, user_type FROM Users WHERE username = ? AND password = ?
            """,
            (user_name, user_password),
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            self.current_user = user
            print(f"Login successful! Welcome, {user_name} ({user[1]}).")
            return True

        print("Invalid username or password.")
        return False

    def logout(self):
        """
        Logs out the current user.
        """
        if self.current_user:
            print(f"Goodbye, {self.current_user[0]}!")
            self.current_user = None
        else:
            print("No user is currently logged in.")

    def is_admin(self):
        """
        Checks if the current user has admin privileges.

        Returns:
            bool: True if the current user is an admin, False otherwise.
        """
        return self.current_user and self.current_user[1] == "admin"

    def is_user(self):
        """
        Checks if the current user is a regular user.

        Returns:
            bool: True if the current user is a regular user, False otherwise.
        """
        return self.current_user and self.current_user[1] == "user"

if __name__ == "__main__":
    # Entry point for running the authentication module as a standalone script.
    auth = Authentication()

    while True:
        print("\nOptions:")
        print("1. Login")
        print("2. Logout")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            user_name = input("Enter username: ")
            user_password = input("Enter password: ")
            auth.login(user_name, user_password)
        elif choice == "2":
            auth.logout()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
