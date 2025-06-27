from __future__ import annotations
import copy
import enum
import re
import typing

from .timeslot import Timeslot

class ShiftError(Exception):
    pass

@enum.unique
class ShiftType(enum.StrEnum):
    T = 'T'
    TP = 'TP'
    PL = 'PL'
    OT = 'OT'

    def __repr__(self) -> str:
        return f'ShiftType.{self}'

class Shift:
    def __init__(
            self,
            shift_type: ShiftType,
            number: int,
            timeslots: None | list[Timeslot] = None
        ) -> None:

        self.__shift_type = shift_type
        self.__number = number
        self.__timeslots: list[Timeslot] = []

        if timeslots:
            for timeslot in timeslots:
                self.add_timeslot(timeslot)

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
        return self.name

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
    def capacity(self) -> None | int:
        if not self.__timeslots or any(timeslot.capacity is None for timeslot in self.__timeslots):
            return None
        else:
            return min(
                timeslot.capacity for timeslot in self.__timeslots if timeslot.capacity is not None
            )

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, Shift):
            return False

        return (
            self.__shift_type == other.shift_type and
            self.__number == other.number and
            self.__timeslots == other.timeslots
        )

    def __copy__(self) -> Shift:
        return Shift(self.__shift_type, self.__number, self.__timeslots)

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            'Shift('
            f'shift_type={self.__shift_type!r}, '
            f'number={self.__number!r}, '
            f'timeslots={self.__timeslots})'
        )

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
