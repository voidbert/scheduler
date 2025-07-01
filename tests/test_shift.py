import copy
import datetime
import typing

import pytest

from scheduler.types.room import Room
from scheduler.types.shift import Shift, ShiftError, ShiftType
from scheduler.types.timeslot import Timeslot
from scheduler.types.weekday import Weekday

def test_shift_type_repr() -> None:
    assert repr(ShiftType.PL) == 'ShiftType.PL'

def test_shift_type_str() -> None:
    assert str(ShiftType.TP) == 'TP'

def test_init_default_timeslots() -> None:
    shift = Shift(ShiftType.PL, 1)

    assert shift.shift_type == ShiftType.PL
    assert shift.number == 1
    assert shift.timeslots == []

def test_init_no_timeslots() -> None:
    shift = Shift(ShiftType.TP, 10, [])

    assert shift.shift_type == ShiftType.TP
    assert shift.number == 10
    assert shift.timeslots == []

def test_init_valid_timeslots() -> None:
    slot = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), Room('CP1', '0.08'))
    shift = Shift(ShiftType.T, 2, [slot])

    assert shift.shift_type == ShiftType.T
    assert shift.number == 2
    assert shift.timeslots == [slot]

def test_init_invalid_timeslots_equals() -> None:
    slot = Timeslot(Weekday.FRIDAY, datetime.time(10, 0), datetime.time(12, 0), Room('CP2', '1.01'))

    with pytest.raises(ShiftError):
        shift = Shift(ShiftType.OT, 4, [slot, slot])

def test_init_invalid_timeslots_different() -> None:
    slot1 = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), Room('Ed 7', 'A1'))
    slot2 = Timeslot(Weekday.MONDAY, datetime.time(11, 0), datetime.time(13, 0), Room('Ed 7', 'A1'))

    with pytest.raises(ShiftError):
        shift = Shift(ShiftType.OT, 4, [slot1, slot2])

def test_init_encapsulation() -> None:
    slot = Timeslot(Weekday.FRIDAY, datetime.time(10, 0), datetime.time(12, 0), Room('Ed 7', 'A1'))
    slots = [slot]
    shift = Shift(ShiftType.OT, 1, [slot])

    assert len(shift.timeslots) == 1
    assert shift.timeslots[0] is slot

    slots.append(slot)
    assert len(shift.timeslots) == 1

def test_add_timeslot_valid_empty() -> None:
    slot = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), Room('CP1', '0.08'))
    shift = Shift(ShiftType.PL, 1, [])
    shift.add_timeslot(slot)

    assert shift.timeslots == [slot]
    assert shift.timeslots[0] is slot

def test_add_timeslot_valid_non_empty() -> None:
    slot1 = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), Room('Ed 7', 'A1'))
    slot2 = Timeslot(Weekday.FRIDAY, datetime.time(10, 0), datetime.time(12, 0), Room('Ed 7', 'A1'))
    shift = Shift(ShiftType.PL, 1, [slot1])

    shift.add_timeslot(slot2)
    assert shift.timeslots == [slot1, slot2]

def test_add_timeslot_invalid_equals() -> None:
    slot = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), Room('CP1', '0.08'))
    shift = Shift(ShiftType.PL, 1, [slot])

    with pytest.raises(ShiftError):
        shift.add_timeslot(slot)

def test_add_timeslot_invalid_different() -> None:
    slot1 = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(13, 0), Room('Ed 7', 'A1'))
    slot2 = Timeslot(Weekday.MONDAY, datetime.time(11, 0), datetime.time(12, 0), Room('Ed 7', 'A1'))
    shift = Shift(ShiftType.PL, 1, [slot1])

    with pytest.raises(ShiftError):
        shift.add_timeslot(slot2)

def test_overlaps_empty() -> None:
    assert not Shift(ShiftType.PL, 1, []).overlaps(Shift(ShiftType.T, 2, []))

def test_overlaps_single_disjoint() -> None:
    slot1 = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(13, 0), Room('Ed 7', 'A1'))
    slot2 = Timeslot(Weekday.FRIDAY, datetime.time(11, 0), datetime.time(12, 0), Room('Ed 7', 'A1'))
    assert not Shift(ShiftType.PL, 1, [slot1]).overlaps(Shift(ShiftType.T, 2, [slot2]))

def test_overlaps_single_overlapping() -> None:
    slot1 = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(13, 0), Room('Ed 7', 'A1'))
    slot2 = Timeslot(Weekday.MONDAY, datetime.time(11, 0), datetime.time(12, 0), Room('Ed 7', 'A1'))
    assert Shift(ShiftType.PL, 1, [slot1]).overlaps(Shift(ShiftType.T, 2, [slot2]))

def test_overlaps_multiple_non_overlapping() -> None:
    slot1 = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(13, 0), Room('Ed 7', 'A1'))
    slot2 = Timeslot(Weekday.FRIDAY, datetime.time(11, 0), datetime.time(13, 0), Room('Ed 7', 'A1'))
    slot3 = Timeslot(Weekday.TUESDAY, datetime.time(9, 0), datetime.time(11, 0), Room('Ed 7', 'A1'))
    assert not Shift(ShiftType.PL, 1, [slot1, slot2]).overlaps(Shift(ShiftType.T, 2, [slot3]))

def test_overlaps_multiple_overlapping() -> None:
    slot1 = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(13, 0), Room('Ed 7', 'A1'))
    slot2 = Timeslot(Weekday.FRIDAY, datetime.time(11, 0), datetime.time(13, 0), Room('Ed 7', 'A1'))
    slot3 = Timeslot(Weekday.FRIDAY, datetime.time(10, 0), datetime.time(12, 0), Room('Ed 7', 'A1'))
    assert Shift(ShiftType.PL, 1, [slot1, slot2]).overlaps(Shift(ShiftType.T, 2, [slot3]))

def test_name() -> None:
    assert Shift(ShiftType.T, 2, []).name == 'T2'

def test_timeslots_encapsulation() -> None:
    shift = Shift(ShiftType.T, 2, [])
    slot = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(13, 0), Room('Ed 7', 'A2'))

    slots = shift.timeslots
    shift.add_timeslot(slot)

    assert slots == [slot]

def test_capacity_no_timeslots() -> None:
    assert Shift(ShiftType.TP, 5, []).capacity is None

def test_capacity_one_unknown_capacity() -> None:
    room1 = Room('Ed 7', 'A1', 55)
    room2 = Room('Ed 7', 'A1')
    slot1 = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(13, 0), room1)
    slot2 = Timeslot(Weekday.FRIDAY, datetime.time(14, 0), datetime.time(16, 0), room2)

    assert Shift(ShiftType.T, 1, [slot1, slot2]).capacity is None

def test_capacity_all_known_capacity() -> None:
    room1 = Room('Ed 7', 'A1', 50)
    room2 = Room('Ed 7', 'A2', 60)
    slot1 = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(13, 0), room1)
    slot2 = Timeslot(Weekday.FRIDAY, datetime.time(14, 0), datetime.time(16, 0), room2)

    assert Shift(ShiftType.OT, 2, [slot1, slot2]).capacity == 50

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

def test_eq_none() -> None:
    assert Shift(ShiftType.T, 1, []) != None

def test_eq_same() -> None:
    shift = Shift(ShiftType.T, 1, [])
    assert shift == shift

def test_eq_equals() -> None:
    shift1 = Shift(ShiftType.T, 1, [])
    shift2 = Shift(ShiftType.T, 1, [])
    assert shift1 == shift2

def test_eq_different_type() -> None:
    shift1 = Shift(ShiftType.T, 1, [])
    shift2 = Shift(ShiftType.TP, 1, [])
    assert shift1 != shift2

def test_eq_different_number() -> None:
    shift1 = Shift(ShiftType.T, 1, [])
    shift2 = Shift(ShiftType.T, 2, [])
    assert shift1 != shift2

def test_eq_different_timeslots() -> None:
    slot = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), Room('CP1', '0.08'))
    shift1 = Shift(ShiftType.T, 1, [])
    shift2 = Shift(ShiftType.T, 1, [slot])
    assert shift1 != shift2

def test_copy() -> None:
    shift = Shift(ShiftType.TP, 3, [])
    assert shift == copy.copy(shift)

def test_copy_encapsulation() -> None:
    shift1 = Shift(ShiftType.TP, 3, [])
    shift2 = copy.copy(shift1)

    slot = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), Room('CP1', '0.04'))
    shift1.add_timeslot(slot)

    assert shift2.timeslots == []

def test_hash_same() -> None:
    shift = Shift(ShiftType.T, 1, [])
    assert hash(shift) == hash(shift)

def test_hash_equals() -> None:
    shift1 = Shift(ShiftType.T, 1, [])
    shift2 = Shift(ShiftType.T, 1, [])
    assert hash(shift1) == hash(shift2)

def test_hash_different_type() -> None:
    shift1 = Shift(ShiftType.T, 1, [])
    shift2 = Shift(ShiftType.TP, 1, [])
    assert hash(shift1) != hash(shift2)

def test_hash_different_number() -> None:
    shift1 = Shift(ShiftType.T, 1, [])
    shift2 = Shift(ShiftType.T, 2, [])
    assert hash(shift1) != hash(shift2)

def test_hash_different_timeslots() -> None:
    slot = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), Room('CP1', '0.08'))
    shift1 = Shift(ShiftType.T, 1, [])
    shift2 = Shift(ShiftType.T, 1, [slot])
    assert hash(shift1) == hash(shift2)

def test_repr() -> None:
    slot = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), Room('CP1', '0.08'))
    shift = Shift(ShiftType.TP, 2, [slot])

    assert repr(shift) == f'Shift(shift_type=ShiftType.TP, number=2, timeslots=[{slot!r}])'
