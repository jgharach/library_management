from flask import Flask, request, jsonify, abort, url_for
from flask_cors import CORS

from Service.LibraryManagementService import *
from Error.CustomErrorHandler import CustomErrorHandler
from Error.LibraryManagementError import NotFoundError, BookDataError, ValidationError

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

library_service = LibraryManagementService()

# Custom exception handler for handling 400 Bad Request errors
app.errorhandler(400)(CustomErrorHandler.handle_bad_request_error)

# Custom exception handler for handling 404 Not Found errors
app.errorhandler(404)(CustomErrorHandler.handle_not_found_error)

# Custom exception handler for handling 500 Internal Server Error
app.errorhandler(500)(CustomErrorHandler.handle_internal_server_error)

# Route to add a book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('Title')
    author = data.get('Author')
    quantity = data.get('Quantity')

    try:
        book = library_service.add_book(title, author, quantity)
          # Create the URL for the newly created resource
        location = url_for('get_book_by_id', book_id=book.ID)
        # Use the jsonify function to create a JSON response
        response = jsonify(book.to_dict())
        response.headers['Location'] = location  # Set the Location header
        return response, 201   
    except ValidationError as e:
        abort(400, e)
    except Exception as e:
        abort(500, e)


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    try:
        # Get the book by its ID from the BookDataAccesss class
        book = library_service.get_book(book_id)
        # Use the jsonify function to create a JSON response
        return jsonify(book.to_dict()), 200
    except NotFoundError as e:
        abort(404, e)
    except Exception as e:  
        abort(500, e)

@app.route('/books', methods=['GET'])
def get_books():
    try:
        # Get page and per_page from query parameters
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        
        # Get the list of books from the BookDataAccesss class with pagination
        books_data = library_service.get_books(page, per_page)
        total_books = len(books_data)
        
        # Calculate previous and next page numbers
        previous_page = page - 1 if page > 1 else None
        next_page = page + 1 if total_books == per_page else None
        
        # Calculate total number of pages
        total_pages = (total_books + per_page - 1) // per_page
        
        # Convert the list of Book objects to a list of dictionaries
        books = [Book.to_dict(book) for book in books_data]
        
        # Prepare links for pagination
        links = [{"rel": "self", "href": f"/books?page={page}&per_page={per_page}"}]
        if next_page is not None:
            links.append({"rel": "next", "href": f"/books?page={next_page}&per_page={per_page}"})
        if previous_page is not None:
            links.append({"rel": "prev", "href": f"/books?page={previous_page}&per_page={per_page}"})
        
        # Add links for individual pages
        for p in range(1, total_pages + 1):
            links.append({"rel": "page", "href": f"/books?page={p}&per_page={per_page}"})
        
        return jsonify(books=books, links=links)
    
    except Exception as e:
        abort(500, e)

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
         # Delete a book
        library_service.delete_book(book_id)
        return jsonify({"message": "Book deleted successfully"}), 200
    except BookDataError as e:
        abort(400, e)
    except Exception as e:
        abort(500, e)

# Route to issue a book to a student
@app.route('/issue_book', methods=['POST'])
def issue_book():
    data = request.get_json()
    B_ID = data.get('B_ID') 
    S_ID = data.get('S_ID')
    try:
        library_service.issue_book(B_ID, S_ID)
        return jsonify({'message': 'Book issued successfully'}), 201
    except BookIssueError as e:
        abort(400, e)
    except Exception as e:
        abort(500, e)

# Route to return a book from a student
@app.route('/return_book', methods=['POST'])
def return_book():
    data = request.get_json()
    B_ID = data.get('B_ID')
    S_ID = data.get('S_ID')
    try:
        library_service.return_book(B_ID, S_ID)
        return jsonify({'message': 'Book returned successfully'}), 200
    except BookIssueError as e:
        abort(400, e)
    except Exception as e:
        abort(500, e)

if __name__ == '__main__':
    app.run(debug=True)