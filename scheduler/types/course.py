from __future__ import annotations
import copy
import typing
import unicodedata

from .ellipsis import EllipsisRepr

if typing.TYPE_CHECKING: # pragma: no cover
    from .student import Student

class CourseError(Exception):
    pass

class Course:
    def __init__(self, name: str, students: None | dict[str, Student] = None) -> None:
        normalized_name = unicodedata.normalize('NFKD', name)
        unaccented_name = normalized_name.encode('ascii', 'ignore').decode('ascii')
        self.__id = ''.join(c for c in unaccented_name if c.isalnum())

        self.__name = unicodedata.normalize('NFC', name)

        if students is None:
            self.__students = {}
        elif any(student_number != student.number for student_number, student in students.items()):
            raise CourseError('students is not a mapping between student IDs and students')
        else:
            self.__students = copy.copy(students)

    def add_student(self, student: Student) -> None:
        if student.number in self.__students:
            raise CourseError('Tried to add a student to a course they\'re already in')

        self.__students[student.number] = student

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def students(self) -> dict[str, Student]:
        return copy.copy(self.__students)

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, Course):
            return False

        # NOTE: don't compare the values of __students to avoid infinite recursion
        return self.__name == other.name and list(self.__students) == list(other.students)

    def __copy__(self) -> Course:
        return Course(self.__name, self.students)

    def __hash__(self) -> int:
        return hash(self.__id)

    def __repr__(self) -> str:
        ellipsis = EllipsisRepr()
        showable_students = {number: ellipsis for number in self.__students}
        return f"Course(name={self.__name!r}, students={showable_students!r})"
