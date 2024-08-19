from config.DBConnection import DBConnection
from models.GenresModel import GenresModel


class BooksModel:
    def __init__(self):
        self.db = DBConnection()
        self.genre_model = GenresModel()

    def create_book(self, book_data):
        try:
            query = ("INSERT INTO books(stock, isbn13, author, original_publication_year, title, summary, genre_id, "
                     "availability, best_seller) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING book_id")
            params = (book_data.get("stock", None),
                      book_data.get("isbn13"),
                      book_data.get("author"),
                      book_data.get("original_publication_year", None),
                      book_data.get("title"),
                      book_data.get("summary", None),
                      book_data.get("genre_id", None),
                      book_data.get("availability", True),
                      book_data.get("best_seller", False))
            result = self.db.execute_query(query, params)  # result returns a list of tuples [(123,)]
            if result:
                return result[0][0]  # access first item in row and column of tuple
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    # try-except is used to handle errors during database operations like connection issues, SQL errors or data
    # processing if-else is conditional logic to handle scenarios based on outcome of the operation or checks

    def get_book_by_isbn(self, isbn13):
        try:
            query = "SELECT book_id, stock FROM books WHERE isbn13 = %s;"
            params = (isbn13,)
            result = self.db.execute_query(query, params)
            return result
        except Exception as e:
            print(f"Error: {e}")

    def update_stock_by_isbn13(self, isbn13):
        try:
            query = "UPDATE books SET stock = stock + 1 WHERE isbn13 = %s;"
            params = (isbn13,)
            self.db.execute_CUD_query(query, params)
        except Exception as e:
            print(f"Error: {e}")

    def search_books(self, author=None, title=None, genre_id=None, isbn13=None, original_publication_year=None,
                     availability=None, best_seller=None, entry_date=None):

        try:
            query = ("SELECT book_id, stock, isbn13, author, original_publication_year, title, summary, genre_id, "
                     "availability, best_seller FROM books WHERE 1=1 ")
            params = []
            if author:
                query += " AND author ILIKE %s"
                params.append(f"%{author}%")
            if title:
                query += " AND title ILIKE %s"
                params.append(f"%{title}%")
            if genre_id:
                query += "AND genre_id = %s"
                params.append(f"{genre_id}")
            if isbn13:
                query += "AND isbn13 = %s"
                params.append(f"{isbn13}")
            if original_publication_year:
                query += "AND original_publication_year = %s"
                params.append(f"{original_publication_year}")
            if availability:
                query += "AND availability = %s"
                params.append(f"{availability}")
            if best_seller:
                query += "AND best_seller = %s"
                params.append(f"{best_seller}")
            if entry_date:
                query += "AND entry_date = %s"
                params.append(f"{entry_date}")
            result = self.db.execute_query(query, params)

            return result
        except Exception as e:
            print(f"Error: {e}")

    def get_book_stock(self, book_id):
        try:
            query = "SELECT stock FROM books WHERE book_id = %s"
            result = self.db.execute_query(query, (book_id,))
            if result:
                return result[0][0]
            return None
        except Exception as e:
            print(f"Error retrieving book stock: {e}")
            return None

    def update_stock_by_id(self, book_id, amount):
        try:
            query = "UPDATE books SET stock = stock + %s WHERE book_id = %s RETURNING stock;"
            params = (amount, book_id)
            book_stock = self.db.execute_CUD_query(query, params)

            if book_stock is None:
                raise ValueError("Failed to update stock, rows_affected is None")

            return book_stock
        except Exception as e:
            print(f"Error updating stock for book ID {book_id}: {e}")
            return False
    def delete_book(self, isbn13):
        try:
            # Consulta SQL para eliminar un libro basado en el ISBN
            query = "DELETE FROM books WHERE isbn13 = %s RETURNING book_id"
            params = (isbn13,)

            # Ejecutar la consulta
            result = self.db.execute_query(query, params)  # result returns a list of tuples [(123,)]

            # Verificar si el libro fue eliminado
            if result:
                print(f"Book with ISBN {isbn13} has been deleted. Book ID: {result[0][0]}")
                return result[0][0]  # Devuelve el ID del libro eliminado
            else:
                print(f"No book found with ISBN {isbn13}.")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def update_book(self, book_id, update_data):
        try:
            update_fields = []
            params = []
            allowed_fields = {
                "stock": "stock = %s",
                "isbn13": "isbn13 = %s",
                "author": "author = %s",
                "original_publication_year": "original_publication_year = %s",
                "title": "title = %s",
                "summary": "summary = %s",
                "genre_id": "genre_id = %s",
                "availability": "availability = %s",
                "best_seller": "best_seller = %s",
            }

            for field, value in update_data.items():
                if field in allowed_fields:
                    update_fields.append(allowed_fields[field])
                    params.append(value)  # Append the value, not the field

            if not update_fields:
                raise ValueError("No valid fields to update.")

            query = f"UPDATE books SET {', '.join(update_fields)} WHERE book_id = %s;"
            params.append(book_id)
            self.db.execute_CUD_query(query, tuple(params))
            return True
        except Exception as e:
            print(f"Error updating book with ID {book_id}: {e}")
            return False

    @staticmethod
    def check_book_stock(book_stock):
        if book_stock <= 0:
            raise ValueError("Book is out of stock")

    def get_book_by_id(self, book_id):
        try:
            query = "SELECT * FROM books WHERE book_id = %s"
            result = self.db.execute_query(query, (book_id,))
            if result:
                return result[0]
            raise ValueError("Book not found")
        except ValueError as ve:
            print(f"ValueError encountered: {str(ve)}")
            return None
        except Exception as e:
            print(f"Error getting book by ID: {e}")
            return None
