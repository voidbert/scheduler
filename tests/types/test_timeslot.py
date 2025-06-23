import copy
import datetime

import pytest

from scheduler.types.timeslot import Timeslot, TimeslotError
from scheduler.types.weekday import Weekday

def test_init_valid() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))

    assert timeslot.day == Weekday.MONDAY
    assert timeslot.start == datetime.time(9, 0)
    assert timeslot.end == datetime.time(11, 0)

def test_init_invalid() -> None:
    with pytest.raises(TimeslotError):
        Timeslot(Weekday.MONDAY, datetime.time(11, 0), datetime.time(9, 0))

def test_overlaps_same() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    assert timeslot.overlaps(timeslot)

def test_overlaps_no_overlap() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(14, 0), datetime.time(16, 0))

    assert not timeslot1.overlaps(timeslot2)
    assert not timeslot2.overlaps(timeslot1)

def test_overlaps_different_day() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.TUESDAY, datetime.time(10, 0), datetime.time(12, 0))

    assert not timeslot1.overlaps(timeslot2)
    assert not timeslot2.overlaps(timeslot1)

def test_overlaps_sequence() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.TUESDAY, datetime.time(11, 0), datetime.time(13, 0))

    assert not timeslot1.overlaps(timeslot2)
    assert not timeslot2.overlaps(timeslot1)

def test_overlaps_inside() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 30), datetime.time(10, 30))

    assert timeslot1.overlaps(timeslot2)
    assert timeslot2.overlaps(timeslot1)

def test_overlaps_overlap() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0))

    assert timeslot1.overlaps(timeslot2)
    assert timeslot2.overlaps(timeslot1)

def test_eq_none() -> None:
    assert Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0)) != None

def test_eq_same() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    assert timeslot == timeslot

def test_eq_equals_and_copy() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = copy.copy(timeslot1)
    assert timeslot1 == timeslot2

def test_eq_different_day() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.WEDNESDAY, datetime.time(9, 0), datetime.time(11, 0))
    assert timeslot1 != timeslot2

def test_eq_different_start() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 30), datetime.time(11, 0))
    assert timeslot1 != timeslot2

def test_eq_same_start() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9), datetime.time(11, 0))
    assert timeslot1 == timeslot2

def test_eq_different_end() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(12, 0))
    assert timeslot1 != timeslot2

def test_hash_same() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    assert hash(timeslot) == hash(timeslot)

def test_hash_equals() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    assert hash(timeslot) == hash(copy.copy(timeslot))

def test_hash_different_day() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.WEDNESDAY, datetime.time(9, 0), datetime.time(11, 0))
    assert hash(timeslot1) != hash(timeslot2)

def test_hash_different_start() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 30), datetime.time(11, 0))
    assert hash(timeslot1) != hash(timeslot2)

def test_hash_different_end() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(12, 0))
    assert hash(timeslot1) != hash(timeslot2)

def test_repr() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    assert repr(timeslot) == 'Timeslot(day=Monday, start=\'09:00:00\', end=\'11:00:00\')'

def test_str() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0))
    assert str(timeslot) == 'Timeslot(day=Monday, start=\'09:00:00\', end=\'11:00:00\')'
