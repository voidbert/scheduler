from __future__ import annotations
import copy
import typing

from .course import Course

class StudentError(Exception):
    pass

class Student:
    def __init__(self, number: str, courses: None | list[Course] = None) -> None:
        self.__number = number
        self.__courses: dict[str, Course] = {}

        if courses:
            for course in courses:
                self.add_course(course)

    def add_course(self, course: Course) -> None:
        if course.id in self.__courses:
            raise StudentError('Tried to add a course to a student more than once')

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

        return self.__number == other.number and list(self.__courses) == list(other.courses)

    def __copy__(self) -> Student:
        return Student(self.__number, list(self.__courses.values()))

    def __hash__(self) -> int:
        return hash(self.__number)

    def __repr__(self) -> str:
        return f'Student(number={self.__number!r}, courses={self.__courses!r})'
