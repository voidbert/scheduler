from __future__ import annotations
from collections.abc import Sequence
import copy
import enum
import re

from .timeslot import Timeslot

class ShiftError(Exception):
    '''Type of exception thrown by :class:`Shift`.'''
    pass

@enum.unique
class ShiftType(enum.StrEnum):
    '''Type of a :class:`Shift`.'''

    T = 'T'
    TP = 'TP'
    PL = 'PL'
    OT = 'OT'

    def __repr__(self) -> str:
        return f'ShiftType.{self}'

class Shift:
    '''
    Subdivision of a :class:`~.course.Course`, to allow for more enrolled students. A shift is
    characterized by its type, its number, and the timeslots that compose it. A shift may be
    composed of more than one timeslot because, for example, it can be broken in multiple classes
    across different days.

    :param shift_type: Type of the shift.
    :param number:     Number of the shift.
    :param timeslots:  List of timeslots of the shift.

    :raises ShiftError: ``timeslots`` overlap.

    See :ref:`this <encapsulation>` to learn how objects and collections are copied.
    '''

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
        '''
        Adds a timeslot to the shift.

        :param timeslot: Timeslot to be added to the shift.

        :raises ShiftError: ``timeslot`` overlaps with at least one of the shift's timeslots.

        >>> shift = Shift(ShiftType.T, 2)
        >>> timeslot = Timeslot(Weekday.MONDAY, time(10, 0), time(12, 0), Room('CP1', '0.04'))
        >>> shift.add_timeslot(timeslot)
        >>> shift.timeslots
        [Timeslot(day=Weekday.MONDAY, start=datetime.time(10, 0), ...)]

        See :ref:`this <encapsulation>` to learn how objects and collections are copied.
        '''

        for t in self.__timeslots:
            if t.overlaps(timeslot):
                raise ShiftError('Overlapping timeslots in shift')

        self.__timeslots.append(timeslot)

    def overlaps(self, other: Shift) -> bool:
        '''
        Checks if at least one of the timeslots of the shift overlaps with any of the timeslots in
        ``other``.

        :param other: Shift to test for overlapping timeslots.
        '''

        for self_timeslot in self.__timeslots:
            for other_timeslot in other.timeslots:
                if self_timeslot.overlaps(other_timeslot):
                    return True

        return False

    @property
    def shift_type(self) -> ShiftType:
        '''
        Type of the shift.

        >>> Shift(ShiftType.T, 2).shift_type
        ShiftType.T
        '''

        return self.__shift_type

    @property
    def number(self) -> int:
        '''
        Number of the shift.

        >>> Shift(ShiftType.T, 2).number
        2
        '''

        return self.__number

    @property
    def name(self) -> str:
        '''
        Name of the shift. Can be used to identify a shift in the context of its course (weak
        identifier). Append this name to the the :attr:`~.course.Course.name` of the course for a
        full identifier.

        >>> Shift(ShiftType.T, 2).name
        'T2'
        '''

        return f'{self.__shift_type}{self.__number}'

    @property
    def timeslots(self) -> Sequence[Timeslot]:
        '''
        List of timeslots that compose the shift.

        >>> slot1 = Timeslot(Weekday.MONDAY, time(9, 0), time(11, 0), Room('CP1', '0.20'))
        >>> slot2 = Timeslot(Weekday.MONDAY, time(14, 0), time(16, 0), Room('CP1', '0.20'))
        >>> shift = Shift(ShiftType.PL, 6, [slot1, slot2])
        >>> shift.timeslots
        [slot1, slot2]

        See :ref:`this <encapsulation>` to learn how objects and collections are copied.
        '''

        return self.__timeslots

    @property
    def capacity(self) -> None | int:
        '''
        Number of students that can be assigned to the shift. It is the capacity of the smallest
        room the shift has classes in. The value of this property is ``None`` when the shift has no
        timeslots, or when the room of one of the timeslots has an unknown
        :attr:`~.room.Room.capacity`.
        '''

        if not self.__timeslots or any(timeslot.capacity is None for timeslot in self.__timeslots):
            return None
        else:
            return min(
                timeslot.capacity for timeslot in self.__timeslots if timeslot.capacity is not None
            )

    def __eq__(self, other: object) -> bool:
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
        return hash(self.name)

    def __repr__(self) -> str:
        return (
            'Shift('
            f'shift_type={self.__shift_type!r}, '
            f'number={self.__number!r}, '
            f'timeslots={self.__timeslots})'
        )

    @staticmethod
    def parse_name(name: str) -> tuple[ShiftType, int]:
        '''
        Parses the name of a shift, decomposing it into a :class:`ShiftType` and the shift's number.

        :param name: Shift name to parse.
        :raises ShiftError: Invalid shift name.

        >>> Shift.parse_name('TP4')
        (ShiftType.TP, 4)
        '''

        shift_types_regex = '|'.join(ShiftType)
        match = re.match(rf'({shift_types_regex})([0-9]+)', name)

        if match is None:
            raise ShiftError(f'Failed to parse shift name: {name!r}')
        else:
            shift_type = ShiftType(match.group(1))
            number = int(match.group(2))
            return shift_type, number
