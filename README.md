# Strategery

## Installation
```bash
pip install strategery
```

## About
The Feature Engine is an approach to structuring code, inspired by the spaghetti-ass feature extraction tasks I've done for machine learning. I'm no expert in design patterns, but I think it's somewhere between [chain-of-responsibility](https://en.wikipedia.org/wiki/Chain-of-responsibility_pattern) and [strategy](https://en.wikipedia.org/wiki/Strategy_pattern).

The concept is that you're trying to build a feature vector, and in the process, you have all these functions you want to apply to a common source of information. You find yourself using the same algorithms in a bunch of scripts, but sometimes just some of them, and sometimes in a different order, and sometimes you want to discard interstitial data. Sometimes you perform an expensive calculation in the middle, but you want to share that result between other functions.

For a toy example, let's say the features you're extracting are a Minimum, Mean, and AbsoluteValueMinimum.

```python
from strategery import fed_by

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
```

Hold up, `@fed_by()`?

OK, so `@fed_by()` is a decorator that will mark up your tasks so it can tell the engine what its own dependencies are. Then the engine can calculate a strategery for how to get to the results you requested, and if you provided all the necessary components, it resolve all the dependencies and hand off values between your functions. `@fed_by` accepts a reference to a function (if you need the results from another task), or a string (if you want to provide the input as a parameter).

All right, that's it for setup. Let's crunch some numbers. When you're calling `strategery.execute`, the `targets` parameter is a list of the results you want, and the `preprocessed` parameter lets you provide information for the engine to start with.

```python
import strategery
import sys

# Enable verbose logging:
strategery.engine.logger = sys.stderr

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

```