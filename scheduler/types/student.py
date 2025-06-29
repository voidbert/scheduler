from __future__ import annotations
import copy
import typing

from .course import Course

class StudentError(Exception):
    '''Type of exception thrown by :class:`Student`.'''
    pass

class Student:
    '''
    A student enrolled in the university. It is characterized by its mechanographic number and the
    courses they are enrolled in.

    :param number:  Mechanographic number of the student, that identifies it.
    :param courses: List of courses the student is enrolled in. No courses will be copied. When
                    ``None`` (default), no courses will be added to the student.

    :raises StudentError: ``courses`` has more than one course with the same
                           :attr:`~.course.Course.id`.
    '''

    def __init__(self, number: str, courses: None | list[Course] = None) -> None:
        self.__number = number
        self.__courses: dict[str, Course] = {}

        if courses:
            for course in courses:
                self.add_course(course)

    def add_course(self, course: Course) -> None:
        '''
        Adds a course to the list of courses the student is enrolled in.

        :param course: Course to enroll the student in. It will not be copied.

        :raises StudentError: The student is already enrolled in a course with the same
                              :attr:`~.course.Course.id`.

        >>> student = Student('A10400')
        >>> student.add_course(Course('Software Labs II'))
        >>> student.courses
        {'Software Labes II': Course(name='Software Labs II', shifts={})}
        '''

        if course.id in self.__courses:
            raise StudentError('Tried to add a course to a student more than once')

        self.__courses[course.id] = course

    @property
    def number(self) -> str:
        '''
        Mechanographic number of the student, that identifies it.

        >>> Student('A104000').number
        'A104000'
        '''

        return self.__number

    @property
    def courses(self) -> dict[str, Course]:
        '''
        Association between course identifiers (:attr:`~.course.Course.id`) and the courses the
        student is enrolled in.

        **A copy of the dictionary will be returned**, but the references to the courses will not.

        >>> Student('A104000', [Course('Software Labs II')]).courses
        {'Software Labes II': Course(name='Software Labs II', shifts={})}
        '''

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
