from __future__ import annotations
import copy
import typing

from .ellipsis import EllipsisRepr
from .shift import Shift

if typing.TYPE_CHECKING: # pragma: no cover
    from .student import Student

class CourseError(Exception):
    pass

class Course:
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__shifts: dict[str, Shift] = {}
        self.__students: dict[str, Student] = {}

    def add_shift(self, shift: Shift) -> None:
        if shift.id in self.__shifts:
            raise CourseError('Tried to add the same shift to a course more than once')
        elif shift.course is not self:
            raise CourseError('Tried to add shift belonging to another course')
        else:
            self.__shifts[shift.id] = shift

    def add_student(self, student: Student) -> None:
        if student.number in self.__students:
            raise CourseError('Tried to add a student to a course they\'re already in')
        else:
            self.__students[student.number] = student

    @property
    def id(self) -> str:
        return self.__name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def shifts(self) -> dict[str, Shift]:
        return copy.copy(self.__shifts)

    @property
    def students(self) -> dict[str, Student]:
        return copy.copy(self.__students)

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, Course):
            return False

        # NOTE: don't compare the values of __students to avoid infinite recursion
        # NOTE: don't compare the values of __shifts for consistency with __students
        return (
            self.__name == other.name and
            list(self.__shifts) == list(other.shifts) and
            list(self.__students) == list(other.students)
        )

    def __copy__(self) -> Course:
        course = Course(self.__name)

        for shift in self.__shifts.values():
            course.add_shift(Shift(
                course,
                shift.shift_type,
                shift.number,
                shift.day,
                shift.start,
                shift.end,
                shift.room
            ))

        for student in self.__students.values():
            course.add_student(student)

        return course

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        # NOTE: don't call __repr__ on __students and __shifts to avoid infinite recursion
        ellipsis = EllipsisRepr()
        showable_students = {number: ellipsis for number in self.__students}
        showable_shifts = {shift.name: ellipsis for shift in self.__shifts.values()}

        return \
            f'Course(name={self.__name!r}, students={showable_students!r}, ' \
            f'shifts={showable_shifts})'
