import copy

import pytest

from scheduler.types.course import Course
from scheduler.types.student import Student, StudentError

def test_init_ascii() -> None:
    student = Student('E5000')
    assert student.number == 'E5000'

def test_init_non_ascii() -> None:
    student = Student('Á100000')
    assert student.number == 'Á100000'

def test_add_course_valid() -> None:
    courses = {'Sistemas Operativos': Course('Sistemas Operativos')}
    student = Student('A100000')
    student.add_course(courses['Sistemas Operativos'])
    assert student.courses == courses

def test_add_course_double() -> None:
    student = Student('A100000')

    student.add_course(Course('Sistemas Operativos'))
    with pytest.raises(StudentError):
        student.add_course(Course('Sistemas Operativos'))

def test_add_course_triple() -> None:
    student = Student('A100000')

    student.add_course(Course('Sistemas Operativos'))
    student.add_course(Course('Sistemas Distribuídos'))

    assert len(student.courses) == 2

    with pytest.raises(StudentError):
        student.add_course(Course('Sistemas Operativos'))

def test_courses_encapsulation() -> None:
    student = Student('A100000')
    courses = student.courses
    courses['SistemasOperativos'] = Course('Sistemas Operativos')
    assert student.courses == {}

def test_eq_none() -> None:
    assert Student('A100000') != None

def test_eq_same() -> None:
    student = Student('A100000')
    assert student == student

def test_eq_equals() -> None:
    student1 = Student('A100000')
    student2 = Student('A100000')
    assert student1 == student2

def test_eq_different_number() -> None:
    student1 = Student('A100000')
    student2 = Student('A100001')
    assert student1 != student2

def test_eq_different_courses() -> None:
    student1 = Student('A100000')
    student2 = Student('A100000')
    student2.add_course(Course('Interface Pessoa-Máquina'))
    assert student1 != student2

def test_eq_different_same_courses_different_content() -> None:
    student1 = Student('A100000')
    student2 = Student('A100000')

    course1 = Course('Interface Pessoa-Máquina')
    course2 = Course('Interface Pessoa-Máquina')
    course2.add_student(student1)

    student1.add_course(course1)
    student2.add_course(course2)
    assert student1 == student2

def test_copy_encapsulation() -> None:
    student1 = Student('A100000')
    student1.add_course(Course('Interface Pessoa-Máquina'))
    student2 = copy.copy(student1)
    student2.add_course(Course('Sistemas Operativos'))

    assert len(student1.courses) == 1
    assert len(student2.courses) == 2

def test_hash_same() -> None:
    student = Student('A100000')
    assert hash(student) == hash(student)

def test_hash_equals() -> None:
    student1 = Student('A100000')
    student2 = Student('A100000')
    assert hash(student1) == hash(student2)

def test_hash_different_number() -> None:
    student1 = Student('A100000')
    student2 = Student('A100001')
    assert hash(student1) != hash(student2)

def test_hash_different_courses() -> None:
    student1 = Student('A100000')
    student2 = Student('A100000')
    student2.add_course(Course('Interface Pessoa-Máquina'))
    assert hash(student1) == hash(student2)

def test_repr_empty() -> None:
    student = Student('A100000')
    assert repr(student) == 'Student(number=\'A100000\', courses={})'

def test_repr_courses() -> None:
    student = Student('A100000')
    student.add_course(Course('Sistemas Operativos'))
    assert repr(student) == 'Student(number=\'A100000\', courses={\'Sistemas Operativos\': ...})'

def test_str_empty() -> None:
    student = Student('A100000')
    assert str(student) == 'Student(number=\'A100000\', courses={})'

def test_str_courses() -> None:
    student = Student('A100000')
    student.add_course(Course('Sistemas Operativos'))
    assert str(student) == 'Student(number=\'A100000\', courses={\'Sistemas Operativos\': ...})'
