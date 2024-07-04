from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from Error.LibraryManagementError import ValidationError

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'
    
    ID = Column(Integer, primary_key=True)    
    Titre = Column(String)
    Auteur = Column(String)
    Qte = Column(Integer)

    def __init__(self, Titre, Auteur, Qte):
        self.validate_fields({'Titre': Titre, 'Auteur': Auteur, 'Qte': Qte})
        self.Titre = Titre
        self.Auteur = Auteur
        self.Qte = Qte

    def validate_fields(self, data):
        if 'Titre' not in data or not data['Titre']:
            raise ValidationError("Title is required", field_name="Titre")
        
        if 'Auteur' not in data or not data['Auteur']:
            raise ValidationError("Author is required", field_name="Auteur")
        
        if 'Qte' not in data or data['Qte'] <= 0:
            raise ValidationError("Quantity must be a positive value", field_name="Qte")

    def to_dict(self):
        return {
            "ID": self.ID,
            "Title": self.Titre,
            "Author": self.Auteur,
            "Quantity": self.Qte
        }