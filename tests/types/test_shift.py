import copy
import datetime
import typing

import pytest

from scheduler.types.course import Course
from scheduler.types.room import Room
from scheduler.types.shift import Shift, ShiftError, ShiftType
from scheduler.types.weekday import Weekday

def test_shift_type_repr() -> None:
    assert repr(ShiftType.PL) == '<ShiftType.PL: \'PL\'>'

def test_shift_type_str() -> None:
    assert str(ShiftType.TP) == 'TP'

reference_shift: Shift

@pytest.fixture(autouse=True)
def initialize_reference_shift() -> None:
    global reference_shift
    reference_shift = Shift(
        Course('Cálculo de Programas'),
        ShiftType.T,
        1,
        Weekday.MONDAY,
        datetime.time(10, 0),
        datetime.time(12, 0),
        Room('CP1', '0.08', 200)
    )

def shift_with(shift: Shift, property_name: str, property_value: typing.Any) -> Shift:
    shift2 = copy.copy(shift)
    setattr(shift2, f'_Shift__{property_name}', property_value)
    return shift2

def test_init() -> None:
    assert reference_shift.course == Course('Cálculo de Programas')
    assert reference_shift.shift_type == ShiftType.T
    assert reference_shift.number == 1
    assert reference_shift.day == Weekday.MONDAY
    assert reference_shift.start == datetime.time(10, 0)
    assert reference_shift.end == datetime.time(12, 0)
    assert reference_shift.room == Room('CP1', '0.08', 200)

def test_init_equal_start_end() -> None:
    with pytest.raises(ShiftError):
        copy.copy(shift_with(reference_shift, 'start', datetime.time(12, 0)))

def test_init_start_after_end() -> None:
    with pytest.raises(ShiftError):
        copy.copy(shift_with(reference_shift, 'start', datetime.time(12, 30)))

def test_id() -> None:
    assert reference_shift.id == 'Cálculo de Programas T1'

def test_name() -> None:
    assert reference_shift.name == 'T1'

def test_capacity_valid() -> None:
    assert reference_shift.capacity == 200

def test_capacity_invalid() -> None:
    invalid_capacity_shift = shift_with(reference_shift, 'room', Room('CP1', '0.08'))
    with pytest.raises(ShiftError):
        invalid_capacity_shift.capacity

def test_overlaps_same() -> None:
    assert reference_shift.overlaps(reference_shift)

def test_overlaps_no_overlap() -> None:
    other = shift_with(
        shift_with(reference_shift, 'end', datetime.time(15, 0)), 'start', datetime.time(13, 0)
    )

    assert not reference_shift.overlaps(other)
    assert not other.overlaps(reference_shift)

def test_overlaps_different_day() -> None:
    other = shift_with(reference_shift, 'day', Weekday.WEDNESDAY)
    assert not reference_shift.overlaps(other)

def test_overlaps_sequence() -> None:
    other = shift_with(
        shift_with(reference_shift, 'end', datetime.time(14, 0)), 'start', datetime.time(12, 0)
    )

    assert not reference_shift.overlaps(other)
    assert not other.overlaps(reference_shift)

def test_overlaps_overlap() -> None:
    other = shift_with(
        shift_with(reference_shift, 'end', datetime.time(13, 30)), 'start', datetime.time(11, 30)
    )

    assert reference_shift.overlaps(other)
    assert other.overlaps(reference_shift)

def test_eq_none() -> None:
    assert reference_shift != None

def test_eq_same() -> None:
    assert reference_shift == reference_shift

def test_eq_equals_and_copy() -> None:
    assert reference_shift == copy.copy(reference_shift)

def test_eq_different_course() -> None:
    assert reference_shift != shift_with(reference_shift, 'course', Course('Álgebra Linear'))

def test_eq_different_type() -> None:
    assert reference_shift != shift_with(reference_shift, 'shift_type', ShiftType.TP)

def test_eq_different_number() -> None:
    assert reference_shift != shift_with(reference_shift, 'number', 2)

def test_eq_different_day() -> None:
    assert reference_shift != shift_with(reference_shift, 'day', Weekday.THURSDAY)

def test_eq_same_start() -> None:
    assert reference_shift == shift_with(reference_shift, 'start', datetime.time(10))

def test_eq_different_start() -> None:
    assert reference_shift != shift_with(reference_shift, 'start', datetime.time(10, 5))

def test_eq_different_end() -> None:
    assert reference_shift != shift_with(reference_shift, 'end', datetime.time(12, 30))

def test_eq_different_room() -> None:
    assert reference_shift != shift_with(reference_shift, 'room', Room('CP1', '0.08'))

def test_hash_same() -> None:
    assert hash(reference_shift) == hash(reference_shift)

def test_hash_equals() -> None:
    assert hash(reference_shift) == hash(copy.copy(reference_shift))

def test_hash_different_course() -> None:
    assert \
        hash(reference_shift) != \
        hash(shift_with(reference_shift, 'course', Course('Álgebra Linear')))

def test_hash_different_type() -> None:
    assert hash(reference_shift) != hash(shift_with(reference_shift, 'shift_type', ShiftType.TP))

def test_hash_different_number() -> None:
    assert hash(reference_shift) != hash(shift_with(reference_shift, 'number', 2))

def test_hash_different_day() -> None:
    assert hash(reference_shift) == hash(shift_with(reference_shift, 'day', Weekday.THURSDAY))

def test_hash_different_start() -> None:
    assert hash(reference_shift) == hash(shift_with(reference_shift, 'start', datetime.time(10, 5)))

def test_hash_different_end() -> None:
    assert hash(reference_shift) == hash(shift_with(reference_shift, 'end', datetime.time(12, 30)))

def test_hash_different_room() -> None:
    assert hash(reference_shift) == hash(shift_with(reference_shift, 'room', Room('CP1', '0.08')))

def test_repr() -> None:
    assert repr(reference_shift) == \
        'Shift(course=Course(id=\'Cálculo de Programas\', ...), shift_type=T, number=1, ' \
        'day=Monday, start=10:00:00, end=12:00:00, ' \
        'room=Room(building=\'CP1\', name_in_building=\'0.08\', capacity=200))'

def test_str() -> None:
    assert str(reference_shift) == \
        'Shift(course=Course(id=\'Cálculo de Programas\', ...), shift_type=T, number=1, ' \
        'day=Monday, start=10:00:00, end=12:00:00, ' \
        'room=Room(building=\'CP1\', name_in_building=\'0.08\', capacity=200))'

def test_parse_name_valid() -> None:
    assert Shift.parse_name('T2') == (ShiftType.T, 2)
    assert Shift.parse_name('TP1') == (ShiftType.TP, 1)
    assert Shift.parse_name('PL10') == (ShiftType.PL, 10)
    assert Shift.parse_name('OT5') == (ShiftType.OT, 5)

def test_parse_name_invalid() -> None:
    with pytest.raises(ShiftError):
        Shift.parse_name('T')

    with pytest.raises(ShiftError):
        Shift.parse_name('TL2')

    with pytest.raises(ShiftError):
        Shift.parse_name('2')
