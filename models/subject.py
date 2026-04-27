import random

class Subject:

    def __init__(self, subject_id = None, mark = None):

        if subject_id is None:
            self.subject_id = f"{random.randint(1,999):03d}"
        else:
            self.subject_id = f"{int(subject_id):03d}"

        if mark is None:
            self.mark = random.randint(25,100)
        else:
            self.mark = int(mark)

        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.mark >= 85:
            return "HD"
        elif self.mark >= 75:
            return "D"
        elif self.mark >= 65:
            return "C"
        elif self.mark >= 50:
            return "P"
        else:
            return "Z"

    # convert the subject object to a dictionary    
    def to_dict(self):
        return {
            "subject_id" : self.subject_id,
            "mark" : self.mark,
            "grade" : self.grade
        }
    
    # create a subject object from a dictionary
    @staticmethod
    def from_dict(data):
        return Subject(
            subject_id = data["subject_id"],
            mark = data["mark"]
        )
    
    def __str__(self):
        return f"[ Subject::{self.subject_id} -- mark = {self.mark:>3} -- grade = {self.grade:>2} ]"
    
