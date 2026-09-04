class Person:
    """Base class representing a general Person."""
    def __init__(self, id_val: str, name: str):
        self.id = id_val
        self.name = name

    def display_info(self):
        print(f"ID: {self.id}")
        print(f"Name: {self.name}")


class Student(Person):
    """Class representing a Student, inheriting from Person."""
    def __init__(self, id_val: str, name: str, student_id: str):
        super().__init__(id_val, name)
        self.student_id = student_id

    def display_info(self):
        super().display_info()
        print(f"Student ID: {self.student_id}")


class Staff(Person):
    """Class representing a Staff member, inheriting from Person."""
    def __init__(self, id_val: str, name: str, staff_id: str, tax_num: str):
        super().__init__(id_val, name)
        self.staff_id = staff_id
        self.tax_num = tax_num

    def display_info(self):
        super().display_info()
        print(f"Staff ID: {self.staff_id}")
        print(f"Tax Number: {self.tax_num}")


class General(Staff):
    """Class representing General Staff, inheriting from Staff."""
    def __init__(self, id_val: str, name: str, staff_id: str, tax_num: str, rate_of_pay: float):
        super().__init__(id_val, name, staff_id, tax_num)
        self.rate_of_pay = rate_of_pay

    def calculate_pay_rate(self, hours_worked: float = 1.0) -> float:
        """Calculates total pay based on hours worked and rate of pay."""
        return self.rate_of_pay * hours_worked

    def display_pay_rate(self, hours_worked: float = 1.0):
        total_pay = self.calculate_pay_rate(hours_worked)
        print(f"Hourly Pay Rate: ${self.rate_of_pay:.2f}")
        if hours_worked != 1.0:
            print(f"Total Pay for {hours_worked} hours: ${total_pay:.2f}")


class Academic(Staff):
    """Class representing Academic Staff (e.g., Lecturer), inheriting from Staff."""
    def __init__(self, id_val: str, name: str, staff_id: str, tax_num: str, publications: list):
        super().__init__(id_val, name, staff_id, tax_num)
        # publications parameter can be a list of publication titles or an integer count
        if isinstance(publications, list):
            self.publications = publications
        else:
            self.publications = [f"Publication #{i+1}" for i in range(int(publications))]

    def get_num_publications(self) -> int:
        """Calculates and returns the total number of publications."""
        return len(self.publications)

    def display_publications(self):
        """Displays the count and list of publications."""
        print(f"Number of Publications: {self.get_num_publications()}")
        if self.publications:
            print("Publications List:")
            for idx, pub in enumerate(self.publications, 1):
                print(f"  {idx}. {pub}")


# Demonstration/Test Code
if __name__ == "__main__":
    print("==========================================")
    print("       UNIVERSITY PEOPLE OOP DEMO         ")
    print("==========================================")

    # 1. Academic / Lecturer Instance
    lecturer_pubs = [
        "Advances in Machine Learning (2023)",
        "Object-Oriented Design Patterns (2024)",
        "Data Science Applications in Education (2025)"
    ]
    lecturer = Academic(
        id_val="P-1001",
        name="Dr. Sarah Connor",
        staff_id="STF-8891",
        tax_num="TX-998823",
        publications=lecturer_pubs
    )

    print("\n--- Lecturer / Academic Staff Details ---")
    lecturer.display_info()
    lecturer.display_publications()

    # 2. General Staff Instance
    general_staff = General(
        id_val="P-2002",
        name="John Doe",
        staff_id="STF-4412",
        tax_num="TX-554411",
        rate_of_pay=35.50
    )

    print("\n--- General Staff Details ---")
    general_staff.display_info()
    general_staff.display_pay_rate(hours_worked=37.5)