'''
Classes and Relations
~~~~~~~~~~~~~~~~~~~~~

The main datatypes in the scheduler are the following:

* :class:`~student.Student`   - A student enrolled in the university.
* :class:`~course.Course`     - A course students can be enrolled in.
* :class:`~shift.Shift`       - A subdivision of a course to allow for more enrolled students.
* :class:`~timeslot.Timeslot` - The space and time location of a shift.
* :class:`~room.Room`         - A room in campus.

The scheduler's data types follow the relations described below:

.. code-block::

    +---------+         +--------+         +-------+         +----------+         +------+
    | Student |<>------>| Course |<>------>| Shift |<>------>| Timeslot |<>------>| Room |
    +---------+     1.* +--------+     1.* +-------+     1.* +----------+       1 +------+


* A student is enrolled in one or more courses.
* A course is composed of one or more shifts. Usually there are many shifts of the same type.
* A shift can be lectured in one or more timeslots. Usually, it is just one, but a long shift may,
  for example, be broken into classes across multiple days.
* The spatial location of a timeslot is a room.

.. _encapsulation:

Encapsulation
~~~~~~~~~~~~~

The API of this module was designed to avoid copying objects. Therefore, there are some aspects that
must be considered:

* In constructors of classes that store collections of objects, a new collection will be created,
  but the class will reference the original objects:

>>> slot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), Room('CP1', '0.08'))
>>> slots = [slot]
>>> shift = Shift(ShiftType.PL, 3, slots)
>>> assert shift.timeslots is not slots
>>> assert shift.timeslots[0] is slot

* In methods that add objects to a class instance, just like in the constructor, no copies of the
  objects will be made:

>>> course = Course('Computer Graphics')
>>> shift = Shift(ShiftType.PL, 1)
>>> course.add_shift(shift)
>>> assert course.shifts['PL1'] is shift

* In the getters of properties that are not collections, the reference to the object will be
  returned directly:

>>> room = Room('CP1', '0.08')
>>> slot = Timeslot(Weekday.MONDAY, datetime.time(9, 0), datetime.time(11, 0), room)
>>> assert slot.room is room

* In getters of collections, a constant reference to the collection is returned, using a type such
  as :class:`~collections.abc.Mapping`. The collection will not be able to be modified, but changes
  to it through the parent object will still be observed:

>>> course = Course('Computer Graphics')
>>> shifts = course.shifts
>>> shifts
{}
>>> course.add_shift(Shift(ShiftType.PL, 1))
>>> shifts
{'PL1': Shift(shift_type=ShiftType.PL, number=1, timeslots=[])}

For object storage (the tree of students, courses, shifts, ...), no copies of the objects should be
performed, and references should be used instead. However, for intermediate computation, if
necessary, shallow copies of collections should be performed.
'''

import sys

from .course import Course, CourseError
from .room import Room, RoomError
from .shift import Shift, ShiftError, ShiftType
from .student import Student, StudentError
from .timeslot import Timeslot, TimeslotError
from .weekday import Weekday

if 'sphinx' not in sys.modules: # pragma: no cover
    __all__ = [
        'Course',
        'CourseError',
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
