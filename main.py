"""
Name: Pushwitha Krishnappa
Course: CS-521
Python3 Version: Python 3.9.6
Description: Main module for running the Book Management System (BMS). Handles user interaction, menu display, and system operations.
"""

import sys
from authentication import Authentication
from book_management import BookManagement

class BookManagementSystem:
    """
    The main system for managing user authentication and book operations in the Book Management System.
    """

    def __init__(self):
        """
        Initializes the BookManagementSystem object.
        """
        self.auth = Authentication()
        self.book_manager = BookManagement()
        self.is_logged_in = False

    def display_menu(self):
        """
        Displays the appropriate menu based on the user's login state and role.
        """
        if not self.is_logged_in:
            print("\nMain Menu:")
            print("1. Login")
            print("2. Exit")
        else:
            user_type = self.auth.current_user[1]
            if user_type == "admin":
                print("\nAdmin Menu:")
                print("1. Add Book")
                print("2. Delete Book")
                print("3. Search Books")
                print("4. Logout")
            elif user_type == "user":
                print("\nUser Menu:")
                print("1. Search Books")
                print("2. Borrow Book")
                print("3. Logout")

    def handle_choice(self, choice):
        """
        Handles the user's choice based on their login state and role.

        Args:
            choice (str): The user's menu selection.
        """
        if not self.is_logged_in:
            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                self.is_logged_in = self.auth.login(username, password)
            elif choice == "2":
                print("Exiting system. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
        else:
            user_type = self.auth.current_user[1]
            if user_type == "admin":
                if choice == "1":
                    title = input("Enter book title: ")
                    author = input("Enter author name: ")
                    year = input("Enter publication year: ")
                    isbn = input("Enter ISBN: ")
                    self.book_manager.add_book(title, author, int(year), isbn)
                elif choice == "2":
                    isbn = input("Enter the ISBN of the book to delete: ")
                    self.book_manager.delete_book(isbn)
                elif choice == "3":
                    print("\nEnter search criteria (leave blank if not applicable):")
                    title = input("Title: ")
                    author = input("Author: ")
                    year = input("Year: ")
                    isbn = input("ISBN: ")
                    self.book_manager.search_books(
                        title=title or None,
                        author=author or None,
                        year=int(year) if year else None,
                        isbn=isbn or None,
                    )
                elif choice == "4":
                    self.auth.logout()
                    self.is_logged_in = False
                else:
                    print("Invalid choice. Please try again.")
            elif user_type == "user":
                if choice == "1":
                    print("\nEnter search criteria (leave blank if not applicable):")
                    title = input("Title: ")
                    author = input("Author: ")
                    year = input("Year: ")
                    isbn = input("ISBN: ")
                    self.book_manager.search_books(
                        title=title or None,
                        author=author or None,
                        year=int(year) if year else None,
                        isbn=isbn or None,
                    )
                elif choice == "2":
                    isbn = input("Enter the ISBN of the book to borrow: ")
                    username = self.auth.current_user[0]
                    self.book_manager.borrow_book(username, isbn)
                elif choice == "3":
                    self.auth.logout()
                    self.is_logged_in = False
                else:
                    print("Invalid choice. Please try again.")

    def run(self):
        """
        Runs the main loop of the Book Management System.
        """
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            self.handle_choice(choice)

if __name__ == "__main__":
    system = BookManagementSystem()
    system.run()
