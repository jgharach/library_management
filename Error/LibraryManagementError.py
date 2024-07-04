class BookIssueError(Exception):
    pass

class BookDataError(Exception):
   pass

class NotFoundError(Exception):
    pass

class ValidationError(Exception):
    def __init__(self, description, field_name):
        super().__init__(description)
        self.field_name = field_name
