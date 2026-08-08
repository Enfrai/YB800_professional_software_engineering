from enum import Enum
from typing import TypeVar, Generic

# To define a generic for Group to accept any type of data
T = TypeVar('T')

# A definition of class as a data type to collect information for student
class Student:
    name = None
    age = None
    address = None
    student_id = None

    # To init a student object by specific attributes
    def __init__(self, name: str, age: int, address: str, student_id: str):
        self.name = name
        self.age = age
        self.address = address
        self.studentID = student_id

    # To init a student object by a collected directory
    def __init__(self, dict):
        self.name = dict['name']
        self.age = dict['age']
        self.address = dict['address']
        self.student_id = dict['student_id']

    # Output format
    def __str__(self):
        # return '{\n' + f'\t"name": {self.name},\n\t"age": {self.age},\n\t"address": {self.address},\n\t"student_id": {self.student_id}' + '\n}'
        return '{' + f'"name": {self.name}, "age": {self.age}, "address": {self.address}, "student_id": {self.student_id}' + '}'

# An enumration of types to sort.
class SortType(Enum):
    NAME = 0
    AGE = 1
    ADDR = 2
    ID = 3

# An class to collect all students with types Student or dictionary.
class Group(Generic[T]):
    students: list[T] = []

    # Init a group object by students with initial information from dictionary or Student.
    def __init__(self, students=[None] * 70):
        self.students = students

    # Sort all students according to specified sort type.
    def sortBy(self, t: SortType):
        if SortType.NAME == t:
            self.students.sort(key=lambda x: x.name if type(x) == Student else x['name'])
        elif SortType.AGE == t:
            self.students.sort(key=lambda x: x.age if type(x) == Student else x['age'])
        elif SortType.ADDR == t:
            self.students.sort(key=lambda x: x.address if type(x) == Student else x['address'])
        elif SortType.ID == t:
            self.students.sort(key=lambda x: x.student_id if type(x) == Student else x['student_id'])
        else:
            print('sort type is not supported!!')

        return self

    # Output all students
    def echo(self):
        str = ''
        for e in self.students:
            str += f'{e}\n'
        print(str)

def main():
    # testing data
    testing = [
        {'name': 'Allex', 'age': 10, 'address': 'iiiii', 'student_id': '222222'},
        {'name': 'Bob', 'age': 9, 'address': 'fffff', 'student_id': '111111'},
        {'name': 'Caron', 'age': 8, 'address': 'eeeeee', 'student_id': '333333'},
        {'name': 'Dragon', 'age': 7, 'address': 'aaaaa', 'student_id': '101010'},
        {'name': 'Ella', 'age': 6, 'address': 'bbbbb', 'student_id': '777777'},
        {'name': 'Elon', 'age': 6, 'address': 'ccccc', 'student_id': '999999'},
        {'name': 'Fox', 'age': 5, 'address': 'ddddd', 'student_id': '666666'},
        {'name': 'Glay', 'age': 4, 'address': 'ggggg', 'student_id': '444444'},
        {'name': 'Haven', 'age': 3, 'address': 'hhhhh', 'student_id': '555555'},
    ]

    # init a group object with dictionary type
    g1 = Group[dict](testing)
    g1.sortBy(SortType.NAME).echo()
    g1.sortBy(SortType.AGE).echo()
    g1.sortBy(SortType.ADDR).echo()
    g1.sortBy(SortType.ID).echo()

    print('\n' + '=' * 30 + '\n')

    # init testing data by Student using testing1 data
    testing2: list[Student] = []
    for e in testing:
        testing2.append(Student(e))

    # init a group object with Student type
    g2 = Group[Student](testing2)
    g2.sortBy(SortType.NAME).echo()
    g2.sortBy(SortType.AGE).echo()
    g2.sortBy(SortType.ADDR).echo()
    g2.sortBy(SortType.ID).echo()


if __name__ == '__main__':
    main()