from Persistence.DataAccess.BookDAO import *
from Persistence.DataAccess.BookIssueDAO import *

class LibraryManagementService:
    def __init__(self):
        self.book_dao = BookDAO()
        self.book_issue_dao = BookIssueDAO()

    # Méthodes simplifiées pour interagir avec les différentes fonctionnalités

    # Livres
    def add_book(self, title, author, quantity):
        return self.book_dao.add_book(title, author, quantity)

    def get_book(self, book_id):
        return self.book_dao.get_book(book_id)

    def get_books(self, page, per_page):
        return self.book_dao.get_books(page, per_page)
    
    def delete_book(self, book_id):
        return self.book_dao.delete_book(book_id)

    # Problèmes d'emprunt
    def issue_book(self, B_ID, S_ID):
        self.book_issue_dao.issue_book(B_ID, S_ID)

    def return_book(self, B_ID, S_ID):
        self.book_issue_dao.return_book(B_ID, S_ID)