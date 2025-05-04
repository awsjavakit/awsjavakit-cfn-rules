from typing import Iterable, TypeVar

T = TypeVar('T')

def flatmap(func, iterable:Iterable[T]):
    nested_results = map(lambda x: func(x),iterable)
    return [item for nested in nested_results for item in nested]

