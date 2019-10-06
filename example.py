from strategery import fed_by
import strategery
import sys


@fed_by('ParamListOfNumbers')
def Minimum(numbers):
    ''' The least '''
    return min(numbers)


@fed_by('ParamListOfNumbers')
def Mean(numbers):
    ''' AKA Average '''
    return 1.0 * sum(numbers) / len(numbers)


@fed_by(Minimum)
def AbsoluteValueMinimum(minimum):
    ''' A highly contrived task for example purposes '''
    return abs(minimum)


# Enable verbose logging:
strategery.engine.logger = sys.stdout

# Provide a list of numbers, get AbsoluteValueMinimum, let strategery figure out the rest.
mean, absolute_value_minimum = strategery.execute(
        targets=[
            Mean,
            AbsoluteValueMinimum
        ],
        preprocessed={
            'ParamListOfNumbers': [-1, -2, -3, -4, -5]
        }
    )

# Disable verbose logging:
strategery.engine.logger = strategery.logging.BypassLogger()

print("")
print('Input: [-1, -2, -3, -4, -5]')
print(f'Mean: {mean}')
print(f'AbsoluteValueMinimum: {absolute_value_minimum}')
