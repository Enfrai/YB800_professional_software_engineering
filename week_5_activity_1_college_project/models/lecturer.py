from typing import List
from models.user import User

class Lecturer(User):
    """Represents a lecturer inheriting from User."""

    def __init__(self, user_id: str, name: str, email: str, department: str):
        super().__init__(user_id, name, email)
        self._department = department
        self._assigned_courses: List = []

    @property
    def department(self) -> str:
        return self._department

    @property
    def assigned_courses(self):
        return self._assigned_courses

    def assign_course(self, course) -> bool:
        if course not in self._assigned_courses:
            self._assigned_courses.append(course)
            course.assigned_lecturer = self
            return True
        return False

    def assign_grade(self, student, course, grade: str) -> bool:
        if course in self._assigned_courses and course in student.enrolled_courses:
            student.set_grade(course.course_code, grade)
            return True
        return False

    def display_info(self) -> str:
        base_info = super().display_info()
        return f"[Lecturer] {base_info} | Department: {self._department}"