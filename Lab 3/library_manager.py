import json
import logging
from pathlib import Path

logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

class LibraryInventory:
    def __init__(self, file_path="catalog.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_data()

    def load_data(self):
        try:
            if self.file_path.exists():
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.books = [Book(**item) for item in data]
            else:
                self.save_data()
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            self.books = []

    def save_data(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([book.to_dict() for book in self.books], f, indent=4)
        except Exception as e:
            logging.error(f"Error saving data: {e}")

    def add_book(self, title, author, isbn):

        if self.search_by_isbn(isbn):
            return False, "A book with this ISBN already exists."
        self.books.append(Book(title, author, isbn))
        logging.info(f"Added book: {title} ({isbn})")
        self.save_data()
        return True, "Book added."

    def search_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def search_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def display_all(self):
        return self.books

    def issue_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if book and book.issue():
            self.save_data()
            logging.info(f"Issued: {isbn}")
            return True
        return False

    def return_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if book and book.return_book():
            self.save_data()
            logging.info(f"Returned: {isbn}")
            return True
        return False

def show_menu():
    print("""
-----------------------------------
        LIBRARY MANAGER
-----------------------------------
1. Add Book
2. Issue Book
3. Return Book
4. View All Books
5. Search Book
6. Exit
-----------------------------------
""")

def run_cli():
    inventory = LibraryInventory()

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            isbn = input("Enter ISBN: ").strip()
            if not (title and author and isbn):
                print("All fields are required.")
                continue
            ok, msg = inventory.add_book(title, author, isbn)
            print(msg)

        elif choice == "2":
            isbn = input("Enter ISBN to issue: ").strip()
            if inventory.issue_book(isbn):
                print("Book issued successfully!")
            else:
                print("Cannot issue book. It may already be issued or ISBN is invalid.")

        elif choice == "3":
            isbn = input("Enter ISBN to return: ").strip()
            if inventory.return_book(isbn):
                print("Book returned successfully!")
            else:
                print("Book not found or not currently issued.")

        elif choice == "4":
            books = inventory.display_all()
            if not books:
                print("No books in catalog.")
            else:
                print("\n--- Library Books ---")
                for book in books:
                    print(book)

        elif choice == "5":
            query = input("Enter title or ISBN to search: ").strip()
            if not query:
                print("Enter a non-empty search query.")
                continue
            book = inventory.search_by_isbn(query)
            if book:
                print(book)
            else:
                results = inventory.search_by_title(query)
                if results:
                    for b in results:
                        print(b)
                else:
                    print("No matching books found.")

        elif choice == "6":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select from 1 to 6.")

if __name__ == "__main__":
    run_cli()
