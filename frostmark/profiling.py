'''
Debug module for finding bottlenecks in the Python functions.
'''

from typing import Callable
from cProfile import Profile
from io import StringIO
from pstats import Stats
from os.path import sep

from ensure import ensure_annotations
from frostmark import __name__ as package


@ensure_annotations
def profile(func: Callable) -> Callable:
    '''
    Profiling decorator that prints to STDOUT.

    Disable with ``python -O file.py``.
    '''

    if not __debug__:
        # just wrap the function for ordinary call
        # in case debug is turned off
        def new_func(*args, **kwargs):
            return func(*args, **kwargs)
    else:
        def new_func(*args, **kwargs):
            # create a Profile and enable tracking
            prof = Profile()
            prof.enable()

            # call the profiled function
            result = func(*args, **kwargs)

            # disable tracking
            prof.disable()

            # simulate writing to file via string buffer
            buff = StringIO()

            # write stats to string buffer
            prof_stats = Stats(prof, stream=buff)
            prof_stats.print_stats()

            # print the output from string buffer
            print('-' * 79)
            path = func.__code__.co_filename.split(sep)
            path = path[len(path) - list(reversed(path)).index(package) - 1:]
            print(
                f'{".".join(path)} :: '
                f'{func.__name__}'
            )
            print(buff.getvalue())

            # propagate back the real func's output
            return result

    # return wrapped function
    return new_func
