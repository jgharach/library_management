from Persistence.ConnectionPool import ConnectionPool
from sqlalchemy.sql import text
from Error.LibraryManagementError import BookIssueError

class BookIssueDAO:  
    def __init__(self):
        # Create a connection pool singleton instance
        self.connection_pool = ConnectionPool.get_instance()

    def issue_book(self, book_id, student_id):
        with self.connection_pool.get_session() as conn:
            # Execute a raw SQL query to call the stored procedure
            conn.execute(text('CALL IssueBook(:book_id, :student_id, @error_code)'), {"book_id": book_id, "student_id": student_id})
            conn.commit()
            error_code = conn.scalar(text("SELECT @error_code"))
            if error_code == 45000:
                raise BookIssueError("Student not exist")
            elif error_code == 45001:
                raise BookIssueError("Book not available for issue")
             
            
    def return_book(self, book_id, student_id):       
        with self.connection_pool.get_session() as conn:
            conn.execute(text('CALL ReturnBook(:book_id, :student_id, @error_code)'), {"book_id": book_id, "student_id": student_id})
            conn.commit()
            error_code = conn.scalar(text("SELECT @error_code"))
            if error_code == 45004:
                raise BookIssueError("Student has not issued this book")