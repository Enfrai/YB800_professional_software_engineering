class UniversityConfig:
    _instance = None

    university_name = None
    academic_year = None
    semester = None

    def getInstance(self):
        return self._instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def config(self, university_name, academic_year, semester):
        self.university_name = university_name
        self.academic_year = academic_year
        self.semester = semester

    def __str__(self):
        return f'{self.__dict__}'


c1 = UniversityConfig()
c2 = UniversityConfig()
c3 = UniversityConfig()

print(c1 is c2, c2 is c3)

c1.config("Yoobee College", 2026, 'Semester 1')

print(c2)

