from typing import List, Optional

class Course:
    """Represents a course in the college system."""

    def __init__(self, course_code: str, title: str, credits: int):
        self._course_code = course_code
        self._title = title
        self._credits = credits
        self._assigned_lecturer: Optional["Lecturer"] = None
        self._enrolled_students: List["Student"] = []

    @property
    def course_code(self) -> str:
        return self._course_code

    @property
    def title(self) -> str:
        return self._title

    @property
    def credits(self) -> int:
        return self._credits

    @property
    def assigned_lecturer(self):
        return self._assigned_lecturer

    @assigned_lecturer.setter
    def assigned_lecturer(self, lecturer):
        self._assigned_lecturer = lecturer

    @property
    def enrolled_students(self):
        return self._enrolled_students

    def add_student(self, student) -> bool:
        if student not in self._enrolled_students:
            self._enrolled_students.append(student)
            return True
        return False

    def remove_student(self, student) -> bool:
        if student in self._enrolled_students:
            self._enrolled_students.remove(student)
            return True
        return False

    def get_details(self) -> str:
        lecturer_name = self._assigned_lecturer.name if self._assigned_lecturer else "Unassigned"
        return (f"Course Code: {self._course_code} | Title: {self._title} | "
                f"Credits: {self._credits} | Lecturer: {lecturer_name} | "
                f"Enrolled Students: {len(self._enrolled_students)}")