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
    
    def _save_student(self):
        """Persist the current student state to the database."""
        students = self.database.read_all()
        for i, s in enumerate(students):
            if s.student_id == self.student.student_id:
                students[i] = self.student
                break
        self.database.write_all(students)

    def enrol_subject(self):
        """Enrol in a new subject. Returns the new Subject, or None if already at 4."""
        if len(self.student.subjects) >= 4:
            return None
        new_subject = Subject()
        self.student.subjects.append(new_subject)
        self._save_student()
        return new_subject

    def remove_subject_by_id(self, subject_id):
        """Remove a subject by ID. Returns the removed Subject, or None if not found."""
        if subject_id.isdigit():
            subject_id = subject_id.zfill(3)
        for subject in self.student.subjects:
            if subject.subject_id == subject_id:
                self.student.subjects.remove(subject)
                self._save_student()
                return subject
        return None

    def enrolment_menu(self):
        """Main enrolment menu loop: C/E/R/S/X"""
        while True:
            choice = input("        Student Course Menu (c/e/r/s/x): ").strip().lower()

            if choice == "c":
                self.change_password()
            elif choice == "e":
                result = self.enrol_subject()
                if result is None:
                    print("        Students are allowed to enrol in 4 subjects only")
                else:
                    print(f"        Enrolling in Subject-{result.subject_id}")
                    print(f"        You are now enrolled in {len(self.student.subjects)} out of 4 subjects")
            elif choice == "r":
                subject_id = input("        Remove Subject by ID: ").strip()
                result = self.remove_subject_by_id(subject_id)
                if result is None:
                    print(f"        Subject-{subject_id} does not exist")
                else:
                    print(f"        Dropping Subject-{result.subject_id}")
                    print(f"        You are now enrolled in {len(self.student.subjects)} out of 4 subjects")
            elif choice == "s":
                self.show_subjects()
            elif choice == "x":
                break
            else:
                print("        Invalid option")
    
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

