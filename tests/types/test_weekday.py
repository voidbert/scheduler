from scheduler.types.weekday import Weekday

def test_repr() -> None:
    assert repr(Weekday.WEDNESDAY) == '<Weekday.WEDNESDAY: \'Wednesday\'>'

def test_str() -> None:
    assert str(Weekday.MONDAY) == 'Monday'
