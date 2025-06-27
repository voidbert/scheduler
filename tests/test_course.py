import copy
import datetime

import pytest

from scheduler.types.course import Course, CourseError
from scheduler.types.room import Room
from scheduler.types.shift import Shift, ShiftType
from scheduler.types.timeslot import Timeslot
from scheduler.types.weekday import Weekday

def test_init_default_shifts() -> None:
    course = Course('Álgebra Linear')

    assert course.name == 'Álgebra Linear'
    assert course.shifts == {}

def test_init_no_shifts() -> None:
    course = Course('Cálculo para Engenharia', [])

    assert course.name == 'Cálculo para Engenharia'
    assert course.shifts == {}

def test_init_valid_shifts() -> None:
    shift1 = Shift(ShiftType.T, 1)
    shift2 = Shift(ShiftType.T, 2)
    course = Course('Tópicos de Matemática Discreta', [shift1, shift2])

    assert course.name == 'Tópicos de Matemática Discreta'
    assert course.shifts == {'T1': shift1, 'T2': shift2}

def test_init_invalid_shifts() -> None:
    shift1 = Shift(ShiftType.T, 1)
    shift2 = Shift(ShiftType.T, 1)

    with pytest.raises(CourseError):
        Course('Programação Funcional', [shift1, shift2])

def test_init_encapsulation() -> None:
    shifts = [Shift(ShiftType.PL, 2)]
    course = Course('Programação Funcional', shifts)

    assert len(course.shifts) == 1
    assert course.shifts['PL2'] is shifts[0]

    shifts.append(shifts[0])
    assert len(course.shifts) == 1

def test_add_shift_valid_empty() -> None:
    course = Course('Laboratórios de Informática I', [])
    shift = Shift(ShiftType.PL, 1)
    course.add_shift(shift)

    assert course.shifts == {'PL1': shift}
    assert course.shifts['PL1'] is shift

def test_add_shift_valid_non_empty() -> None:
    course = Course('Opção UMinho', [Shift(ShiftType.TP, 1)])
    course.add_shift(Shift(ShiftType.TP, 2))
    assert course.shifts == {'TP1': Shift(ShiftType.TP, 1), 'TP2': Shift(ShiftType.TP, 2)}

def test_add_shift_invalid_equals() -> None:
    course = Course('Lógica', [Shift(ShiftType.TP, 1)])

    with pytest.raises(CourseError):
        course.add_shift(Shift(ShiftType.TP, 1))

def test_add_shift_invalid_different() -> None:
    slot = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), Room('CP1', '0.08'))
    course = Course('Análisa Matemática para Engenharia', [Shift(ShiftType.TP, 1, [slot])])

    with pytest.raises(CourseError):
        course.add_shift(Shift(ShiftType.TP, 1))

def test_id() -> None:
    assert Course('Elementos de Probabilidades e Teoria de Números').id == \
        'Elementos de Probabilidades e Teoria de Números'

def test_shifts_encapsulation() -> None:
    course = Course('Programação Imperativa', [Shift(ShiftType.TP, 1)])
    shifts = course.shifts
    shifts['TP2'] = Shift(ShiftType.TP, 2)

    assert len(course.shifts) == 1

def test_eq_none() -> None:
    assert Course('Laboratórios de Informática II') != None

def test_eq_same() -> None:
    course = Course('Sistemas de Computação')
    assert course == course

def test_eq_equals() -> None:
    course1 = Course('Algoritmos e Complexidade')
    course2 = Course('Algoritmos e Complexidade', [])
    assert course1 == course2

def test_eq_different_name() -> None:
    course1 = Course('Arquitetura de Computadores')
    course2 = Course('Estatística Aplicada')
    assert course1 != course2

def test_eq_different_shifts() -> None:
    course1 = Course('Física Moderna')
    course2 = Course('Física Moderna', [Shift(ShiftType.T, 1)])
    assert course1 != course2

def test_eq_same_shifts_different_shift_content() -> None:
    slot = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), Room('CP1', '0.08'))
    course1 = Course('Fundamentos de Comunicação de Dados', [Shift(ShiftType.TP, 1)])
    course2 = Course('Fundamentos de Comunicação de Dados', [Shift(ShiftType.TP, 1, [slot])])
    assert course1 == course2

def test_copy() -> None:
    course = Course('Laboratórios de Informática III')
    assert course == copy.copy(course)

def test_copy_encapsulation() -> None:
    course1 = Course('Bases de Dados')
    course2 = copy.copy(course1)
    course2.add_shift(Shift(ShiftType.PL, 8))

    assert not course1.shifts

def test_hash_same() -> None:
    course = Course('Investigação Operacional')
    assert hash(course) == hash(course)

def test_hash_equals() -> None:
    course1 = Course('Métodos Numéricos e Otimização não Linear')
    course2 = Course('Métodos Numéricos e Otimização não Linear', [])
    assert hash(course1) == hash(course2)

def test_hash_different_name() -> None:
    course1 = Course('Programação Orientada aos Objetos')
    course2 = Course('Redes de Computadores')
    assert hash(course1) != hash(course2)

def test_hash_different_shifts() -> None:
    course1 = Course('Sistemas Operativos')
    course2 = Course('Sistemas Operativos', [Shift(ShiftType.T, 2)])
    assert hash(course1) == hash(course2)

def test_repr() -> None:
    shift = Shift(ShiftType.T, 2)
    course = Course('Cálculo de Programas', [shift])
    assert repr(course) == f'Course(name=\'Cálculo de Programas\', shifts={{\'T2\': {shift!r}}})'
