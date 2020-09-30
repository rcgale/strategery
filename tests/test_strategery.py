from typing import NamedTuple

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
        @staticmethod
        @fed_by('IntegerParameter')
        def compute(integer):
            return integer + 1

    expected = 1
    actual, = strategery.execute(targets=[IntegerPlusOne], input={'IntegerParameter': 0})
    assert actual == expected


def test_series_of_class_usage():
    class IntegerPlusOne(StrategeryFeature):
        def __init__(self, value):
            self.value = value

        @staticmethod
        @fed_by('IntegerParameter')
        def compute(integer: int):
            return IntegerPlusOne(integer + 1)

    class IntegerPlusTwo(StrategeryFeature):
        def __init__(self, value: int):
            self.value = value

        @staticmethod
        @fed_by(IntegerPlusOne)
        def compute(ipo: IntegerPlusOne):
            return IntegerPlusTwo(value=ipo.value + 2)

    expected = 3
    actual, = strategery.execute(targets=[IntegerPlusTwo], input={'IntegerParameter': 0})
    assert actual.value == expected


def test_class_usage_unambiguous():
    class IntegerPlus1(StrategeryFeature):
        @staticmethod
        @fed_by('Integer')
        def compute(integer):
            return integer + 1

    class IntegerPlus2(StrategeryFeature):
        @staticmethod
        @fed_by(IntegerPlus1)
        def compute(integer):
            return integer + 2

    actual, = strategery.execute(targets=[IntegerPlus2], input={'Integer': 0})
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
