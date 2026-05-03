import random
from models.subject import Subject

class Student:

    def __init__(self, name, email, password, student_id = None, subjects = None):
        
        self.name = name
        self.email = email
        self.password = password

        if student_id is None:
            self.student_id = f"{random.randint(1,999999):06d}"
        else:
            self.student_id = f"{int(student_id):06d}"

        if subjects is None:
            self.subjects = []
        else:
            self.subjects = subjects

    def average_mark(self):
        if self.subjects == []:
            return 0
        
        total = 0
        for s in self.subjects:
            total += s.mark
        average = total / len(self.subjects)
        return average
    
    def is_pass(self):
        return self.average_mark() >= 50

    # convert the student object to a dictionary    
    def to_dict(self):

        subjects_list = []
        for s in self.subjects:
            subjects_list.append(s.to_dict())
        
        return {
            "name" : self.name,
            "email" : self.email,
            "password" : self.password,
            "student_id" : self.student_id,
            "subjects" : subjects_list
        }
    
    # create a student object from a dictionary
    @staticmethod
    def from_dict(data):

        subjects = []
        for s in data.get("subjects",[]):
            subjects.append(Subject.from_dict(s))

        return Student(
            name = data["name"],
            email = data["email"],
            password = data["password"],
            student_id = data["student_id"],
            subjects = subjects
        )
    
    def __str__(self):
        return f"{self.name} :: {self.student_id} --> Email: {self.email}"
    