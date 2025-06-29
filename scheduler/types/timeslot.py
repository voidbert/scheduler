from __future__ import annotations
import datetime
import typing

from .room import Room
from .weekday import Weekday

class TimeslotError(Exception):
    '''Type of exception thrown by :class:`Timeslot`.'''
    pass

class Timeslot:
    '''
    The time and location (:class:`Room`) of a class (part of a :class:`Shift`). Note that a shift
    may be broken into many different timeslots, for example, by being broken into classes across
    multiple days.

    :param day:   Day of the class.
    :param start: Starting hour of the class.
    :param end:   Ending hour of the class.
    :param room:  Room where the class is taught. It will not be copied.

    :raises TimeslotError: If and only if ``end <= start``
    '''

    def __init__(self, day: Weekday, start: datetime.time, end: datetime.time, room: Room) -> None:
        if end <= start:
            raise TimeslotError(f'Timeslot\'s start ({start!r}) must precede its end ({end!r})')

        self.__day = day
        self.__start = start
        self.__end = end
        self.__room = room

    def overlaps(self, other: Timeslot) -> bool:
        '''
        Tests if there is overlap between two timeslots.

        :param other: Timeslot to test for overlap.

        >>> timeslot1 = Timeslot(Weekday.MONDAY, time(10, 0), time(12, 0), Room('CP1', '0.04'))
        >>> timeslot2 = Timeslot(Weekday.MONDAY, time(11, 0), time(13, 0), Room('CP1', '0.04'))
        >>> timeslot3 = Timeslot(Weekday.FRIDAY, time(10, 0), time(12, 0), Room('CP1', '0.04'))
        >>> timeslot1.overlaps(timeslot2)
        True
        >>> timeslot1.overlaps(timeslot3)
        False
        '''

        return self.__day == other.day and self.__start < other.end and other.start < self.__end

    @property
    def day(self) -> Weekday:
        '''
        Day of the class.

        >>> Timeslot(Weekday.THURSDAY, time(10, 0), time(12, 0), Room('CP1', '0.04', 150)).day
        Weekday.THURSDAY
        '''

        return self.__day

    @property
    def start(self) -> datetime.time:
        '''
        Starting hour of the class.

        >>> Timeslot(Weekday.THURSDAY, time(10, 0), time(12, 0), Room('CP1', '0.04', 150)).start
        datetime.time(10, 0)
        '''

        return self.__start

    @property
    def end(self) -> datetime.time:
        '''
        Ending hour of the class.

        >>> Timeslot(Weekday.THURSDAY, time(10, 0), time(12, 0), Room('CP1', '0.04', 150)).end
        datetime.time(12, 0)
        '''

        return self.__end

    @property
    def room(self) -> Room:
        '''
        Room where the class is taught. It will not be copied.

        >>> Timeslot(Weekday.THURSDAY, time(10, 0), time(12, 0), Room('CP1', '0.04', 150)).room
        Room(building='CP1', name_in_building='0.04', capacity=150)
        '''

        return self.__room

    @property
    def capacity(self) -> None | int:
        '''
        Capacity of the room where the class is taught. A value of ``None`` means the room's
        capacity is unknown.

        >>> Timeslot(Weekday.THURSDAY, time(10, 0), time(12, 0), Room('CP1', '0.04', 150)).capacity
        150
        '''

        return self.__room.capacity

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, Timeslot):
            return False

        return (
            self.__day == other.day and
            self.__start == other.start and
            self.__end == other.end and
            self.__room.id == other.room.id
        )

    def __copy__(self) -> Timeslot:
        return Timeslot(self.__day, self.__start, self.__end, self.__room)

    def __hash__(self) -> int:
        return hash((self.__day, self.__start, self.__end, self.__room))

    def __repr__(self) -> str:
        return (
            'Timeslot('
            f'day={self.__day!r}, '
            f'start={self.__start!r}, '
            f'end={self.__end!r}, '
            f'room={self.__room!r})'
        )
