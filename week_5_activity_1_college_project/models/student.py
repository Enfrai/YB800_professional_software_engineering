from typing import Dict
from models.user import User

class Student(User):
    """Represents a student inheriting from User."""

    def __init__(self, user_id: str, name: str, email: str, major: str):
        super().__init__(user_id, name, email)
        self._major = major
        self._enrolled_courses = []
        self._grades: Dict[str, str] = {}  # course_code -> grade

    @property
    def major(self) -> str:
        return self._major

    @property
    def enrolled_courses(self):
        return self._enrolled_courses

    @property
    def grades(self) -> Dict[str, str]:
        return self._grades

    def enroll_course(self, course) -> bool:
        if course not in self._enrolled_courses:
            if course.add_student(self):
                self._enrolled_courses.append(course)
                return True
        return False

    def set_grade(self, course_code: str, grade: str):
        self._grades[course_code] = grade

    def display_info(self) -> str:
        base_info = super().display_info()
        return f"[Student] {base_info} | Major: {self._major}"