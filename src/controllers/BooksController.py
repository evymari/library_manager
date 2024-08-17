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
                self.books_model.update_stock_by_isbn13(valid_data.get("isbn13"))
                print(
                    f"ISBN {book_data["isbn13"]} already exists. Title: {book_data["title"]} Author:{book_data["author"]}. Stock will be updated by 1.")
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


    def validate_search_criteria(self,search_criteria):
        required_keys = {
            "author": (str, type(None)),
            "title": (str, type(None)),
            "isbn13": (str, type(None)),
            "original_publication_year": (str, type(None)),  # Allow int or None
            "availability": (bool, type(None)),
            "best_seller": (bool, type(None)),
            "entry_date": (str, type(None)),  # Assuming date is provided as string in 'YYYY-MM-DD' format
            "genre_name": (str, type(None))
        }

        for key, expected_type in required_keys.items():
            if key not in search_criteria:
                raise ValueError(f"Missing key: {key}")
            if not isinstance(search_criteria[key], expected_type):
                raise ValueError(
                    f"Invalid type for key {key}: expected {expected_type}, got {type(search_criteria[key])}")

        return True

    def search_books(self, search_criteria):
        try:
            # Validate search criteria
            self.validate_search_criteria(search_criteria)

            author = search_criteria["author"]
            title = search_criteria["title"]
            isbn13 = search_criteria["isbn13"]
            original_publication_year = search_criteria["original_publication_year"]
            availability = search_criteria["availability"]
            best_seller = search_criteria["best_seller"]
            entry_date = search_criteria["entry_date"]

            genre_name = search_criteria.get("genre_name")  # Retrieve genre_name with default value of None

            genre_id = self.genre_model.get_genre_id(genre_name) if genre_name else None
            result = self.books_model.search_books(
                author, title, genre_id, isbn13, original_publication_year,
                availability, best_seller, entry_date
            )

            if result:
                print(f"Books found: {result}")
                return dict(status_code=200, books=result)
            else:
                print("No books found.")
                return dict(status_code=404, message="No books found.")
        except ValueError as ve:
            print(f"Validation Error: {ve}")
            return dict(status_code=400, message=f"Validation Error: {ve}")
        except Exception as e:
            print(f"Error: {e}")
            return dict(status_code=500, message=f"Error searching book: {e}")

            return dict(status_code=500, message=f"Error searching book: {e}")

    def delete_book(self, isbn13):
        try:
            # Verificar si el libro existe en la base de datos
            existing_book = self.books_model.get_book_by_isbn(isbn13)

            if existing_book:
                # Si el libro existe, eliminarlo de la base de datos
                self.books_model.remove_book(isbn13)
                print(f"Book with ISBN {isbn13} has been deleted.")
                return dict(status_code=200, message="Book deleted successfully")
            else:
                print(f"No book found with ISBN {isbn13}.")
                return dict(status_code=404, message="Book not found")
        except Exception as e:
            print(f"Error: {e}")
            return dict(status_code=500, message=f"Error deleting book: {e}")