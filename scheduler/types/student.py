from __future__ import annotations
import copy
import typing

from .ellipsis import EllipsisRepr

if typing.TYPE_CHECKING: # pragma: no cover
    from .course import Course

class StudentError(Exception):
    pass

class Student:
    def __init__(self, number: str) -> None:
        self.__number = number
        self.__courses: dict[str, Course] = {}

    def add_course(self, course: Course) -> None:
        if course.id in self.__courses:
            raise StudentError('Tried to add a student to a course they\'re already in')

        self.__courses[course.id] = course

    @property
    def number(self) -> str:
        return self.__number

    @property
    def courses(self) -> dict[str, Course]:
        return copy.copy(self.__courses)

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, Student):
            return False

        # NOTE: don't compare the values of __courses to avoid infinite recursion
        return self.__number == other.number and list(self.__courses) == list(other.courses)

    def __copy__(self) -> Student:
        student = Student(self.__number)
        for course in self.__courses.values():
            student.add_course(course)

        return student

    def __hash__(self) -> int:
        return hash(self.__number)

    def __repr__(self) -> str:
        # NOTE: don't call __repr__ on __courses to avoid infinite recursion
        ellipsis = EllipsisRepr()
        showable_courses = {id: ellipsis for id in self.__courses}

        return f'Student(number={self.__number!r}, courses={showable_courses!r})'
