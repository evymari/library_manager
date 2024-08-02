from config.DBConnection import DBConnection


class BooksModel:
    def __init__(self):
        self.db = DBConnection()

        self.genre_list = {"Adventure": 1,
                       "Science fiction": 2,
                       "Fantasy": 3,
                       "Horror": 4,
                       "Detective": 5,
                       "Crime": 6,
                       "Romance": 7,
                       "Historical": 8,
                       "Mystery": 9,
                       "Dystopian": 10,
                       "Contemporary fiction": 11,
                       "Urban fantasy": 12,
                       "Magic realism": 13,
                       "Spy": 14,
                       "War": 15,
                       "Humor": 16,
                       "Graphic": 17,
                       "Psychological": 18,
                       "Bildungsroman (coming-of-age)": 19,
                       "Satirical": 20,
                       "Epistolary": 21,
                       "Gothic": 22,
                       "Western": 23,
                       "Young adult": 24,
                       "Autofiction": 25,
                       "Social commentary": 26,
                       "Picaresque": 27,
                       "Suspense (thriller)": 28,
                       "Feminist literature": 29,
                       "LGBTQ+ literature": 30
                       }
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
# try-except is used to handle errors during database operations like connection issues, SQL errors or data processing
# if-else is conditional logic to handle scenarios based on outcome of the operation or checks

    def get_book_by_isbn(self, isbn13):
        try:
            query = "SELECT book_id, stock FROM books WHERE isbn13 = %s;"
            params = (isbn13,)
            result = self.db.execute_query(query, params)
            return result
        except Exception as e:
            print(f"Error: {e}")

    def update_stock(self, isbn13):
        try:
            query = "UPDATE books SET stock = stock + 1 WHERE isbn13 = %s;"
            params = (isbn13,)
            self.db.execute_CUD_query(query, params)
        except Exception as e:
            print(f"Error: {e}")

    def search_books(self, author=None, title=None, genre_id=None):

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
            result = self.db.execute_query(query, params)

            return result
        except Exception as e:
            print(f"Error: {e}")

    def get_genre_id(self, genre_name):
        genre_id = self.genre_list.get(genre_name)
        return  genre_id



