from Persistence.ConnectionPool import ConnectionPool
from sqlalchemy.sql import text
from Persistence.Entity.Student import Student

class StudentDAO:
    def __init__(self):
        # Create a connection pool singleton instance
        self.connection_pool = ConnectionPool.get_instance()

    def add_student(self, surname, name):
        # Get a connection from the pool       
        with self.connection_pool.get_session() as conn:       
            student = Student(None, surname, name)
            # Execute a raw SQL query using SQLAlchemy's execute method
            result = conn.execute(text('''INSERT INTO Student (Nom, Prenom) 
                    VALUES (:surname, :name)'''), {"surname": surname, "name": name})
            conn.commit()
            # Retrieve the newly assigned ID and update the student object
            student.ID = result.lastrowid
            return student

    def get_students(self):
        # Get a connection from the pool
        with self.connection_pool.get_session() as conn:         
            result = conn.execute(text('SELECT ID, Nom, Prenom FROM student'))
            students_data = result.fetchall()
            # Convert the list of tuples to a list of Student objects
            students = []
            for student_data in students_data:
                # Create a Student object using the Student class
                student = Student(student_data[0], student_data[1], student_data[2])
                students.append(student)

            return students
        
    def delete_student(self, student_id):
        # Get a connection from the pool
        with self.connection_pool.get_session() as conn:
            conn.execute(text('DELETE FROM student WHERE ID = :student_id').params(student_id=student_id))
            conn.commit()
