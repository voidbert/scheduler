from __future__ import annotations
import copy
import typing

from .shift import Shift

class CourseError(Exception):
    pass

class Course:
    def __init__(self, name: str, shifts: None | list[Shift] = None) -> None:
        self.__name = name
        self.__shifts: dict[str, Shift] = {}

        if shifts:
            for shift in shifts:
                self.add_shift(shift)

    def add_shift(self, shift: Shift) -> None:
        if shift.id in self.__shifts:
            raise CourseError('Tried to add a shift to a course more than once')
        else:
            self.__shifts[shift.id] = shift

    @property
    def id(self) -> str:
        return self.__name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def shifts(self) -> dict[str, Shift]:
        return copy.copy(self.__shifts)

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, Course):
            return False

        return self.__name == other.name and list(self.__shifts) == list(other.shifts)

    def __copy__(self) -> Course:
        return Course(self.__name, list(self.__shifts.values()))

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f'Course(name={self.__name!r}, shifts={self.__shifts!r})'
