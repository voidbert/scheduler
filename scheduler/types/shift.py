from __future__ import annotations
import copy
import enum
import re
import typing

from .room import Room, RoomError
from .timeslot import Timeslot

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
        timeslots: list[Timeslot],
        room: Room,
    ) -> None:
        self.__course = course
        self.__shift_type = shift_type
        self.__number = number
        self.__timeslots: list[Timeslot] = []
        self.__room = room

        for timeslot in timeslots:
            self.add_timeslot(timeslot)

        if not self.__timeslots:
            raise ShiftError('At least one shift timeslot is required')

    def add_timeslot(self, timeslot: Timeslot) -> None:
        for t in self.__timeslots:
            if t.overlaps(timeslot):
                raise ShiftError('Overlapping timeslots in shift')

        self.__timeslots.append(timeslot)

    def overlaps(self, other: Shift) -> bool:
        for self_timeslot in self.__timeslots:
            for other_timeslot in other.timeslots:
                if self_timeslot.overlaps(other_timeslot):
                    return True

        return False

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
    def timeslots(self) -> list[Timeslot]:
        return copy.copy(self.__timeslots)

    @property
    def room(self) -> Room:
        return self.__room

    @property
    def capacity(self) -> int:
        try:
            return self.__room.capacity
        except RoomError as e:
            raise ShiftError('Shift\'s room doesn\'t have a capacity defined') from e

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, Shift):
            return False

        return (
            self.__course.id == other.course.id and
            self.__shift_type == other.shift_type and
            self.__number == other.number and
            self.__timeslots == other.timeslots and
            self.__room == other.room
        )

    def __copy__(self) -> Shift:
        return Shift(
            self.__course,
            self.__shift_type,
            self.__number,
            self.__timeslots,
            self.__room
        )

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        # NOTE: don't call __repr__ on __course to avoid infinite recursion
        return \
            f'Shift(course=Course(id={self.__course.id!r}, ...), ' \
            f'shift_type={self.__shift_type}, number={self.__number!r}, ' \
            f'timeslots={self.__timeslots}, room={self.__room!r})'

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
