from .logger import Logger
from .db.database import reset_all, create_connection
from .db.student import Student
from .db.subject import Subjects
from .db.lecture import Lecture
from .db.lecturer import Lecturer
from .db.enrollment import Enrollment

courses = {
    '800': 'Professional Software Engineering',
    '801': 'Research Methods',
    '802': 'Quantom Computing'
}

conn = None

def select_course() -> str:
    global courses

    while True:
        print('-' * 40)
        print('| ALL COURSES: ')
        print('-' * 40)
        for k in courses:
            print(f'| {k} | {courses[k]}')
        print('-' * 40)
        code = input('please select a course by code: ').strip()
        try:
            value = courses[code]
            print(f'SELECTED: {code} : {value}')
            return code
        except KeyError:
            print('Please select a correct code. Try again...')
            continue

def select_subject():
    s = Subjects()

    while True:
        all = s.all_subjects()
        print('-' * 40)
        print(all)
        print('-' * 40)

        try:
            code = int(input('Please select a subject: ').strip())
            if len(s.search(code)) == 0:
                print('Please select a correct code. Try again...')
                continue
            else:
                return code
        except ValueError:
            print('Please select a correct code. Try again...')

def select_lecturer():
    l = Lecturer()

    while True:
        all = l.all_lecturers()
        print('-' * 40)
        print(all)
        print('-' * 40)

        try:
            code = int(input('Please select a lecturer: ').strip())
            if len(l.search(code)) == 0:
                print('Please select a correct code. Try again...')
                continue
            else:
                return code
        except ValueError:
            print('Please select a correct code. Try again...')

def select_student():
    s = Student()

    while True:
        all = s.all_students()
        print('-' * 40)
        print(all)
        print('-' * 40)
        try:
            code = int(input('Please select a student: ').strip())
            if len(s.search(code)) == 0:
                print('Please select a correct code. Try again...')
                continue
            else:
                return code
        except ValueError:
            print('Please select a correct code. Try again...')

def get_a_str(prompt: str, no_check:bool = False) -> str:
    while True:
        value = input(prompt).strip()
        if no_check:
            return value
        elif len(value) > 0:
            return value

def check_continue(prompt: str) -> bool:
    while True:
        opt = input(prompt)
        if opt.lower() == 'y':
            return True
        elif opt.lower() == 'n':
            return False

def setup_students() -> bool:
    s = Student()
    s.create_table(create_connection())

    while True:
        print('Set up a student following these steps:')
        first_name = get_a_str("* First Name: ")
        last_name = get_a_str("* Last Name: ")
        birthdate = get_a_str("* Birthdate (DD/MM/YYYY): ")
        email = get_a_str("* Email: ")
        try:
            s.add(first_name=first_name, last_name=last_name, b_date=birthdate, email=email)
            if not check_continue('Continue to add another student? [Y/N]: '):
                return True
        except ValueError:
            Logger().e("insert student failed")


def setup_subjects() -> bool:
    s = Subjects()
    s.create_table(create_connection())

    while True:
        print('Set up a subject following these steps:')
        unit = get_a_str("* Subject Unit: ")
        desc = get_a_str("* Subject Desc: ")
        try:
            s.add(unit, desc)
            if not check_continue('Continue to add another subject? [Y/N]: '):
                return True
        except ValueError:
            Logger().e("insert subject failed")

def setup_lecturers() -> bool:
    l = Lecturer()
    l.create_table(create_connection())

    while True:
        print('Set up a lecturer following these steps:')
        f_name = get_a_str("* First Name: ")
        l_name = get_a_str("* Last Name: ")
        l_email = get_a_str('* Email: ')
        l_addr = get_a_str('Address: ', True)
        if len(l_addr) == 0:
            l_addr = None
        try:
            l.add(f_name, l_name, l_addr, l_email)
            if not check_continue('Continue to add another lecturer? [Y/N]: '):
                return True
        except ValueError:
            Logger().e("insert lecturer failed")

def setup_lectures() -> bool:
    l = Lecture()
    l.create_table(create_connection())

    while True:
        print('Set up a lecture following these steps:')

        c_code = select_course()
        if len(l.search_by_course(c_code)) > 0:
            print('Already set up.')
            if not check_continue('Add another one? [Y/N] '):
                return True
            else:
                continue

        s_code = select_subject()
        l_code = select_lecturer()
        
        time = get_a_str("* Time (HH:MM) ")
        date = get_a_str("* Date (DD/MM/YYYY): ")
        l_name = get_a_str('* Lecture Name: ')

        try:
            l.add(s_code, c_code, time, date, l_name, l_code)
            if not check_continue('Continue to add another lecture? [Y/N]: '):
                return True
        except ValueError:
            Logger().e("insert lecturer failed")

def enroll() -> bool:
    global courses

    e = Enrollment()
    e.create_table(create_connection())

    while True:
        print('Start an enrollment with following steps: ')
        s_id = select_student()
        # if len(e.search(s_id)) > 0:
        #     print('Already enrolled.')
        #     if not check_continue('Would you like to continue to enrol another one? [Y/N]: '):
        #         return True
        #     else:
        #         continue

        c_code = select_course()
        c_name = courses[c_code]

        try:
            e.add(s_id, c_name, c_code)
            if not check_continue('Continue to enroll another one? [Y/N]: '):
                return True
        except ValueError:
            Logger().e("-- enroll failed")

def main():
    global conn

    conn = create_connection()

    # Step 1 - init students
    if check_continue('Set up students? [Y/N]" ') and not setup_students():
        Logger().e('setup students failed!!')

    # Step 2 - init subjects
    if check_continue('Set up subjects? [Y/N]" ') and not setup_subjects():
        Logger().e('setup subjects failed!!')
        
    # Step 3 - init lecturers
    if check_continue('Set up lecturers? [Y/N]" ') and not setup_lecturers():
        Logger().e('setup lecturers failed!!')
        
    # Step 4 - init lectures
    if check_continue('Set up lectures? [Y/N]" ') and not setup_lectures():
        Logger().e('setup lectures failed!!')
        
    # Step 5 - student enrollment
    if check_continue('Enrol or not? [Y/N]" ') and not enroll():
        Logger().e('++ enrol failed!!')

    # question 1 - How many students are registered in each course?
    print("How many students are registered in each course?\n", 
          Enrollment().count_students_for_each_course())
    print('-' * 30)

    # question 2 - List the names and student IDs of students who have enrolled in more than one course.
    print('List the names and student IDs of students who have enrolled in more than one course.\n', 
          Enrollment().list_students_for_more_than_one_course())
    print('-' * 30)

    if check_continue('would you like to reset all tables before exit? [Y/N]?'):
        reset_all()

    conn.close()
        
if __name__ == '__main__':
    main()