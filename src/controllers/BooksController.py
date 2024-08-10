from models.BooksModel import BooksModel
from models.GenresModel import GenresModel
from src.validators.BooksValidator import BooksValidator


class BooksController:
    def __init__(self):
        self.books_model = BooksModel()
        self.genres_model = GenresModel()
        self.books_validator = BooksValidator()

    def add_book(self, book_data):
        try:
            self.books_validator.validate_required_fields(book_data)
            if self.books_model.book_data_validator(book_data):
                print("Valid data")
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

    def update_book(self, book_id, update_data):
        try:
            valid_data = self.books_validator.validate_update_data(update_data)

            for required_field in self.books_validator.required_fields:
                if required_field in update_data:
                    self.books_validator.validate_required_fields({required_field: update_data[required_field]})

            updated = self.books_model.update_book(book_id, valid_data)
            if updated:
                return dict(status_code=200, message="Book updated succesfully")
            else:
                return dict(status_code=500, message="Failed to update book")
        except Exception as e:
            print(f"Error updating book: {e}")
            return dict(status_code=500, message=f"Error updating book: {e}")
