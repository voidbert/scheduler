from __future__ import annotations
from collections.abc import Mapping
import copy

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
    :param shifts: List of shifts of the course.

    :raises CourseError: ``shifts`` has more than one shift with the same
                         :attr:`~.shift.Shift.name`.

    See :ref:`this <encapsulation>` to learn how objects and collections are copied.
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

        :raises CourseError: The course already has a shift with the same
                             :attr:`~.shift.Shift.name`.

        >>> course = Course('Computer Graphics')
        >>> course.add_shift(Shift(ShiftType.PL, 1))
        >>> course.shifts
        {'PL1': Shift(shift_type=ShiftType.PL, number=1, timeslots=[])}

        See :ref:`this <encapsulation>` to learn how objects and collections are copied.
        '''

        if shift.name in self.__shifts:
            raise CourseError('Tried to add a shift to a course more than once')
        else:
            self.__shifts[shift.name] = shift

    @property
    def name(self) -> str:
        '''
        The full name of the course. Can be used to identify the course.

        >>> Course('Software Labs I').name
        'Software Labs I'
        '''

        return self.__name

    @property
    def shifts(self) -> Mapping[str, Shift]:
        '''
        Association between shift names (:attr:`~.course.Shift.name`) and the shifts that are part
        of the course.

        >>> Course('Software Labs I', [Shift(ShiftType.PL, 1)]).shifts
        {'PL1': Shift(shift_type=ShiftType.PL, number=1, timeslots=[])}

        See :ref:`this <encapsulation>` to learn how objects and collections are copied.
        '''

        return self.__shifts

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Course):
            return False

        return self.__name == other.name and list(self.__shifts) == list(other.shifts)

    def __copy__(self) -> Course:
        return Course(self.__name, list(self.__shifts.values()))

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f'Course(name={self.__name!r}, shifts={self.__shifts!r})'
