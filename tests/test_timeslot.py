import copy
import datetime

import pytest

from scheduler.types.room import Room
from scheduler.types.timeslot import Timeslot, TimeslotError
from scheduler.types.weekday import Weekday

room_1: Room
room_2: Room
room_3: Room

@pytest.fixture(autouse=True)
def initialize_reference_rooms() -> None:
    global room_1, room_2, room_3
    room_1 = Room('CP1', '0.08')
    room_2 = Room('CP1', '0.08', 200)
    room_3 = Room('CP1', '0.04')

def test_init_valid() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)

    assert timeslot.day == Weekday.MONDAY
    assert timeslot.start == datetime.time(9, 0)
    assert timeslot.end == datetime.time(11, 0)
    assert timeslot.room is room_1

def test_init_invalid_start_after_end() -> None:
    with pytest.raises(TimeslotError):
        Timeslot(Weekday.MONDAY, datetime.time(11, 0), datetime.time(9, 0), room_1)

def test_init_invalid_start_equals_end() -> None:
    with pytest.raises(TimeslotError):
        Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(9, 0), room_1)

def test_overlaps_same() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)
    assert timeslot.overlaps(timeslot)

def test_overlaps_no_overlap() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(14, 0), datetime.time(16, 0), room_1)

    assert not timeslot1.overlaps(timeslot2)
    assert not timeslot2.overlaps(timeslot1)

def test_overlaps_different_day() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)
    timeslot2 = Timeslot(Weekday.TUESDAY, datetime.time(10, 0), datetime.time(12, 0), room_1)

    assert not timeslot1.overlaps(timeslot2)
    assert not timeslot2.overlaps(timeslot1)

def test_overlaps_sequence() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)
    timeslot2 = Timeslot(Weekday.TUESDAY, datetime.time(11, 0), datetime.time(13, 0), room_1)

    assert not timeslot1.overlaps(timeslot2)
    assert not timeslot2.overlaps(timeslot1)

def test_overlaps_inside() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 30), datetime.time(10, 30), room_1)

    assert timeslot1.overlaps(timeslot2)
    assert timeslot2.overlaps(timeslot1)

def test_overlaps_partial_overlap() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(10, 0), datetime.time(12, 0), room_1)

    assert timeslot1.overlaps(timeslot2)
    assert timeslot2.overlaps(timeslot1)

def test_capacity_valid() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    assert timeslot.capacity == 200

def test_capacity_unset() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)
    assert timeslot.capacity is None

def test_eq_none() -> None:
    assert Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2) != None

def test_eq_same() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    assert timeslot == timeslot

def test_eq_equals() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    assert timeslot1 == timeslot2

def test_eq_different_day() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    timeslot2 = Timeslot(Weekday.FRIDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    assert timeslot1 != timeslot2

def test_eq_different_start() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 30), datetime.time(11, 0), room_2)
    assert timeslot1 != timeslot2

def test_eq_same_start() -> None:
    # NOTE: test if datetime.time(n) == datetime.time(n, 0)
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9), datetime.time(11, 0), room_2)
    assert timeslot1 == timeslot2

def test_eq_different_end() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(12, 0), room_2)
    assert timeslot1 != timeslot2

def test_eq_different_room_different_id() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_3)
    assert timeslot1 != timeslot2

def test_eq_different_room_same_id() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    assert timeslot1 == timeslot2

def test_copy() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_3)
    assert timeslot == copy.copy(timeslot)

def test_copy_encapsulation() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_3)
    timeslot2 = copy.copy(timeslot1)
    assert timeslot2.room is room_3

def test_hash_same() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    assert hash(timeslot) == hash(timeslot)

def test_hash_equals() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    assert hash(timeslot) == hash(copy.copy(timeslot))

def test_hash_different_day() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    timeslot2 = Timeslot(Weekday.WEDNESDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    assert hash(timeslot1) != hash(timeslot2)

def test_hash_different_start() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 30), datetime.time(11, 0), room_2)
    assert hash(timeslot1) != hash(timeslot2)

def test_hash_different_end() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_2)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(12, 0), room_2)
    assert hash(timeslot1) != hash(timeslot2)

def test_hash_different_room_different_id() -> None:
    timeslot1 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)
    timeslot2 = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_3)
    assert hash(timeslot1) != hash(timeslot2)

def test_repr() -> None:
    timeslot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room_1)
    assert repr(timeslot) == (
        'Timeslot('
        'day=Weekday.MONDAY, '
        'start=datetime.time(9, 0), '
        'end=datetime.time(11, 0), '
        f'room={room_1!r})'
    )
