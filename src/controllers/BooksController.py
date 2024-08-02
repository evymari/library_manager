from models.BooksModel import BooksModel
from models.GenresModel import GenresModel


class BooksController:
    def __init__(self):
        self.books_model = BooksModel()
        self.genre_model = GenresModel()

    def add_book(self, book_data):
        try:
            existing_book = self.books_model.get_book_by_isbn(book_data.get("isbn13"))

            if existing_book:
                self.books_model.update_stock(book_data.get("isbn13"))
                print(
                    f"ISBN {book_data["isbn13"]} found. Title: {book_data["title"]} Author:{book_data["author"]}. Stock updated.")
                return dict(status_code=200, message="Book stock updated successfully")
            else:
                book_data["stock"] = 1
                new_book_id = self.books_model.create_book(book_data)
                if new_book_id is not None:
                    print(f"Book added: {book_data["title"]} Book ID: {new_book_id}")
                    return dict(status_code=200, message="Book added successfully")
                else:
                    print("Failed to retrieve the new book ID.")
                    return dict(status_code=500, message="Failed to add book.")
        except Exception as e:
            print(f"Error: {e}")
            return dict(status_code=500, message=f"Error adding book: {e}")

    def search_books(self, search_criteria):
        author = search_criteria["author"]
        title = search_criteria["title"]
        genre_id = search_criteria["genre_id"]
        try:
            result = self.books_model.search_books(author,title,genre_id)
            if result:
                print(f"Bools found: {result}")
                return dict(status_code=200, books=result)
            else:
                print("No books found.")
                return dict(status_code=404, message="No books found.")
        except Exception as e:
               print(f"Error: {e}")
               return dict(status_code=500, message=f"Error searching book: {e}")

