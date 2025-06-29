import copy

import pytest

from scheduler.types.room import Room, RoomError

def test_init_no_capacity() -> None:
    room = Room('CP2', '1.01')

    assert room.building == 'CP2'
    assert room.name_in_building == '1.01'
    assert room.capacity is None

def test_init_valid_capacity() -> None:
    room = Room('CP3', '2.04', 50)

    assert room.building == 'CP3'
    assert room.name_in_building == '2.04'
    assert room.capacity == 50

def test_init_invalid_capacity_zero() -> None:
    with pytest.raises(RoomError):
        Room('CP1', '0.08', 0)

def test_init_invalid_capacity_negative() -> None:
    with pytest.raises(RoomError):
        Room('Ed 7', '1.04', -1)

def test_name() -> None:
    assert Room('Ed 7', '1.04').name == 'Ed 7 1.04'

def test_capacity_setter_positive() -> None:
    room = Room('Ed 7', '1.08')
    room.capacity = 20
    assert room.capacity == 20

def test_capacity_setter_zero() -> None:
    room = Room('Ed 7', '1.08')
    with pytest.raises(RoomError):
        room.capacity = 0

def test_capacity_setter_negative() -> None:
    room = Room('Ed 7', '1.08')
    with pytest.raises(RoomError):
        room.capacity = -1

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

def test_eq_different_capacity_both_valid() -> None:
    room1 = Room('CP2', '1.05', 60)
    room2 = Room('CP2', '1.05', 40)
    assert room1 != room2

def test_eq_different_capacity_one_valid() -> None:
    room1 = Room('CP2', '1.05', 60)
    room2 = Room('CP2', '1.05', None)
    assert room1 != room2

def test_copy() -> None:
    room = Room('CP2', '1.05')
    assert room == copy.copy(room)

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
    assert repr(room) == 'Room(building=\'Ed 7\', name_in_building=\'1.04\', capacity=None)'
