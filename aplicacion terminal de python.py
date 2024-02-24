import pickle
from datetime import datetime
from typing import List
from pydantic import BaseModel

# Define Pydantic models
class Book(BaseModel):
    title: str
    author: str
    available: bool = True

class User(BaseModel):
    name: str
    user_id: int

class Loan(BaseModel):
    book: Book
    user: User
    loan_date: datetime = datetime.now()

# Library class to manage operations
class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.loans = []

    def add_book(self, title: str, author: str):
        book = Book(title=title, author=author)
        self.books.append(book)

    def show_books(self):
        for idx, book in enumerate(self.books, start=1):
            print(f"{idx}. {book.title} by {book.author} - Available: {book.available}")

    def lend_book(self, book_idx: int, user_id: int):
        if book_idx < 0 or book_idx >= len(self.books):
            print("Invalid book index.")
            return

        book = self.books[book_idx]
        if not book.available:
            print("Book is not available for lending.")
            return

        user = next((user for user in self.users if user.user_id == user_id), None)
        if user is None:
            print("User not found.")
            return

        book.available = False
        loan = Loan(book=book, user=user)
        self.loans.append(loan)
        print(f"{book.title} is now borrowed by {user.name}")

    def register_user(self, name: str, user_id: int):
        user = User(name=name, user_id=user_id)
        self.users.append(user)

    def save_data(self, filename: str):
        with open(filename, "wb") as f:
            pickle.dump((self.books, self.users, self.loans), f)
        print("Data saved successfully.")

    def load_data(self, filename: str):
        try:
            with open(filename, "rb") as f:
                self.books, self.users, self.loans = pickle.load(f)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No existing data found.")

    def list_users(self):
        for user in self.users:
            print(f"User ID: {user.user_id}, Name: {user.name}")

    def list_users_books(self, user_id: int):
        user_books = [loan.book for loan in self.loans if loan.user.user_id == user_id]
        if user_books:
            print(f"Books borrowed by user {user_id}:")
            for book in user_books:
                print(f"{book.title} by {book.author}")
        else:
            print("No books borrowed by this user.")

    def return_books(self, user_id: int):
        returned_books = []
        for loan in self.loans:
            if loan.user.user_id == user_id:
                loan.book.available = True
                returned_books.append(loan.book)
        self.loans = [loan for loan in self.loans if loan.user.user_id != user_id]
        if returned_books:
            print(f"Books returned by user {user_id}:")
            for book in returned_books:
                print(f"{book.title} by {book.author}")
        else:
            print("No books returned by this user.")

# Main function to run the application
def main():
    library = Library()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Show Books")
        print("3. Lend Book")
        print("4. Register User")
        print("5. Save Data")
        print("6. Load Data")
        print("7. List Users")
        print("8. List User's Books")
        print("9. Return Books")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            library.add_book(title, author)

        elif choice == "2":
            library.show_books()

        elif choice == "3":
            book_idx = int(input("Enter book index to lend: "))
            user_id = int(input("Enter user ID: "))
            library.lend_book(book_idx - 1, user_id)

        elif choice == "4":
            name = input("Enter user name: ")
            user_id = int(input("Enter user ID: "))
            library.register_user(name, user_id)

        elif choice == "5":
            filename = input("Enter filename to save data: ")
            library.save_data(filename)

        elif choice == "6":
            filename = input("Enter filename to load data: ")
            library.load_data(filename)

        elif choice == "7":
            library.list_users()

        elif choice == "8":
            user_id = int(input("Enter user ID to list books: "))
            library.list_users_books(user_id)

        elif choice == "9":
            user_id = int(input("Enter user ID to return books: "))
            library.return_books(user_id)

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
