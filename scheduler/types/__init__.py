'''
The main datatypes in the scheduler are the following:

* :class:`~student.Student`   - A student enrolled in the university.
* :class:`~course.Course`     - A course students can be enrolled in.
* :class:`~shift.Shift`       - A subdivision of a course to allow for more enrolled students.
* :class:`~timeslot.Timeslot` - The space and time location of a shift.
* :class:`~room.Room`         - A room in campus.

The scheduler's data types follow the aggregation relations described below:

.. code-block::

    +---------+         +--------+         +-------+         +----------+         +------+
    | Student |<>------>| Course |<>------>| Shift |<>------>| Timeslot |<>------>| Room |
    +---------+     1.* +--------+     1.* +-------+     1.* +----------+       1 +------+


* A student is enrolled in one or more courses.
* A course is composed of one or more shifts. Usually there are many shifts of the same type.
* A shift can be lectured in one or more timeslots. Usually, it is just one, but a long shift may,
  for example, be broken into classes across multiple days.
* The spatial location of a timeslot is a room.

Aggregation is used to to achieve better performance and to make the API easier to use. However,
some care is necessary. For example, the following will not work:

>>> course = Course('Computer Graphics')
>>> course.shifts['PL1'] = Shift(ShiftType.PL, 1)
>>> course.shifts
{}

You should work the appropriate methods in the classes instead:

>>> course = Course('Computer Graphics')
>>> course.add_shift(Shift(ShiftType.PL, 1))
>>> course.shifts
{'PL1': Shift(shift_type=ShiftType.PL, number=1, timeslots=[])}
'''

import sys

from .course import Course, CourseError
from .problem import SchedulingProblem
from .room import Room, RoomError
from .shift import Shift, ShiftError, ShiftType
from .student import Student, StudentError
from .timeslot import Timeslot, TimeslotError
from .weekday import Weekday

if 'sphinx' not in sys.modules:
    __all__ = [
        'Course',
        'CourseError',
        'SchedulingProblem',
        'Room',
        'RoomError',
        'Shift',
        'ShiftError',
        'ShiftType',
        'Student',
        'StudentError',
        'Timeslot',
        'TimeslotError',
        'Weekday'
    ]
