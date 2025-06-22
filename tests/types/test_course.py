import copy

import pytest

from scheduler.types.course import Course, CourseError
from scheduler.types.student import Student

def test_init_name_id() -> None:
    course = Course('Programação Orientada aos Objetos')
    assert course.name == 'Programação Orientada aos Objetos'
    assert course.id == 'Programação Orientada aos Objetos'

def test_init_students_empty() -> None:
    course1 = Course('Programação Orientada aos Objetos')
    course2 = Course('Programação Orientada aos Objetos', {})
    assert course1 == course2

def test_init_students_encapsulation() -> None:
    students = {'A100000': Student('A100000')}
    course = Course('Processamento de Linguagem', students)
    assert course.students == students

    students['E5000'] = Student('E5000')
    assert len(course.students) == 1

def test_init_students_invalid() -> None:
    students = {'A100000': Student('A100001')}
    with pytest.raises(CourseError):
        Course('Processamento de Linguagem', students)

def test_students_encapsulation() -> None:
    course = Course('Sistemas Operativos')
    students = course.students
    students['A100000'] = Student('A100000')
    assert course.students == {}

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

def test_eq_different_name_different_id() -> None:
    course1 = Course('Desenvolvimento de Sistemas de Software')
    course2 = Course('Sistemas Operativos')
    assert course1 != course2

def test_eq_different_name_same_id() -> None:
    course1 = Course('SistemasOperativos')
    course2 = Course('Sistemas Operativos')
    assert course1 != course2

def test_eq_different_students() -> None:
    course1 = Course('Desenvolvimento de Sistemas de Software')
    course2 = Course('Desenvolvimento de Sistemas de Software')
    course2.add_student(Student('A100000'))
    assert course1 != course2

def test_eq_different_same_courses_different_content() -> None:
    course1 = Course('Processamento de Linguagens')
    course2 = Course('Processamento de Linguagens')
    course1.add_student(Student('A100000'))
    course2.add_student(Student('A100000', {'Processamento de Linguagens': course1}))
    assert course1 == course2

def test_copy_encapsulation() -> None:
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

def test_hash_different_students() -> None:
    course1 = Course('Desenvolvimento de Sistemas de Software')
    course2 = Course('Desenvolvimento de Sistemas de Software')
    course2.add_student(Student('A100000'))
    assert hash(course1) == hash(course2)

def test_repr_empty() -> None:
    course = Course('Programação Imperativa')
    assert repr(course) == 'Course(name=\'Programação Imperativa\', students={})'

def test_repr_courses() -> None:
    course = Course('Programação Imperativa')
    course.add_student(Student('A100000'))
    assert repr(course) == 'Course(name=\'Programação Imperativa\', students={\'A100000\': ...})'

def test_str_empty() -> None:
    course = Course('Programação Imperativa')
    assert str(course) == 'Course(name=\'Programação Imperativa\', students={})'

def test_str_courses() -> None:
    course = Course('Programação Imperativa')
    course.add_student(Student('A100000'))
    assert str(course) == 'Course(name=\'Programação Imperativa\', students={\'A100000\': ...})'
