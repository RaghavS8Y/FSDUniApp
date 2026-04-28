import re
from models.database import Database
from models.subject import Subject

# Password pattern: starts with uppercase, 5+ letters total, ends with 3+ digits
PASSWORD_PATTERN = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")


class SubjectController:
    """Handles subject enrolment menu and operations for a logged-in student"""
    
    def __init__(self, student):
        """Initialize with a Student object"""
        self.student = student
        self.database = Database()
    
    def enrolment_menu(self):
        """Main enrolment menu loop: C/E/R/S/X"""
        while True:
            choice = input("        Student Course Menu (c/e/r/s/x): ").strip().lower()
            
            if choice == "c":
                self.change_password()
            elif choice == "e":
                self.enrol_subject()
            elif choice == "r":
                self.remove_subject()
            elif choice == "s":
                self.show_subjects()
            elif choice == "x":
                self.database.write_all(self.database.read_all())
                break
            else:
                print("        Invalid option")
    
    def enrol_subject(self):
        """Enrol the student in a new subject (max 4)"""
        if len(self.student.subjects) >= 4:
            print("        Students are allowed to enrol in 4 subjects only")
            return
        
        # Create a new subject
        new_subject = Subject()
        self.student.subjects.append(new_subject)
        
        # Update the database
        students = self.database.read_all()
        for i, s in enumerate(students):
            if s.student_id == self.student.student_id:
                students[i] = self.student
                break
        self.database.write_all(students)
        
        print(f"        Enrolling in Subject-{new_subject.subject_id}")
        print(f"        You are now enrolled in {len(self.student.subjects)} out of 4 subjects")
    
    def remove_subject(self):
        """Remove a subject by ID"""
        subject_id = input("        Remove Subject by ID: ").strip()
        
        # Pad with zeros if it's a number
        if subject_id.isdigit():
            subject_id = subject_id.zfill(3)
        
        # Find and remove the subject
        removed = None
        for subject in self.student.subjects:
            if subject.subject_id == subject_id:
                removed = subject
                self.student.subjects.remove(subject)
                break
        
        if removed is None:
            print(f"        Subject-{subject_id} does not exist")
        else:
            # Update the database
            students = self.database.read_all()
            for i, s in enumerate(students):
                if s.student_id == self.student.student_id:
                    students[i] = self.student
                    break
            self.database.write_all(students)
            
            print(f"        Dropping Subject-{removed.subject_id}")
            print(f"        You are now enrolled in {len(self.student.subjects)} out of 4 subjects")
    
    def show_subjects(self):
        """Display all enrolled subjects with mark and grade"""
        print(f"        Showing {len(self.student.subjects)} subjects")
        
        for subject in self.student.subjects:
            print(f"        {subject}")
    
    def change_password(self):
        """Change student password with validation"""
        print("        Updating Password")
        
        # Get new password
        new_password = input("        New Password: ").strip()
        
        # Validate password format
        while not PASSWORD_PATTERN.fullmatch(new_password):
            print("        Incorrect password format")
            new_password = input("        New Password: ").strip()
        
        # Confirm password
        confirm_password = input("        Confirm Password: ").strip()
        
        while new_password != confirm_password:
            print("        Password does not match - try again")
            confirm_password = input("        Confirm Password: ").strip()
        
        # Update password
        self.student.password = new_password
        
        # Save to database
        students = self.database.read_all()
        for i, s in enumerate(students):
            if s.student_id == self.student.student_id:
                students[i] = self.student
                break
        self.database.write_all(students)

# Password rule:
# Starts with one upper-case letter,
# followed by at least 4 more letters,
# followed by at least 3 digits.
PASSWORD_PATTERN = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")


@dataclass
class Subject:
    id: str
    mark: int
    grade: str

    @staticmethod
    def generate_subject_id(existing_ids: set) -> str:
        while True:
            new_id = f"{random.randint(1, 999):03d}"
            if new_id not in existing_ids:
                return new_id

    @staticmethod
    def calculate_grade(mark: float) -> str:
        if mark >= 85:
            return "HD"
        elif mark >= 75:
            return "D"
        elif mark >= 65:
            return "C"
        elif mark >= 50:
            return "P"
        else:
            return "F"

    @classmethod
    def create_new_subject(cls, existing_ids: set):
        subject_id = cls.generate_subject_id(existing_ids)
        mark = random.randint(25, 100)
        grade = cls.calculate_grade(mark)
        return cls(subject_id, mark, grade)


@dataclass
class Student:
    id: str
    name: str
    email: str
    password: str
    subjects: List[Subject] = field(default_factory=list)

    def enrol_subject(self) -> Optional[Subject]:
        if len(self.subjects) >= 4:
            return None

        existing_ids = {subject.id for subject in self.subjects}
        new_subject = Subject.create_new_subject(existing_ids)
        self.subjects.append(new_subject)
        return new_subject

    def remove_subject(self, subject_id: str) -> Optional[Subject]:
        for subject in self.subjects:
            if subject.id == subject_id:
                self.subjects.remove(subject)
                return subject
        return None

    def average_mark(self) -> float:
        if not self.subjects:
            return 0.0

        total = sum(subject.mark for subject in self.subjects)
        return total / len(self.subjects)

    def average_grade(self) -> str:
        return Subject.calculate_grade(self.average_mark())

    def change_password(self, new_password: str):
        self.password = new_password


class Database:
    def __init__(self, filename: str = DATA_FILE):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "wb") as file:
                pickle.dump([], file)

    def read_students(self) -> List[Student]:
        self.ensure_file_exists()

        try:
            with open(self.filename, "rb") as file:
                return pickle.load(file)
        except EOFError:
            return []

    def write_students(self, students: List[Student]):
        with open(self.filename, "wb") as file:
            pickle.dump(students, file)

    def update_student(self, updated_student: Student):
        students = self.read_students()

        for index, student in enumerate(students):
            if student.id == updated_student.id:
                students[index] = updated_student
                self.write_students(students)
                return

        students.append(updated_student)
        self.write_students(students)


class SubjectEnrolmentSystem:
    def __init__(self, database: Database):
        self.database = database

    def run(self, student: Student):
        while True:
            choice = input("        Student Course Menu (c/e/r/s/x): ").strip().lower()

            if choice == "c":
                self.change_password(student)

            elif choice == "e":
                self.enrol_subject(student)

            elif choice == "r":
                self.remove_subject(student)

            elif choice == "s":
                self.show_subjects(student)

            elif choice == "x":
                self.database.update_student(student)
                break

            else:
                print("        Invalid option")

    def enrol_subject(self, student: Student):
        if len(student.subjects) >= 4:
            print("        Students are allowed to enrol in 4 subjects only")
            return

        subject = student.enrol_subject()

        if subject is not None:
            self.database.update_student(student)
            print(f"        Enrolling in Subject-{subject.id}")
            print(f"        You are now enrolled in {len(student.subjects)} out of 4 subjects")

    def remove_subject(self, student: Student):
        subject_id = input("        Remove Subject by ID: ").strip()

        if subject_id.isdigit():
            subject_id = subject_id.zfill(3)

        removed_subject = student.remove_subject(subject_id)

        if removed_subject is None:
            print(f"        Subject-{subject_id} does not exist")
        else:
            self.database.update_student(student)
            print(f"        Dropping Subject-{removed_subject.id}")
            print(f"        You are now enrolled in {len(student.subjects)} out of 4 subjects")

    def show_subjects(self, student: Student):
        print(f"        Showing {len(student.subjects)} subjects")

        for subject in student.subjects:
            print(
                f"        [ Subject::{subject.id} -- mark = {subject.mark} -- grade = {subject.grade} ]"
            )

    def change_password(self, student: Student):
        print("        Updating Password")

        new_password = input("        New Password: ").strip()

        while not PASSWORD_PATTERN.fullmatch(new_password):
            print("        Incorrect password format")
            new_password = input("        New Password: ").strip()

        confirm_password = input("        Confirm Password: ").strip()

        while new_password != confirm_password:
            print("        Password does not match - try again")
            confirm_password = input("        Confirm Password: ").strip()

        student.change_password(new_password)
        self.database.update_student(student)