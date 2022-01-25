import pytest

from calculator import Calculator


def wont_run_as_a_test():
    assert False

def test_add():
    calc = Calculator()
    assert calc.add(12, 14) == 26
    assert calc.add(-3, 3) == 0

def test_divide():
    calc = Calculator()
    assert calc.divide(3, 5) == 3/5
    with pytest.raises(ZeroDivisionError):
        calc.divide(12, 0)

class TestSubtract:
    calc = Calculator()

    def test_one(self):
        assert 2 == self.calc.subtract(22, 20)

    def test_two(self):
        assert 10 == self.calc.subtract(20, 10)

    def not_a_test(self):
        assert False
