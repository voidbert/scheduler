import copy
import datetime
import re
import typing

import requests

from .errors import ImporterError
from ..types import Course, Shift, ShiftError, Room, Timeslot, Weekday

DEFAULT_CALENDARIUM_URL = \
    'https://raw.githubusercontent.com/cesium/calendarium/refs/heads/master/data/shifts.json'

class CalendariumImporter:
    def __init__(self, url: str = DEFAULT_CALENDARIUM_URL) -> None:
        self.__courses: dict[str, Course] = {}
        self.__shifts: dict[str, Shift] = {}
        self.__rooms: dict[str, Room] = {}

        try:
            response = requests.get(url, timeout=None)
            response.raise_for_status()
            json_data = response.json()
        except requests.RequestException as e:
            raise ImporterError('Failed to obtain data from Calendarium') from e

        self.__parse_json(json_data)

    @property
    def courses(self) -> dict[str, Course]:
        return copy.copy(self.__courses)

    @property
    def shifts(self) -> dict[str, Shift]:
        return copy.copy(self.__shifts)

    @property
    def rooms(self) -> dict[str, Room]:
        return copy.copy(self.__rooms)

    def __parse_json(self, json_data: typing.Any) -> None:
        if not isinstance(json_data, list):
            raise ImporterError('Expecting a list in Calendarium\'s data')

        for shift in json_data:
            self.__parse_shift(shift)

    def __parse_shift(self, shift_json: typing.Any) -> None:
        if not isinstance(shift_json, dict):
            raise ImporterError('Expecting a dict in Calendarium\'s data')

        elif not ({'title', 'shift', 'day', 'start', 'end', 'building', 'room'} <= set(shift_json)):
            raise ImporterError('Missing keys in one of Calendarium\'s shift')

        elif not isinstance(shift_json['shift'], str):
            # NOTE: the type of the remaining keys are validated in helper methods
            raise ImporterError('Expecting a str for shift in Calendarium\'s data')

        course = self.__get_course_from_shift(shift_json)
        room = self.__get_room_from_shift(shift_json)
        timeslot = self.__get_timeslot_from_shift(shift_json)

        try:
            shift_type, number = Shift.parse_name(shift_json['shift'])
            shift = Shift(course, shift_type, number, [timeslot], room)
        except ShiftError as e:
            raise ImporterError('Invalid shift information in Calendarium\'s data') from e

        if shift.id in self.__shifts:
            print(shift.id)
            raise ImporterError('Same shift appears more than once in Calendarium\'s data')
        else:
            self.__shifts[shift.id] = shift

    def __get_course_from_shift(self, shift_json: dict[typing.Any, typing.Any]) -> Course:
        if not isinstance(shift_json['title'], str):
            raise ImporterError('Expecting a str for title in Calendarium\'s data')

        course = Course(shift_json['title'])
        if course.id in self.__courses:
            course = self.__courses[course.id]
        else:
            self.__courses[course.id] = course

        return course

    def __get_room_from_shift(self, shift_json: dict[typing.Any, typing.Any]) -> Room:
        if not isinstance(shift_json['building'], str):
            raise ImporterError('Expecting a str for building in Calendarium\'s data')

        elif not isinstance(shift_json['room'], str):
            raise ImporterError('Expecting a str for room in Calendarium\'s data')

        room = Room(shift_json['building'], shift_json['room'])
        if room.id in self.__rooms:
            room = self.__rooms[room.id]
        else:
            self.__rooms[room.id] = room

        return room

    def __get_timeslot_from_shift(self, shift_json: dict[typing.Any, typing.Any]) -> Timeslot:
        day = self.__parse_day(shift_json['day'])
        start = self.__parse_hour('start', shift_json['start'])
        end = self.__parse_hour('end', shift_json['end'])
        return Timeslot(day, start, end)

    def __parse_day(self, value: typing.Any) -> Weekday:
        if not isinstance(value, int):
            raise ImporterError('Expecting a str for day in Calendarium\'s data')

        if value >= 0 and value <= 4:
            # TODO - fix mypy
            return list(Weekday)[value]
        else:
            raise ImporterError('Value of day in Calendarium\'s JSON data must be between 0 and 4')

    def __parse_hour(self, key: str, value: typing.Any) -> datetime.time:
        if not isinstance(value, str):
            raise ImporterError(f'Expecting a str for {key} in Calendarium\'s data')

        match = re.match(r'([0-9]{2}):([0-9]{2})', value)
        if match is None:
            raise ImporterError(f'Invalid hour in Calendarium\'s data: {value}')
        else:
            hour = int(match.group(1))
            minutes = int(match.group(2))
            return datetime.time(hour, minutes)
