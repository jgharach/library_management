from Error.LibraryManagementError import ValidationError

class Student:
    def __init__(self, ID, surname, name):      
        self.validate_fields({'Surname': surname, 'Name': name})
        self.ID = ID
        self.surname = surname
        self.name = name

    def validate_fields(self, data):
        if 'Surname' not in data or not data['Surname']:
            raise ValidationError("Surname is required", field_name="Surname")
        
        if 'Name' not in data or not data['Name']:
            raise ValidationError("Name is required", field_name="Name")

    def to_dict(self):
        return {
            "ID": self.ID,
            "Surname": self.surname,
            "Name": self.name,
        }