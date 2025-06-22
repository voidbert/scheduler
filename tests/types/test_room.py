import copy

import pytest

from scheduler.types.room import Room, RoomError

def test_init_no_capacity() -> None:
    room = Room('CP2', '1.01')

    assert room.building == 'CP2'
    assert room.name_in_building == '1.01'
    assert not room.has_valid_capacity()

def test_init_with_capacity() -> None:
    room = Room('CP3', '2.04', 50)

    assert room.building == 'CP3'
    assert room.name_in_building == '2.04'
    assert room.capacity == 50

def test_id() -> None:
    assert Room('Ed 7', '1.04').id == 'Ed 7 1.04'

def test_name() -> None:
    assert Room('Ed 7', '1.04').id == 'Ed 7 1.04'

def test_capacity_getter_zero() -> None:
    with pytest.raises(RoomError):
        Room('Ed 7', '1.08').capacity

def test_capacity_getter_negative() -> None:
    with pytest.raises(RoomError):
        Room('Ed 7', '1.08', -1).capacity

def test_capacity_getter_positive() -> None:
    assert Room('Ed 7', '1.08', 20).capacity == 20

def test_capacity_setter_zero() -> None:
    room = Room('Ed 7', '1.08')
    room.capacity = 0
    assert not room.has_valid_capacity()

def test_capacity_setter_negative() -> None:
    room = Room('Ed 7', '1.08')
    room.capacity = -1
    assert not room.has_valid_capacity()

def test_capacity_setter_positive() -> None:
    room = Room('Ed 7', '1.08')
    room.capacity = 20

    assert room.has_valid_capacity()
    assert room.capacity == 20

def test_eq_none() -> None:
    assert Room('CP2', '1.05') != None

def test_eq_same() -> None:
    room = Room('CP2', '1.05')
    assert room == room

def test_eq_equals() -> None:
    room1 = Room('CP2', '1.05')
    room2 = Room('CP2', '1.05')
    assert room1 == room2

def test_eq_different_building() -> None:
    room1 = Room('CP2', '1.05')
    room2 = Room('CP3', '1.05')
    assert room1 != room2

def test_eq_different_name_in_building() -> None:
    room1 = Room('CP2', '1.05')
    room2 = Room('CP2', '1.07')
    assert room1 != room2

def test_eq_same_capacity_both_positive() -> None:
    room1 = Room('CP2', '1.05', 60)
    room2 = Room('CP2', '1.05', 60)
    assert room1 == room2

def test_eq_same_capacity_both_negative() -> None:
    room1 = Room('CP2', '1.05', 0)
    room2 = Room('CP2', '1.05', -5)
    assert room1 == room2

def test_eq_different_capacity_both_positive() -> None:
    room1 = Room('CP2', '1.05', 60)
    room2 = Room('CP2', '1.05', 30)
    assert room1 != room2

def test_eq_different_capacity() -> None:
    room1 = Room('CP2', '1.05', 60)
    room2 = Room('CP2', '1.05', -5)
    assert room1 != room2

def test_copy_valid_capacity() -> None:
    room1 = Room('Ed 7', '1.04', 15)
    room2 = copy.copy(room1)

    assert room1 == room2

    room2.capacity = 20
    assert room1.capacity == 15

def test_copy_valid_invalid_capacity() -> None:
    room1 = Room('Ed 7', '1.04')
    room2 = copy.copy(room1)

    assert room1 == room2

    room2.capacity = 20
    assert not room1.has_valid_capacity()

def test_hash_same() -> None:
    room = Room('CP2', '1.05')
    assert hash(room) == hash(room)

def test_hash_equals() -> None:
    room1 = Room('CP2', '1.05')
    room2 = Room('CP2', '1.05')
    assert hash(room1) == hash(room2)

def test_hash_different_building() -> None:
    room1 = Room('CP2', '1.05')
    room2 = Room('CP3', '1.05')
    assert hash(room1) != hash(room2)

def test_hash_different_name_in_building() -> None:
    room1 = Room('CP2', '1.05')
    room2 = Room('CP2', '1.07')
    assert hash(room1) != hash(room2)

def test_hash_different_capacity() -> None:
    room1 = Room('CP2', '1.05', 20)
    room2 = Room('CP2', '1.05', 10)
    assert hash(room1) == hash(room2)

def test_repr_valid_capacity() -> None:
    room = Room('Ed 7', '1.04', 15)
    assert repr(room) == 'Room(building=\'Ed 7\', name_in_building=\'1.04\', capacity=15)'

def test_repr_invalid_capacity() -> None:
    room = Room('Ed 7', '1.04')
    assert repr(room) == 'Room(building=\'Ed 7\', name_in_building=\'1.04\', capacity=UNKNOWN)'

def test_str_valid_capacity() -> None:
    room = Room('Ed 7', '1.04', 15)
    assert repr(room) == 'Room(building=\'Ed 7\', name_in_building=\'1.04\', capacity=15)'

def test_str_invalid_capacity() -> None:
    room = Room('Ed 7', '1.04')
    assert repr(room) == 'Room(building=\'Ed 7\', name_in_building=\'1.04\', capacity=UNKNOWN)'
