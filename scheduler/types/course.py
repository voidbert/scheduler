from __future__ import annotations
import copy
import typing

from .shift import Shift

class CourseError(Exception):
    '''Type of exception thrown by :class:`Course`.'''
    pass

class Course:
    '''
    A course that a student may be enrolled in. A course is characterized by its name and its
    shifts. Courses are divided into shifts to allow for a higher number of enrolled students, and a
    student must be attributed, for every course, a single shift of each type the course has.

    :param name:   Full name of the course.
    :param shifts: List of shifts of the course. No shifts will be copied. When ``None`` (default),
                   no shifts will be added to the course.

    :raises CourseError: ``shifts`` has more than one shift with the same :attr:`~.shift.Shift.id`.
    '''

    def __init__(self, name: str, shifts: None | list[Shift] = None) -> None:
        self.__name = name
        self.__shifts: dict[str, Shift] = {}

        if shifts:
            for shift in shifts:
                self.add_shift(shift)

    def add_shift(self, shift: Shift) -> None:
        '''
        Adds a shift to the course.

        :param shift: Shift to be added to the course.

        :raises CourseError: The course already has a shift with the same :attr:`~.shift.Shift.id`.

        >>> course = Course('Computer Graphics')
        >>> course.add_shift(Shift(ShiftType.PL, 1))
        >>> course.shifts
        {'PL1': Shift(shift_type=ShiftType.PL, number=1, timeslots=[])}
        '''

        if shift.id in self.__shifts:
            raise CourseError('Tried to add a shift to a course more than once')
        else:
            self.__shifts[shift.id] = shift

    @property
    def id(self) -> str:
        '''Identifier (the full name) of the course. Same as :attr:`name`.'''
        return self.__name

    @property
    def name(self) -> str:
        '''
        The full name of the course.

        >>> Course('Software Labs I').name
        'Software Labs I'
        '''

        return self.__name

    @property
    def shifts(self) -> dict[str, Shift]:
        '''
        Association between shift identifiers (:attr:`~.course.Shift.id`) and the shifts that are
        part of the course.

        **A copy of the dictionary will be returned**, but the references to the shifts will not.

        >>> Course('Software Labs I', [Shift(ShiftType.PL, 1)]).shifts
        {'PL1': Shift(shift_type=ShiftType.PL, number=1, timeslots=[])}
        '''

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
