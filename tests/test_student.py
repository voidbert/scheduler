import copy

import pytest

from scheduler.types.course import Course
from scheduler.types.shift import Shift, ShiftType
from scheduler.types.student import Student, StudentError

def test_init_default_courses() -> None:
    student = Student('A100')

    assert student.number == 'A100'
    assert student.courses == {}

def test_init_no_courses() -> None:
    student = Student('A100', [])

    assert student.number == 'A100'
    assert student.courses == {}

def test_init_valid_courses() -> None:
    courses = [Course('Comunicações por Computador')]
    student = Student('A100', courses)

    assert student.number == 'A100'
    assert student.courses == {'Comunicações por Computador': courses[0]}

def test_init_invalid_courses() -> None:
    course = Course('Desenvolvimento de Sistemas de Software')

    with pytest.raises(StudentError):
        Student('A100', [course, course])

def test_init_encapsulation() -> None:
    courses = [Course('Inteligência Artificial')]
    student = Student('A100', courses)

    assert len(student.courses) == 1
    assert student.courses['Inteligência Artificial'] is courses[0]

    courses.append(courses[0])
    assert len(student.courses) == 1

def test_add_course_valid_empty() -> None:
    courses = {'Laboratórios de Informática IV': Course('Laboratórios de Informática IV')}
    student = Student('A100')
    student.add_course(courses['Laboratórios de Informática IV'])

    assert student.courses == courses
    assert student.courses['Laboratórios de Informática IV'] is \
        courses['Laboratórios de Informática IV']

def test_add_course_valid_non_empty() -> None:
    courses = {'Sistemas Distribuídos': Course('Sistemas Distribuídos')}
    student = Student('A100', list(courses.values()))

    courses['Análise e Testes de Software'] = Course('Análise e Testes de Software')
    student.add_course(courses['Análise e Testes de Software'])

    assert student.courses == courses

def test_add_course_invalid_equals() -> None:
    course = Course('Análise de Projetos')
    student = Student('A100', [course])

    with pytest.raises(StudentError):
        student.add_course(course)

def test_add_course_invalid_different() -> None:
    student = Student('A100', [Course('Aprendizagem e Decisão Inteligentes')])

    with pytest.raises(StudentError):
        student.add_course(Course('Aprendizagem e Decisão Inteligentes', [Shift(ShiftType.OT, 2)]))

def test_courses_encapsulation() -> None:
    student = Student('A100', [])
    courses = student.courses

    course = Course('Computação Gráfica')
    student.add_course(course)
    assert courses[course.name] == course

def test_eq_none() -> None:
    assert Student('A100') != None

def test_eq_same() -> None:
    student = Student('A100')
    assert student == student

def test_eq_equals() -> None:
    student1 = Student('A100')
    student2 = Student('A100', [])
    assert student1 == student2

def test_eq_different_number() -> None:
    student1 = Student('A100')
    student2 = Student('E100')
    assert student1 != student2

def test_eq_different_courses() -> None:
    student1 = Student('A100')
    student2 = Student('A100', [Course('Engenharia Web')])
    assert student1 != student2

def test_eq_same_courses_same_course_content() -> None:
    student1 = Student('A100', [Course('Engenharia Web')])
    student2 = Student('A100', [Course('Engenharia Web', [Shift(ShiftType.PL, 1)])])
    assert student1 == student2

def test_copy() -> None:
    student = Student('A100', [Course('Interface Pessoa-Máquina')])
    assert student == copy.copy(student)

def test_copy_encapsulation() -> None:
    student1 = Student('A100')
    student2 = copy.copy(student1)
    student2.add_course(Course('Processamento de Linguagens'))

    assert not student1.courses

def test_hash_same() -> None:
    student = Student('A100')
    assert hash(student) == hash(student)

def test_hash_equals() -> None:
    student1 = Student('A100')
    student2 = Student('A100', [])
    assert hash(student1) == hash(student2)

def test_hash_different_number() -> None:
    student1 = Student('A100')
    student2 = Student('E100')
    assert hash(student1) != hash(student2)

def test_hash_different_courses() -> None:
    student1 = Student('A100')
    student2 = Student('A100', [Course('Segurança de Sistemas Informáticos')])
    assert hash(student1) == hash(student2)

def test_repr() -> None:
    course = Course('Computação Paralela')
    student = Student('A100', [course])
    assert repr(student) == \
        f'Student(number=\'A100\', courses={{\'Computação Paralela\': {course}}})'
