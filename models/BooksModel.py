from models.GeneralModel import GeneralModel


class BooksModel(GeneralModel):
    def __init__(self):
        super().__init__('books')

    # CREATE
    def create_book(self, book_data):
        return self.create(book_data)

    # READ
    def get_book_by_isbn(self, isbn13):
        filters = {"isbn13": isbn13}
        return self.read(filters)

    def get_book_stock(self, book_id):
        result = self.read({"book_id": book_id})
        return result[0]["stock"] if result else None

    def get_book_by_id(self, book_id):
        result = self.read({"book_id": book_id})
        if result:
            return result[0]
        else:
            raise ValueError("Book not found")

    def search_books(self, author=None, title=None, genre_id=None, isbn13=None, original_publication_year=None,
                     availability=None, best_seller=None, entry_date=None):
        filters = {}
        if author:
            filters["author"] = f"%{author}%"
        if title:
            filters["title"] = f"%{title}%"
        if genre_id:
            filters["genre_id"] = genre_id
        if isbn13:
            filters["isbn13"] = isbn13
        if original_publication_year:
            filters["original_publication_year"] = original_publication_year
        if availability is not None:
            filters["availability"] = availability
        if best_seller is not None:
            filters["best_seller"] = best_seller
        if entry_date:
            filters["entry_date"] = entry_date
        return self.read(filters)

    # UPDATE

    def update_stock_by_isbn13(self, isbn13):
        update_data = {"stock": "stock + 1"}
        filters = {"isbn13": isbn13}
        return self.update(update_data, filters)

    def update_stock_by_id(self, book_id, amount):
        update_data = {"stock": f"stock + {amount}"}
        filters = {"book_id": book_id}
        return self.update(update_data, filters)

    def update_book(self, book_id, update_data):
        filters = {"book_id": book_id}
        return self.update(update_data, filters)

    # DELETE

    def delete_book(self, isbn13):
        filters = {"isbn13": isbn13}
        return self.delete(filters)

    # EXTRA FUNCTIONALITY

    @staticmethod
    def check_stock(stock):
        if stock < 0:
            raise ValueError("Stock cannot be negative")


