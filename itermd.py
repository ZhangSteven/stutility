"""
The module aims to provide iterator related functions.
"""

__all__ = ('firstof', 'firstn', 'skipn', 'allequal', 'num_elements')


def firstof(func, L):
    """
    Return the first element in L that makes the function 'func' evaluating
    to True.
    """
    try:
        return next(filter(func, L))
    except StopIteration:
        raise ValueError('no element satisfies func') from None


def firstn(n, L):
    """
    Return the first n elements of L, n >= 0. When L has less than n
    elements, all elements in L are returned.
    """
    if isinstance(n, int) and n > -1:
        for idx, el in enumerate(L):
            if idx < n:
                yield el
            else:
                break
    
    else:
        raise ValueError(f'invalid argument: n={n}')


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
        raise ValueError(f'invalid argument: n={n}')


def allequal(L):
    """
    Test whether all elements in Iterable L are equal.

    Returns True if L has zero or only one element.
    """
    iterator = iter(L)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    else:
        return all(first==x for x in iterator)


def num_elements(L):
    """
    Return the total number of elements in iterable L.
    """
    return sum(1 for el in L)