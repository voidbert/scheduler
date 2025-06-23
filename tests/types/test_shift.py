import copy
import datetime
import typing

import pytest

from scheduler.types.course import Course
from scheduler.types.room import Room
from scheduler.types.shift import Shift, ShiftError, ShiftType
from scheduler.types.timeslot import Timeslot
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
        [Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0))],
        Room('CP1', '0.08', 200)
    )

def shift_with(shift: Shift, property_name: str, property_value: typing.Any) -> Shift:
    shift2 = copy.copy(shift)
    setattr(shift2, f'_Shift__{property_name}', property_value)
    return shift2

def test_init_valid() -> None:
    assert reference_shift.course == Course('Cálculo de Programas')
    assert reference_shift.shift_type == ShiftType.T
    assert reference_shift.number == 1
    assert reference_shift.timeslots == \
        [Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0))]
    assert reference_shift.room == Room('CP1', '0.08', 200)

def test_init_overlap() -> None:
    with pytest.raises(ShiftError):
        Shift(
            Course('Cálculo de Programas'),
            ShiftType.T,
            1,
            [
                Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0)),
                Timeslot(Weekday.MONDAY, datetime.time(11, 0), datetime.time(12, 0))
            ],
            Room('CP1', '0.08', 200)
        )

def test_init_no_timeslots() -> None:
    with pytest.raises(ShiftError):
        Shift(Course('Cálculo de Programas'), ShiftType.T, 1, [], Room('CP1', '0.08', 200))

def test_init_encapsulation() -> None:
    slots = [
        Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0)),
        Timeslot(Weekday.FRIDAY, datetime.time(11, 0), datetime.time(12, 0))
    ]

    shift = Shift(Course('Cálculo de Programas'), ShiftType.T, 1, slots, Room('CP1', '0.08', 200))
    assert len(shift.timeslots) == 2

    slots.append(Timeslot(Weekday.WEDNESDAY, datetime.time(11, 0), datetime.time(12, 0)))

    assert len(shift.timeslots) == 2

def test_add_timeslot_successful() -> None:
    reference_shift.add_timeslot(Timeslot(Weekday.MONDAY, datetime.time(7, 0), datetime.time(9, 0)))
    assert len(reference_shift.timeslots) == 2

def test_add_timeslot_unsuccessful() -> None:
    with pytest.raises(ShiftError):
        reference_shift.add_timeslot(
            Timeslot(Weekday.MONDAY, datetime.time(11, 0), datetime.time(12, 0))
        )

def test_overlaps() -> None:
    shift = Shift(
        Course('Cálculo de Programas'),
        ShiftType.T,
        1,
        [
            Timeslot(Weekday.MONDAY, datetime.time(8, 0), datetime.time(9, 0)),
            Timeslot(Weekday.MONDAY, datetime.time(13, 0), datetime.time(14, 0))
        ],
        Room('CP1', '0.08', 200)
    )

    assert not shift.overlaps(reference_shift)
    assert not reference_shift.overlaps(shift)

    reference_shift.add_timeslot(Timeslot(Weekday.MONDAY, datetime.time(7, 0), datetime.time(9, 0)))

    assert shift.overlaps(reference_shift)
    assert reference_shift.overlaps(shift)

def test_id() -> None:
    assert reference_shift.id == 'Cálculo de Programas T1'

def test_name() -> None:
    assert reference_shift.name == 'T1'

def test_timeslots_encapsulation() -> None:
    reference_shift.timeslots.append(
        Timeslot(Weekday.FRIDAY, datetime.time(16, 0), datetime.time(18, 0))
    )

    assert len(reference_shift.timeslots) == 1

def test_capacity_valid() -> None:
    assert reference_shift.capacity == 200

def test_capacity_invalid() -> None:
    invalid_capacity_shift = shift_with(reference_shift, 'room', Room('CP1', '0.08'))
    with pytest.raises(ShiftError):
        invalid_capacity_shift.capacity

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

def test_eq_different_timeslots() -> None:
    assert reference_shift != shift_with(reference_shift, 'timeslots', [])

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

def test_hash_different_timeslots() -> None:
    assert hash(reference_shift) == hash(shift_with(reference_shift, 'timeslots', []))

def test_hash_different_room() -> None:
    assert hash(reference_shift) == hash(shift_with(reference_shift, 'room', Room('CP1', '0.08')))

def test_repr() -> None:
    assert repr(reference_shift) == \
        'Shift(course=Course(id=\'Cálculo de Programas\', ...), shift_type=T, number=1, ' \
        'timeslots=[Timeslot(day=Monday, start=\'10:00:00\', end=\'12:00:00\')], ' \
        'room=Room(building=\'CP1\', name_in_building=\'0.08\', capacity=200))'

def test_str() -> None:
    assert str(reference_shift) == \
        'Shift(course=Course(id=\'Cálculo de Programas\', ...), shift_type=T, number=1, ' \
        'timeslots=[Timeslot(day=Monday, start=\'10:00:00\', end=\'12:00:00\')], ' \
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
