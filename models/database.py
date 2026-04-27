import json
import os
from models.student import Student

DATABASE_FILE = "student.data"

class Database:

    def __init__(self):
        self.file_exists()

    def file_exists(self):
        if not os.path.exists(DATABASE_FILE):
            with open (DATABASE_FILE, "w") as f:
                json.dump([],f)

    def read_all(self):

        self.file_exists()

        with open (DATABASE_FILE, "r") as f:
            data = json.load(f)
                
        students = []
        for s in data:
            student = Student.from_dict(s)
            students.append(student)

        return students
    
    def write_all(self, students):

        self.file_exists()

        with open (DATABASE_FILE, "w") as f:
            
            students_list = []
            for s in students:
                student_dict = s.to_dict()
                students_list.append(student_dict)
                       
            json.dump(students_list, f, indent=2)

    def clear(self):

        self.file_exists()

        with open(DATABASE_FILE, "w") as f:
            json.dump([],f)

