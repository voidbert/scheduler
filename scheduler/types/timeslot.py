from __future__ import annotations
import datetime
import typing

from .room import Room
from .weekday import Weekday

class TimeslotError(Exception):
    pass

class Timeslot:
    def __init__(self, day: Weekday, start: datetime.time, end: datetime.time, room: Room) -> None:
        if end <= start:
            raise TimeslotError(f'Timeslot\'s start ({start!r}) must precede its end ({end!r})')

        self.__day = day
        self.__start = start
        self.__end = end
        self.__room = room

    def overlaps(self, other: Timeslot) -> bool:
        return self.__day == other.day and self.__start < other.end and other.start < self.__end

    @property
    def day(self) -> Weekday:
        return self.__day

    @property
    def start(self) -> datetime.time:
        return self.__start

    @property
    def end(self) -> datetime.time:
        return self.__end

    @property
    def room(self) -> Room:
        return self.__room

    @property
    def capacity(self) -> None | int:
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
