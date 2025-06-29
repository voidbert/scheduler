from __future__ import annotations
import typing

class RoomError(Exception):
    '''Type of exception thrown by :class:`Room`.'''
    pass

class Room:
    '''
    A room in campus. It is characterized by the building it is in, its name in the building, and
    its capacity.

    :param building:         Name of the building the room is located in.
    :param name_in_building: Name of the room in the building (floor and number).
    :param capacity:         Number of students the room can sit. A value of ``None`` (default)
                             means the room's capacity is unknown.

    :raises RoomError: ``capacity`` is not positive.
    '''

    def __init__(self, building: str, name_in_building: str, capacity: None | int = None) -> None:
        self.__building = building
        self.__name_in_building = name_in_building
        self.capacity = capacity

    @property
    def name(self) -> str:
        '''
        Full name of the room, containing both the building and room names. Can be used to identify
        the room.

        >>> Room('CP1', '0.08').name
        'CP1 0.08'
        '''

        return f'{self.__building} {self.__name_in_building}'

    @property
    def building(self) -> str:
        '''
        Name of the building the room is located in.

        >>> Room('CP1', '0.08').building
        'CP1'
        '''

        return self.__building

    @property
    def name_in_building(self) -> str:
        '''
        Name of the room in its building (floor and number).

        >>> Room('CP1', '0.08').name_in_building
        '0.08'
        '''

        return self.__name_in_building

    @property
    def capacity(self) -> None | int:
        '''
        Number of students the room can sit. A value of ``None`` means the room's capacity is
        unknown.

        >>> Room('CP1', '0.08').capacity
        None
        >>> Room('CP1', '0.08', 250).capacity
        250

        This property can be also set:

        :raises RoomError: ``capacity`` is not positive.

        >>> room = Room('CP1', '0.08')
        >>> room.capacity = 250
        >>> room.capacity = None
        >>> room.capacity = -10
        scheduler.types.room.RoomError: Room's capacity must be positive
        '''

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
        return hash(self.name)

    def __repr__(self) -> str:
        return (
            'Room('
            f'building={self.__building!r}, '
            f'name_in_building={self.__name_in_building!r}, '
            f'capacity={self.__capacity!r})'
        )
