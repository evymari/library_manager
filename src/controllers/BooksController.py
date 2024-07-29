from models.BooksModel import BooksModel


class BooksController:
    def __init__(self):
        self.books_model = BooksModel()
    def add_book(self, book_data):
        try:
            self.books_model.create_book(book_data)
            print(f"Book added: {book_data["title"]}")
            return dict(status_code = 200, message = "Book added successfully")
        except Exception as e:
            print (f"Error: {e}")