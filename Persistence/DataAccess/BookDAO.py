from Persistence.ConnectionPool import ConnectionPool
from Persistence.Entity.Book import Book
from sqlalchemy.sql import text
from Error.LibraryManagementError import BookDataError, NotFoundError

class BookDAO:
    def __init__(self):
        # Create a connection pool singleton instance
        self.connection_pool = ConnectionPool.get_instance()

    def add_book(self, title, author, quantity):
        # Get a connection from the pool
        # Any exception within the block will result in a rollback
        # No need for conn.commit() or conn.rollback() here
        with self.connection_pool.get_session() as conn:
            book = Book(Titre=title, Auteur=author, Qte=quantity)
            conn.add(book)
            conn.commit()
            conn.refresh(book)  # Refresh the object from the database to get the generated ID
            return book  # Return the original book object


    def get_books(self, page, per_page):
        with self.connection_pool.get_session() as conn:
        # Calculate the offset based on the page and per_page
            offset = (page - 1) * per_page 
            # Use slice() to paginate the query results
            books = conn.query(Book).slice(offset, offset + per_page).all()
            return books
    
    def get_book(self, book_id):
        # Get a connection from the pool
        with self.connection_pool.get_session() as conn:
            # Use SQLAlchemy ORM to query the Book entity by ID
            book = conn.query(Book).filter_by(ID=book_id).first()
            if book:
                return book 
            else:
                raise NotFoundError("Book not found")
        
    def delete_book(self, book_id):
        with self.connection_pool.get_session() as conn:
            conn.execute(text("CALL DeleteBook(:book_id, @error_code)"), {"book_id": book_id})
            conn.commit()
            error_code = conn.scalar(text("SELECT @error_code"))
            if error_code == 45002:
                raise BookDataError("There is book issued")
            elif error_code == 45003:
                raise BookDataError("There is no book in the database with this ID") 