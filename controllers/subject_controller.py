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

