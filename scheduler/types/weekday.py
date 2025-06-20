import enum

@enum.unique
class Weekday(enum.Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5

    def __repr__(self) -> str:
        return str(self)[len('Weekday') + 1:].capitalize()
