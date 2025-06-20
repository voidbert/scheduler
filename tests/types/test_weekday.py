from scheduler.types.weekday import Weekday

def test_repr():
    assert repr(Weekday.WEDNESDAY) == 'Wednesday'

def test_str():
    assert str(Weekday.MONDAY) == 'Weekday.MONDAY'
