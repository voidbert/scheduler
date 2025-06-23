from __future__ import annotations
import datetime
import enum
import re
import typing

from .room import Room, RoomError
from .weekday import Weekday

if typing.TYPE_CHECKING: # pragma: no cover
    from .course import Course

class ShiftError(Exception):
    pass

@enum.unique
class ShiftType(enum.StrEnum):
    T = 'T'
    TP = 'TP'
    PL = 'PL'
    OT = 'OT'

class Shift:
    def __init__(
        self,
        course: Course,
        shift_type: ShiftType,
        number: int,
        day: Weekday,
        start: datetime.time,
        end: datetime.time,
        room: Room,
    ) -> None:

        if end <= start:
            raise ShiftError('Shift\'s starting time must precede its ending time')

        self.__course = course
        self.__shift_type = shift_type
        self.__number = number
        self.__day = day
        self.__start = start
        self.__end = end
        self.__room = room

    @property
    def id(self) -> str:
        return f'{self.course.id} {self.name}'

    @property
    def course(self) -> Course:
        return self.__course

    @property
    def shift_type(self) -> ShiftType:
        return self.__shift_type

    @property
    def number(self) -> int:
        return self.__number

    @property
    def name(self) -> str:
        return f'{self.__shift_type}{self.__number}'

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
    def capacity(self) -> int:
        try:
            return self.__room.capacity
        except RoomError as e:
            raise ShiftError('Shift\'s room doesn\'t have a capacity defined') from e

    def overlaps(self, other: Shift) -> bool:
        return self.__day == other.day and self.__start < other.end and other.start < self.__end

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, Shift):
            return False

        return (
            self.__course.id == other.course.id and
            self.__shift_type == other.shift_type and
            self.__number == other.number and
            self.__day == other.day and
            self.__start == other.start and
            self.__end == other.end and
            self.__room == other.room
        )

    def __copy__(self) -> Shift:
        return Shift(
            self.__course,
            self.__shift_type,
            self.__number,
            self.__day,
            self.__start,
            self.__end,
            self.__room
        )

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        # NOTE: don't call __repr__ on __course to avoid infinite recursion
        return \
            f'Shift(course=Course(id={self.__course.id!r}, ...), ' \
            f'shift_type={self.__shift_type}, number={self.__number!r}, day={self.__day}, ' \
            f'start={self.__start}, end={self.__end}, room={self.__room!r})'

    @staticmethod
    def parse_name(name: str) -> tuple[ShiftType, int]:
        shift_types_regex = '|'.join(ShiftType)
        match = re.match(rf'({shift_types_regex})([0-9]+)', name)

        if match is None:
            raise ShiftError(f'Failed to parse shift name: {name!r}')
        else:
            shift_type = ShiftType(match.group(1))
            number = int(match.group(2))
            return shift_type, number
