from models.BooksModel import BooksModel
from models.GenresModel import GenresModel
from src.data_validators.BooksValidator import BooksValidator


class BooksController:
    def __init__(self):
        self.books_model = BooksModel()
        self.genres_model = GenresModel()
        self.books_validator = BooksValidator()

    def add_book(self, book_data):
        try:
            valid_data = self.books_validator.book_data_validator(book_data)
            existing_book = self.books_model.get_book_by_isbn(book_data.get("isbn13"))

            if existing_book:
                self.books_model.update_stock(valid_data.get("isbn13"))
                print(
                    f"ISBN {book_data["isbn13"]} found. Title: {book_data["title"]} Author:{book_data["author"]}. Stock updated.")
                return dict(status_code=200, message="Book stock updated successfully")
            else:
                book_data["stock"] = 1
                new_book_id = self.books_model.create_book(valid_data)
                if new_book_id is not None:
                    print(f"Book added: {book_data["title"]} Book ID: {new_book_id}")
                    return dict(status_code=200, message="Book added successfully")
                else:
                    print("Failed to retrieve the new book ID.")
                    return dict(status_code=500, message="Failed to add book.")
        except (KeyError, ValueError, TypeError) as e:
            print(f"Validation error: {e}")
            return dict(status_code=400, message=f"Validation error: {e}")
        except Exception as e:
            print(f"Error: {e}")
            return dict(status_code=500, message=f"Error adding book: {e}")

    def update_book(self, book_id, update_data):
        try:
            valid_fields = self.books_validator.validate_update_data(update_data)
            updated = self.books_model.update_book(book_id, valid_fields)
            if updated:
                return dict(status_code=200, message="Book updated successfully")
            else:
                return dict(status_code=500, message="Failed to update book")
        except (KeyError, ValueError, TypeError) as e:
            print(f"Validation error: {e}")
            return dict(status_code=400, message=f"Validation error: {e}")
        except Exception as e:
            print(f"Error updating book: {e}")
            return dict(status_code=500, message=f"Error updating book: {e}")
