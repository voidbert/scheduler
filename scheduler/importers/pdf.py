import os
import re

import pypdf

from .errors import ImporterError
from ..types import Course, CourseError, Student, StudentError

class BlackboardPdfImporter:
    def __init__(self) -> None:
        self.__courses: dict[str, Course] = {}
        self.__students: dict[str, Student] = {}
        self.__can_import_more = True

        self.__course_name_regex = re.compile(r'^\s+Nome do\s+(.+?)\s*$', flags=re.MULTILINE)
        self.__student_number_regex = re.compile(r'^\s+Email\s+(.+?)@', flags=re.MULTILINE)

    @property
    def students(self) -> dict[str, Student]:
        self.__can_import_more = False
        return self.__students

    @property
    def courses(self) -> dict[str, Course]:
        self.__can_import_more = False
        return self.__courses

    def load_pdf_directory(self, directory_path: str) -> None:
        if not self.__can_import_more:
            raise ImporterError('Cannot import more data after accessing .students or .courses')

        try:
            directory_contents = [
                os.path.join(directory_path, entry) for entry in os.listdir(directory_path)
            ]
            pdf_files = [entry for entry in directory_contents if self.__is_pdf_file(entry)]
        except IOError as e:
            raise ImporterError(f'Failed to list directory {directory_path}') from e

        for pdf_file in pdf_files:
            self.load_pdf(pdf_file)

    def load_pdf(self, file_path: str) -> None:
        if not self.__can_import_more:
            raise ImporterError('Cannot import more data after accessing .students or .courses')

        try:
            pdf_reader = pypdf.PdfReader(file_path)
        except (IOError, pypdf.errors.PyPdfError) as e:
            raise ImporterError(f'Failed to open PDF file {file_path}') from e

        course_name: None | str = None
        student_numbers: list[str] = []
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text(extraction_mode='layout')

            if page_num == 0:
                course_match = self.__course_name_regex.search(page_text)
                if course_match is not None:
                    course_name = course_match.group(1)

            student_numbers += self.__student_number_regex.findall(page_text)

        if course_name is None:
            raise ImporterError(f'Course name not found in {file_path}')

        self.__store_course(course_name, student_numbers)

    def __is_pdf_file(self, path: str) -> bool:
        return path.endswith('.pdf') and os.path.isfile(path)

    def __store_course(self, course_name: str, student_numbers: list[str]) -> None:
        course = Course(course_name)

        if course.id in self.__courses:
            raise ImporterError(f'Course {course_name} imported more than once')
        else:
            self.__courses[course_name] = course

        for student_number in student_numbers:
            student = self.__students.get(student_number)

            if student is None:
                student = Student(student_number)
                self.__students[student_number] = student

            try:
                student.add_course(course)
            except StudentError as e:
                raise ImportError(
                    'Course added to student more than once. Please report this as a bug. Make sure'
                    'to include the PDF files you were trying to import.'
                ) from e

            try:
                course.add_student(student)
            except CourseError as e:
                raise ImportError(
                    f'PDF file for {course_name} included student {student_number} more than once'
                ) from e
