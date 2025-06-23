import copy
import datetime

import pytest

from scheduler.types.course import Course, CourseError
from scheduler.types.room import Room
from scheduler.types.shift import Shift, ShiftType
from scheduler.types.student import Student
from scheduler.types.timeslot import Timeslot
from scheduler.types.weekday import Weekday

def test_init_name_id() -> None:
    course = Course('Programação Orientada aos Objetos')
    assert course.name == 'Programação Orientada aos Objetos'
    assert course.id == 'Programação Orientada aos Objetos'

def test_shifts_encapsulation() -> None:
    course = Course('Sistemas Operativos')
    shifts = course.shifts
    shifts['Sistemas Operativos T2'] = Shift(
        Course('Sistemas Operativos'),
        ShiftType.T,
        2,
        [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
        Room('CP1', '0.08', 200)
    )

    assert course.shifts == {}

def test_students_encapsulation() -> None:
    course = Course('Sistemas Operativos')
    students = course.students
    students['A100000'] = Student('A100000')
    assert course.students == {}

def test_add_shift_valid() -> None:
    course = Course('Sistemas Operativos')
    shifts = {
        'Sistemas Operativos T2': Shift(
            course,
            ShiftType.T,
            2,
            [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
            Room('CP1', '0.08', 200)
        )
    }

    course.add_shift(shifts['Sistemas Operativos T2'])
    assert course.shifts == shifts

def test_add_shift_double() -> None:
    course = Course('Sistemas Operativos')
    shift = Shift(
        course,
        ShiftType.T,
        2,
        [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
        Room('CP1', '0.08', 200)
    )

    course.add_shift(shift)
    with pytest.raises(CourseError):
        course.add_shift(copy.copy(shift))

def test_add_shift_triple() -> None:
    course = Course('Sistemas Operativos')
    shift1 = Shift(
        course,
        ShiftType.T,
        1,
        [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
        Room('CP1', '0.04', 150)
    )
    shift2 = Shift(
        course,
        ShiftType.T,
        2,
        [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
        Room('CP1', '0.08', 200)
    )

    course.add_shift(shift1)
    course.add_shift(shift2)
    assert len(course.shifts) == 2

    with pytest.raises(CourseError):
        course.add_shift(copy.copy(shift2))

def test_add_shift_other_course() -> None:
    course = Course('Sistemas Operativos')
    shifts = {
        'Sistemas Operativos T2': Shift(
            Course('Sistemas Operativos'), # Equal, but not the same object
            ShiftType.T,
            2,
            [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
            Room('CP1', '0.08', 200)
        )
    }

    with pytest.raises(CourseError):
        course.add_shift(shifts['Sistemas Operativos T2'])

def test_add_student_valid() -> None:
    students = {'A100000': Student('A100000')}
    course = Course('Sistemas Operativos')
    course.add_student(students['A100000'])
    assert course.students == students

def test_add_student_double() -> None:
    course = Course('Sistemas Operativos')

    course.add_student(Student('A100000'))
    with pytest.raises(CourseError):
        course.add_student(Student('A100000'))

def test_add_student_triple() -> None:
    course = Course('Sistemas Operativos')

    course.add_student(Student('A100000'))
    course.add_student(Student('E5000'))

    assert len(course.students) == 2

    with pytest.raises(CourseError):
        course.add_student(Student('A100000'))

def test_eq_none() -> None:
    assert Course('Desenvolvimento de Sistemas de Software') != None

def test_eq_same() -> None:
    course = Course('Desenvolvimento de Sistemas de Software')
    assert course == course

def test_eq_equals() -> None:
    course1 = Course('Desenvolvimento de Sistemas de Software')
    course2 = Course('Desenvolvimento de Sistemas de Software')
    assert course1 == course2

def test_eq_different_name() -> None:
    course1 = Course('Desenvolvimento de Sistemas de Software')
    course2 = Course('Sistemas Operativos')
    assert course1 != course2

def test_eq_different_shifts() -> None:
    course1 = Course('Desenvolvimento de Sistemas de Software')
    course2 = Course('Desenvolvimento de Sistemas de Software')
    course2.add_shift(Shift(
        course2,
        ShiftType.PL,
        1,
        [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
        Room('CP1', '1.10', 45)
    ))
    assert course1 != course2

def test_eq_different_students() -> None:
    course1 = Course('Desenvolvimento de Sistemas de Software')
    course2 = Course('Desenvolvimento de Sistemas de Software')
    course2.add_student(Student('A100000'))
    assert course1 != course2

def test_eq_different_same_courses_different_content() -> None:
    course1 = Course('Processamento de Linguagens')
    course2 = Course('Processamento de Linguagens')

    student1 = Student('A100000')
    student2 = Student('A100000')
    student2.add_course(course1)

    course1.add_student(student1)
    course2.add_student(student2)

    assert course1 == course2

def test_copy_encapsulation_shifts() -> None:
    course1 = Course('Sistemas Operativos')
    course1.add_shift(Shift(
        course1,
        ShiftType.PL,
        1,
        [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
        Room('CP1', '1.10', 45)
    ))

    course2 = copy.copy(course1)
    course2.add_shift(Shift(
        course2,
        ShiftType.PL,
        2,
        [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
        Room('CP2', '1.12', 45)
    ))

    assert len(course1.shifts) == 1
    assert len(course2.shifts) == 2
    assert course1.shifts['Sistemas Operativos PL1'] == course2.shifts['Sistemas Operativos PL1']

def test_copy_encapsulation_students() -> None:
    course1 = Course('Sistemas Operativos')
    course1.add_student(Student('A100000'))
    course2 = copy.copy(course1)
    course2.add_student(Student('E5000'))

    assert len(course1.students) == 1
    assert len(course2.students) == 2

def test_hash_same() -> None:
    course = Course('Desenvolvimento de Sistemas de Software')
    assert hash(course) == hash(course)

def test_hash_equals() -> None:
    course1 = Course('Desenvolvimento de Sistemas de Software')
    course2 = Course('Desenvolvimento de Sistemas de Software')
    assert hash(course1) == hash(course2)

def test_hash_different_name() -> None:
    course1 = Course('Desenvolvimento de Sistemas de Software')
    course2 = Course('Sistemas Operativos')
    assert hash(course1) != hash(course2)

def test_hash_different_shifts() -> None:
    course1 = Course('Desenvolvimento de Sistemas de Software')
    course2 = Course('Desenvolvimento de Sistemas de Software')
    course2.add_shift(Shift(
        course2,
        ShiftType.PL,
        1,
        [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
        Room('CP1', '1.10', 45)
    ))
    assert hash(course1) == hash(course2)

def test_hash_different_students() -> None:
    course1 = Course('Desenvolvimento de Sistemas de Software')
    course2 = Course('Desenvolvimento de Sistemas de Software')
    course2.add_student(Student('A100000'))
    assert hash(course1) == hash(course2)

def test_repr_empty() -> None:
    course = Course('Programação Imperativa')
    assert repr(course) == 'Course(name=\'Programação Imperativa\', students={}, shifts={})'

def test_repr_shifts() -> None:
    course = Course('Programação Imperativa')
    course.add_shift(Shift(
        course,
        ShiftType.PL,
        1,
        [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
        Room('CP1', '1.10', 45)
    ))

    assert repr(course) == \
    'Course(name=\'Programação Imperativa\', students={}, shifts={\'PL1\': ...})'

def test_repr_students() -> None:
    course = Course('Programação Imperativa')
    course.add_student(Student('A100000'))
    assert repr(course) == \
        'Course(name=\'Programação Imperativa\', students={\'A100000\': ...}, shifts={})'

def test_str_empty() -> None:
    course = Course('Programação Imperativa')
    assert repr(course) == 'Course(name=\'Programação Imperativa\', students={}, shifts={})'

def test_str_shifts() -> None:
    course = Course('Programação Imperativa')
    course.add_shift(Shift(
        course,
        ShiftType.PL,
        1,
        [Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))],
        Room('CP1', '1.10', 45)
    ))

    assert repr(course) == \
    'Course(name=\'Programação Imperativa\', students={}, shifts={\'PL1\': ...})'

def test_str_students() -> None:
    course = Course('Programação Imperativa')
    course.add_student(Student('A100000'))
    assert repr(course) == \
        'Course(name=\'Programação Imperativa\', students={\'A100000\': ...}, shifts={})'
