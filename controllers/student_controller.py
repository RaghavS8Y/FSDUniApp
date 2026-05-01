import re
from models.student import Student
from models.database import Database

EMAIL_PATTERN = r"^[a-zA-Z]+\.[a-zA-Z]+@university\.com$"
PASSWORD_PATTERN = r"^[A-Z][a-zA-Z]{4,}\d{3,}$"

class StudentController:

    def __init__(self):
        self.db = Database()

    def validate_credentials(self, email, password):
        email_ok = bool(re.match(EMAIL_PATTERN, email))
        password_ok = bool(re.match(PASSWORD_PATTERN, password))

        return email_ok and password_ok
    
    def extract_name_from_email(self, email):
        name_part = email.split("@")[0]
        parts = name_part.split(".")

        return " ".join(p.capitalize() for p in parts)
    
    def university_menu(self):

        while True:
            choice = input("University System: (A)dmin, (S)tudent, or X : ").srtip()

            if choice == "A":
                from controllers.admin_controller import AdminController
                AdminController.admin_menu()

            elif choice == "S":
                self.student_menu()

            elif choice == "X":
                print("Thank You")
                break

    def student_menu(self):

        while True:
            choice = input("        Student System (l/r/x): ").strip()

            if choice == "r":
                self.register_student()

            elif choice == "l":
                student = self.login_student()

                if student is not None:
                    from controllers.subject_controller import SubjectController
                    SubjectController(student).enrolment_menu()

            elif choice == "x":
                break

    def register_student(self):

        print("        Student Sign Up")

        while True:
            email = input("        Email: ").strip()
            password = input("        Password: ").strip()

            if not self.validate_credentials(email, password):
                print("        Incorrect email or password format")
                continue

            print("        email and password formats acceptable")

            students = self.db.read_all()
            exist_emails = [s.email for s in students]

            if email in exist_emails:

                name = self.extract_name_from_email(email)
                print(f"        Student {name} already exists")
                return
            
            name = input("        Name:").strip()

            new_student = Student(name=name, email= email, password = password)

            students.append(new_student)
            self.db.write_all(students)

            print(f"        Enrolling Student {name}")
            return
        
    def login_student(self):

        print("        Student Sign In")

        while True:
            email = input("        Email: ").strip()
            password = input("         Password: ").strip()

            if not self.validate_credentials(email, password):
                print("        Incorrect email or password format")
                continue

            print("        email and password formats acceptable")

            students = self.db.read_all()
            for s in students:
                if s.email == email and s.password == password:
                    return s
                
            print("        Student does not exist")
            return 





