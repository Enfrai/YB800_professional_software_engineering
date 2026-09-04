import sys
from models.student import Student
from models.lecturer import Lecturer
from models.course import Course

class CollegeSystemCLI:
    def __init__(self):
        self.students = {}
        self.lecturers = {}
        self.courses = {}
        self._seed_data()

    def _seed_data(self):
        # Initial sample data
        l1 = Lecturer("L001", "Dr. Alan Turing", "turing@college.edu", "Computer Science")
        s1 = Student("S001", "Alice Smith", "alice@student.edu", "Software Engineering")
        s2 = Student("S002", "Bob Jones", "bob@student.edu", "Information Technology")
        
        c1 = Course("CS101", "Introduction to OOP", 3)
        c2 = Course("CS102", "Database Systems", 4)

        l1.assign_course(c1)
        s1.enroll_course(c1)
        
        self.lecturers[l1.user_id] = l1
        self.students[s1.user_id] = s1
        self.students[s2.user_id] = s2
        self.courses[c1.course_code] = c1
        self.courses[c2.course_code] = c2

    def main_menu(self):
        while True:
            print("\n========================================")
            print("   COLLEGE MANAGEMENT SYSTEM (CLI)     ")
            print("========================================")
            print("1. Lecturer Portal")
            print("2. Student Portal")
            print("3. System Overview")
            print("4. Exit")
            
            choice = input("\nSelect an option (1-4): ").strip()
            if choice == "1":
                self.lecturer_menu()
            elif choice == "2":
                self.student_menu()
            elif choice == "3":
                self.system_overview()
            elif choice == "4":
                print("\nExiting application. Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

    def lecturer_menu(self):
        print("\n--- Lecturer Portal ---")
        lect_id = input("Enter Lecturer ID (e.g., L001): ").strip()
        lecturer = self.lecturers.get(lect_id)
        
        if not lecturer:
            print("Lecturer ID not found.")
            return

        print(f"\nWelcome, {lecturer.name}!")
        while True:
            print("\n1. View Assigned Courses")
            print("2. Assign Grade to Student")
            print("3. Return to Main Menu")
            
            choice = input("Select an option (1-3): ").strip()
            if choice == "1":
                print("\nAssigned Courses:")
                if not lecturer.assigned_courses:
                    print("No courses assigned.")
                for c in lecturer.assigned_courses:
                    print(f" - {c.get_details()}")
            elif choice == "2":
                c_code = input("Enter Course Code: ").strip()
                course = self.courses.get(c_code)
                if not course or course not in lecturer.assigned_courses:
                    print("Invalid course code or course not assigned to you.")
                    continue
                
                s_id = input("Enter Student ID: ").strip()
                student = self.students.get(s_id)
                if not student or student not in course.enrolled_students:
                    print("Student not enrolled in this course.")
                    continue
                
                grade = input("Enter Grade (A, B, C, D, F): ").strip().upper()
                if lecturer.assign_grade(student, course, grade):
                    print(f"Successfully assigned grade '{grade}' to {student.name} for {course.course_code}.")
            elif choice == "3":
                break

    def student_menu(self):
        print("\n--- Student Portal ---")
        stud_id = input("Enter Student ID (e.g., S001, S002): ").strip()
        student = self.students.get(stud_id)
        
        if not student:
            print("Student ID not found.")
            return

        print(f"\nWelcome, {student.name}!")
        while True:
            print("\n1. View Available Courses & Enroll")
            print("2. View My Enrolled Courses & Grades")
            print("3. Return to Main Menu")
            
            choice = input("Select an option (1-3): ").strip()
            if choice == "1":
                print("\nAvailable Courses:")
                for code, c in self.courses.items():
                    print(f" - [{code}] {c.title} (Credits: {c.credits})")
                
                c_code = input("\nEnter Course Code to Enroll (or Enter to cancel): ").strip()
                if c_code in self.courses:
                    if student.enroll_course(self.courses[c_code]):
                        print(f"Enrolled successfully in {c_code}.")
                    else:
                        print("Already enrolled in this course.")
            elif choice == "2":
                print("\nEnrolled Courses & Grades:")
                if not student.enrolled_courses:
                    print("Not enrolled in any courses.")
                for c in student.enrolled_courses:
                    grade = student.grades.get(c.course_code, "Not Graded Yet")
                    print(f" - {c.course_code}: {c.title} | Grade: {grade}")
            elif choice == "3":
                break

    def system_overview(self):
        print("\n=== SYSTEM OVERVIEW ===")
        print("\nLecturers:")
        for l in self.lecturers.values():
            print(f" - {l.display_info()}")
            
        print("\nStudents:")
        for s in self.students.values():
            print(f" - {s.display_info()}")
            
        print("\nCourses:")
        for c in self.courses.values():
            print(f" - {c.get_details()}")

if __name__ == "__main__":
    app = CollegeSystemCLI()
    app.main_menu()