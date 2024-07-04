import unittest
from Persistence.DataAccess.StudentDAO import StudentDAO
from Service.LibraryManagementService import LibraryManagementService
from marshmallow import ValidationError
from Error.LibraryManagementError import NotFoundError, BookDataError, BookIssueError, ValidationError

class TestBookDataAccessMethods(unittest.TestCase):
    def setUp(self):
        # Initialisation : Créez une instance de la classe à tester, éventuellement avec des mocks ou des dépendances simulées.
        self.library_service = LibraryManagementService()
        self.student_dao = StudentDAO()

    def verification_proprietes(self, retrieved_book, book):
        self.assertEqual(retrieved_book.ID, book.ID)
        self.assertEqual(retrieved_book.Titre, book.Titre)
        self.assertEqual(retrieved_book.Auteur, book.Auteur)
        self.assertEqual(retrieved_book.Qte, book.Qte)
    
    def test_scenar1(self):
        with self.assertRaises(ValidationError):
           book1 = self.library_service.add_book("", "", 0)

        # Ajouter le premier livre
        book1 = self.library_service.add_book("a", "b", 4)

        # Récupérer le livre ajouté
        retrieved_book1 = self.library_service.get_book(book1.ID)

        # Vérifier les propriétés du premier livre
        self.verification_proprietes(retrieved_book1, book1)

        # Ajouter le deuxième livre
        book2 = self.library_service.add_book("a5", "b4", 4)
        retrieved_book2 = self.library_service.get_book(book2.ID)

        # Vérifier les propriétés du deuxième livre
        self.verification_proprietes(retrieved_book2, book2)

        # Récupérer tous les livres
        books_data = self.library_service.get_books()

        # Vérifier si les livres sont présents
        book1_found = any(book.ID == book1.ID for book in books_data)
        book2_found = any(book.ID == book2.ID for book in books_data)
        self.assertTrue(book1_found)
        self.assertTrue(book2_found)

        # Supprimer les livres
        self.library_service.delete_book(book1.ID)
        self.library_service.delete_book(book2.ID)

        with self.assertRaises(NotFoundError):
            self.library_service.get_book(book1.ID)
            self.library_service.get_book(book2.ID)
        
    def test_scenar2(self):
         # Ajouter un livre et un étudiant
        book1 = self.library_service.add_book("a", "a", 5)
        student1 = self.student_dao.add_student("a", "a")

        # Tenter d'emprunter le livre avec un étudiant inexistant
        with self.assertRaises(BookIssueError):
            self.library_service.issue_book(book1.ID, 80000)

        # Tenter d'ajouter un étudiant avec des informations manquantes
        with self.assertRaises(ValidationError):
            self.student_dao.add_student("", "")

        # Emprunter le livre avec un étudiant existant
        self.library_service.issue_book(book1.ID, student1.ID)

        with self.assertRaises(BookDataError):
            self.library_service.delete_book(book1.ID)
        self.library_service.return_book(book1.ID, student1.ID)

        self.library_service.delete_book(book1.ID)
        self.student_dao.delete_student(student1.ID)

if __name__ == '__main__':
    unittest.main()