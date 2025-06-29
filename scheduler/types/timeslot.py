from __future__ import annotations
import datetime
import typing

from .weekday import Weekday

class TimeslotError(Exception):
    pass

class Timeslot:
    def __init__(self, day: Weekday, start: datetime.time, end: datetime.time) -> None:
        if end <= start:
            raise TimeslotError(
                f'Timeslot\'s starting time ({start!r}) must precede its ending time ({end!r})'
            )

        self.__day = day
        self.__start = start
        self.__end = end

    def overlaps(self, other: Timeslot) -> bool:
        return self.__day == other.day and self.__start < other.end and other.start < self.__end

    @property
    def day(self) -> Weekday:
        return self.__day

    @property
    def start(self) -> datetime.time:
        return self.__start

    @property
    def end(self) -> datetime.time:
        return self.__end

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, Timeslot):
            return False

        return self.__day == other.day and self.__start == other.start and self.__end == other.end

    def __copy__(self) -> Timeslot:
        return Timeslot(self.__day, self.__start, self.__end)

    def __hash__(self) -> int:
        return hash((self.__day, self.__start, self.__end))

    def __repr__(self) -> str:
        return f'Timeslot(day={self.__day}, start=\'{self.__start}\', end=\'{self.__end}\')'
