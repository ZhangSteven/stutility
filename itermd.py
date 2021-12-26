"""
The module aims to provide iterator related functions.
"""

from itertools import dropwhile
from functools import partial
from toolz.functoolz import compose


def firstof(func, L):
    """
    Return the first element in L that makes the function 'func' evaluating
    to True.
    """
    return next(el for el in L if func(el))


def skipn(n, L):
    """
    [Int] n (>=0), [Iterable] L => [Iterable] L1

    Whwere L1 is L after skipping the first n elements
    """
    if isinstance(n, int) and n > -1:
        for idx, el in enumerate(L):
            if idx < n:
                continue
            else:
                yield el
    
    else:
        raise ValueError(f'skipn() invalid argument: n={n}')


def num_elements(L):
    """
    Return the total number of elements in iterable L.
    """
    return sum(1 for el in L)