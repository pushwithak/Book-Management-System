"""
Name: Pushwitha Krishnappa
Course: CS-521
Python3 Version: Python 3.9.6
Description: Module for managing books in the Book Management System (BMS). Includes functionality for adding, deleting, searching, borrowing, and listing borrowed books.
"""

import sqlite3

class BookManagement:
    """
    Handles book management operations, including adding, deleting, searching, borrowing, and listing borrowed books.
    """

    def __init__(self, db_name="book_management.db"):
        """
        Initializes the BookManagement object.

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

    def add_book(self, book_title, book_author, publication_year, book_isbn):
        """
        Adds a new book to the database.

        Args:
            book_title (str): The title of the book.
            book_author (str): The author of the book.
            publication_year (int): The publication year of the book.
            book_isbn (str): The ISBN of the book.
        """
        conn = self.connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO Books (title, author, year, isbn)
                VALUES (?, ?, ?, ?)
                """,
                (book_title, book_author, publication_year, book_isbn),
            )
            conn.commit()
            print(f"Book '{book_title}' added successfully!")
        except sqlite3.IntegrityError:
            print("Book with this ISBN already exists.")
        finally:
            conn.close()

    def delete_book(self, book_isbn):
        """
        Deletes a book from the database using its ISBN.

        Args:
            book_isbn (str): The ISBN of the book to delete.
        """
        conn = self.connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM Books WHERE isbn = ?
                """,
                (book_isbn,),
            )
            if cursor.rowcount > 0:
                conn.commit()
                print(f"Book with ISBN {book_isbn} deleted successfully.")
            else:
                print(f"No book found with ISBN {book_isbn}.")
        except sqlite3.Error as error:
            print(f"An error occurred: {error}")
        finally:
            conn.close()

    def search_books(self, **kwargs):
        """
        Searches for books in the database based on criteria.

        Args:
            **kwargs: Search criteria such as title, author, year, or isbn.
        """
        conn = self.connect_db()
        cursor = conn.cursor()

        query = "SELECT * FROM Books WHERE 1=1"
        params = []

        for key, value in kwargs.items():
            if value:
                query += f" AND {key} = ?"
                params.append(value)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        if results:
            print("\nBooks Found:")
            for book in results:
                print(f"Title: {book[1]}, Author: {book[2]}, Year: {book[3]}, ISBN: {book[4]}")
        else:
            print("No books match your criteria.")

    def borrow_book(self, user_name, book_isbn):
        """
        Allows a user to borrow a book by ISBN.

        Args:
            user_name (str): The name of the user borrowing the book.
            book_isbn (str): The ISBN of the book to borrow.
        """
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM Books WHERE isbn = ?
            """,
            (book_isbn,),
        )
        book = cursor.fetchone()

        if book:
            try:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS BorrowedBooks (
                        username TEXT NOT NULL,
                        book_title TEXT NOT NULL
                    )
                    """
                )
                cursor.execute(
                    """
                    INSERT INTO BorrowedBooks (username, book_title)
                    VALUES (?, ?)
                    """,
                    (user_name, book[1]),
                )
                conn.commit()
                print(f"{user_name} has borrowed '{book[1]}'.")
            except sqlite3.Error as error:
                print(f"An error occurred: {error}")
        else:
            print("Book not found.")

        conn.close()

    def list_borrowed_books(self):
        """
        Lists all borrowed books from the database.

        Returns:
            list: A list of tuples containing the username and book title.
        """
        conn = self.connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT username, book_title FROM BorrowedBooks
                """
            )
            borrowed_books = cursor.fetchall()
            if borrowed_books:
                print("\nBorrowed Books:")
                for user_name, book_title in borrowed_books:
                    print(f"User: {user_name}, Book: {book_title}")
            else:
                print("No books are currently borrowed.")
        except sqlite3.Error as error:
            print(f"An error occurred: {error}")
        finally:
            conn.close()

if __name__ == "__main__":
    book_manager = BookManagement()

    while True:
        print("\nBook Management Options:")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. Search Books")
        print("4. Borrow Book")
        print("5. List Borrowed Books")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            year = input("Enter publication year: ")
            isbn = input("Enter ISBN: ")
            book_manager.add_book(title, author, int(year), isbn)
        elif choice == "2":
            isbn = input("Enter the ISBN of the book to delete: ")
            book_manager.delete_book(isbn)
        elif choice == "3":
            print("\nEnter search criteria (leave blank to display all books):")
            title = input("Title: ")
            author = input("Author: ")
            year = input("Year: ")
            isbn = input("ISBN: ")
            book_manager.search_books(
                title=title or None,
                author=author or None,
                year=int(year) if year else None,
                isbn=isbn or None,
            )
        elif choice == "4":
            username = input("Enter your username: ")
            isbn = input("Enter the ISBN of the book to borrow: ")
            book_manager.borrow_book(username, isbn)
        elif choice == "5":
            book_manager.list_borrowed_books()
        elif choice == "6":
            print("Exiting Book Management. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")