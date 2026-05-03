import os
import sys

if __name__ == "__main__" and __package__ is None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)

from models.database import Database


class AdminController:
    def __init__(self):
        self.database = Database()

    def admin_menu(self):
        while True:
            choice = input("Admin System (c/g/p/r/s/x): ").strip().lower()

            if choice == "c":
                self.clear_database()
            elif choice == "g":
                self.group_students()
            elif choice == "p":
                self.partition_students()
            elif choice == "r":
                self.remove_student()
            elif choice == "s":
                self.show_students()
            elif choice == "x":
                break
            else:
                print("Invalid option")

    def show_students(self):
        students = self.database.read_all()

        print("Student List")
        if not students:
            print("\t< Nothing to Display >")
            return

        for student in students:
            print(student)

    def group_students(self):
        students = self.database.read_all()

        print("Grade Grouping")
        if not students:
            print("\t< Nothing to Display >")
            return

        groups = {}

        for student in students:
            grade = self._average_grade(student)
            if grade not in groups:
                groups[grade] = []
            groups[grade].append(student)

        for grade in ["HD", "D", "C", "P", "Z"]:
            if grade in groups:
                print(f"{grade} --> {self._format_admin_group(groups[grade])}")

    def partition_students(self):
        students = self.database.read_all()

        pass_students = []
        fail_students = []

        for student in students:
            if student.is_pass():
                pass_students.append(student)
            else:
                fail_students.append(student)

        print("PASS/FAIL Partition")
        print(f"FAIL --> {self._format_admin_group(fail_students)}")
        print(f"PASS --> {self._format_admin_group(pass_students)}")

    def remove_student(self):
        student_id = input("Remove by ID: ").strip().zfill(6)
        students = self.database.read_all()

        for student in students:
            if student.student_id == student_id:
                students.remove(student)
                self.database.write_all(students)
                print(f"Removing Student {student_id} Account")
                return

        print(f"Student {student_id} does not exist")

    def clear_database(self):
        print("Clearing students database")
        confirmation = input("Are you sure you want to clear the database (Y)ES/(N)O: ").strip().lower()

        if confirmation == "y":
            self.database.clear()
            print("Students data cleared")

    def _format_admin_group(self, students):
        if not students:
            return "[]"

        formatted_students = []
        for student in students:
            formatted_students.append(self._format_admin_student(student))

        return f"[{', '.join(formatted_students)}]"

    def _format_admin_student(self, student):
        average = student.average_mark()
        grade = self._average_grade(student)
        return f"{student.name} :: {student.student_id} --> GRADE: {grade} - MARK: {average:.2f}"

    def _average_grade(self, student):
        if not student.subjects:
            return "N/A"

        average = student.average_mark()

        if average >= 85:
            return "HD"
        if average >= 75:
            return "D"
        if average >= 65:
            return "C"
        if average >= 50:
            return "P"
        return "Z"


if __name__ == "__main__":
    AdminController().admin_menu()
