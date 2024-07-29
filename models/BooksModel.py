from config.DBConnection import DBConnection
from datetime import date


class BooksModel:
    def __init__(self):
        self.db = DBConnection()

    def create_book(self, book_data):
        try:
            query = "INSERT INTO books(stock, isbn13, author, original_publication_year, title, summary, genre_id, availability, best_seller) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            params = (book_data.get("stock", None),
                      book_data.get("isbn13"),
                      book_data.get("author"),
                      book_data.get("original_publication_year", None),
                      book_data.get("title"),
                      book_data.get("summary", None),
                      book_data.get("genre_id", None),
                      book_data.get("availability", True),
                      book_data.get("best_seller", False))
            return self.db.execute_query(query, params)
        except Exception as e:
            print(f"Error: {e}")
