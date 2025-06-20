from scheduler.types.ellipsis import EllipsisRepr

def test_repr() -> None:
    assert repr(EllipsisRepr()) == '...'

def test_str() -> None:
    assert str(EllipsisRepr()) == '...'
