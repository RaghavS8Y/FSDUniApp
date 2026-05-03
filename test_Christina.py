"""
Test file for Christina's Subject Enrolment System (Part C)
Tests the SubjectController independently
"""

from models.student import Student
from models.database import Database
from controllers.subject_controller import SubjectController


if __name__ == "__main__":
    # Create a test database
    database = Database()
    
    # Create a test student
    test_student = Student(
        name="Alan Jones",
        email="alan.jones@university.com",
        password="Helloworld123"
    )
    
    # Save to database
    students = database.read_all()
    students.append(test_student)
    database.write_all(students)
    
    # Run the enrolment menu
    system = SubjectController(test_student)
    system.enrolment_menu()