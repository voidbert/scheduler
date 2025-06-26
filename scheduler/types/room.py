from __future__ import annotations
import typing

class RoomError(Exception):
    pass

class Room:
    def __init__(self, building: str, name_in_building: str, capacity: None | int = None) -> None:
        self.__building = building
        self.__name_in_building = name_in_building
        self.capacity = capacity

    @property
    def id(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return f'{self.__building} {self.__name_in_building}'

    @property
    def building(self) -> str:
        return self.__building

    @property
    def name_in_building(self) -> str:
        return self.__name_in_building

    @property
    def capacity(self) -> None | int:
        return self.__capacity

    @capacity.setter
    def capacity(self, capacity: None | int) -> None:
        if capacity is not None and capacity <= 0:
            raise RoomError('Room\'s capacity must be positive')

        self.__capacity = capacity

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, Room):
            return False

        return (
            self.__building == other.building and
            self.__name_in_building == other.name_in_building and
            self.__capacity == other.capacity
        )

    def __copy__(self) -> Room:
        return Room(self.__building, self.__name_in_building, self.__capacity)

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            'Room('
            f'building={self.__building!r}, '
            f'name_in_building={self.__name_in_building!r}, '
            f'capacity={self.__capacity!r})'
        )
