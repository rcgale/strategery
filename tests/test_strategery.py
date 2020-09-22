import strategery
from strategery import fed_by
from strategery.features import StrategeryFeature


def test_function_usage():
    @fed_by('Integer')
    def integer_plus_one(integer):
        return integer + 1

    expected = 1
    actual, = strategery.execute(targets=[integer_plus_one], input={'Integer': 0})
    assert actual == expected


def test_class_usage():
    class IntegerPlusOne(StrategeryFeature):
        @fed_by('Integer')
        def __call__(self, integer):
            return integer + 1

    expected = 1
    actual, = strategery.execute(targets=[IntegerPlusOne()], input={'Integer': 0})
    assert actual == expected


def test_series_of_class_usage():
    class IntegerPlusOne(StrategeryFeature):
        @fed_by('Integer')
        def __call__(self, integer):
            return integer + 1

    class IntegerPlusTwo(StrategeryFeature):
        @fed_by(IntegerPlusOne())
        def __call__(self, integer):
            return integer + 2

    expected = 3
    actual, = strategery.execute(targets=[IntegerPlusTwo()], input={'Integer': 0})
    assert actual == expected


def test_class_usage_with_constructor_and_mulitple_instances():
    class IntegerPlus(StrategeryFeature):
        def __init__(self, operand):
            super().__init__(unique_key=(operand,))
            self.operand = operand

        @fed_by('Integer')
        def __call__(self, integer):
            return integer + self.operand


    actual1, actual2 = strategery.execute(targets=[IntegerPlus(1), IntegerPlus(2)], input={'Integer': 0})
    assert actual1 == 1
    assert actual2 == 2


def test_class_usage_unambiguous():
    class IntegerPlus1(StrategeryFeature):
        @fed_by('Integer')
        def __call__(self, integer):
            return integer + 1

    class IntegerPlus2(StrategeryFeature):
        @fed_by(IntegerPlus1())
        def __call__(self, integer):
            return integer + 2

    actual, = strategery.execute(targets=[IntegerPlus2()], input={'Integer': 0})
    assert actual == 3


def test_series_of_dependencies():
    @fed_by('Integer')
    def func_one(integer):
        return integer

    @fed_by(func_one)
    def func_two(same_integer):
        return same_integer

    actual, = strategery.execute(targets=[func_two], input={'Integer': 0})
    assert actual == 0
