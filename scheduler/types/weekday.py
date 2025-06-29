import enum

@enum.unique
class Weekday(enum.StrEnum):
    '''A day of the week in which there can be classes (Saturday and Sunday are excluded).'''

    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'

    def __repr__(self) -> str:
        return f'Weekday.{self.upper()}'
