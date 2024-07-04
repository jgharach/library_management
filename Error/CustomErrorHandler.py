from flask import jsonify

class CustomErrorHandler:
    # Custom exception handler for handling 400 Bad Request errors
    @staticmethod
    def handle_bad_request_error(error):
        if hasattr(error.description, 'field_name'):
            error_message = str(error.description)
            field_name = error.description.field_name
            response = {
                'error': error_message,
                'field': field_name
            }
        else:
            error_message = str(error)
            response = {
                'error': error_message
            }
        
        return jsonify(response), 400       
    
   # Custom exception handler for handling 404 Not Found errors
    @staticmethod
    def handle_not_found_error(error):
        error_message = str(error)  # Get the exception message
        response = {
        'error': error_message
        }
        return jsonify(response), 404
    
    # Custom exception handler for handling 500 Internal Server Error
    @staticmethod
    def handle_internal_server_error(error):
        error_message = str(error)  # Get the exception message
        response = {
            'error': error_message
        }
        return jsonify(response), 500