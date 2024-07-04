import argparse
import pandas as pd

from Service.LibraryManagementService import *
from Persistence.DataAccess.StudentDAO import *

def main():
    parser = argparse.ArgumentParser(description="Library Management System CLI")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add Book command
    add_book_parser = subparsers.add_parser("add_book", help="Add a new book")
    add_book_parser.add_argument("title", type=str, help="Book title")
    add_book_parser.add_argument("author", type=str, help="Book author")
    add_book_parser.add_argument("quantity", type=int, help="Book quantity")

    # Add Student command
    add_student_parser = subparsers.add_parser("add_student", help="Add a new student")
    add_student_parser.add_argument("name", type=str, help="Student name")
    add_student_parser.add_argument("surname", type=str, help="Student surname")

    # Delete Book command
    delete_book_parser = subparsers.add_parser("delete_book", help="Delete book")
    delete_book_parser.add_argument("book_id", type=int, help="Book ID")

    # List Books command
    subparsers.add_parser("list_books", help="List all books")

    # List Students command
    subparsers.add_parser("list_students", help="List all students")

    # Issue Book command
    issue_book_parser = subparsers.add_parser("issue_book", help="Issue a book to a student")
    issue_book_parser.add_argument("book_id", type=int, help="Book ID")
    issue_book_parser.add_argument("student_id", type=int, help="Student ID")

    # Return Book command
    return_book_parser = subparsers.add_parser("return_book", help="Return a book")
    return_book_parser.add_argument("book_id", type=int, help="Book ID")
    return_book_parser.add_argument("student_id", type=int, help="Book ID")


    args = parser.parse_args()

    # Initialize the LibraryManagementService with existing database connection parameters
    library_service = LibraryManagementService()
    student_dao = StudentDAO()

    # Execute the appropriate command based on the subparser selected
    if args.command == "add_book":
        print("add book:")
        library_service.add_book(args.title, args.author, args.quantity)
    elif args.command == "add_student":
        student_dao.add_student(args.name, args.surname)
    elif args.command == "delete_book":
        library_service.delete_book(args.book_id)
    elif args.command == "list_books":
        books = library_service.get_books()
        print(books)
    elif args.command == "list_students":
        students = student_dao.get_students()
        column_names = ["ID", "Nom", "Prénom"]
        df = pd.DataFrame(students, columns=column_names)
        print(df.to_string(index=False))
    elif args.command == "issue_book":
        library_service.issue_book(args.book_id, args.student_id)
    elif args.command == "return_book":
        library_service.return_book(args.book_id, args.student_id)

main()