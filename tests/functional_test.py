from __future__ import annotations

from collections.abc import Iterable
from typing import List

from assertpy import assert_that
from hamcrest import equal_to

from awsjavakit_cfn_rules.utils.functional import flatmap


def should_return_flattened_result():
    input = [1,2,3,4]
    nested_results:List[List[int]] = list(map(lambda input: create_nested(input),input))
    flattened_results: Iterable[int] = list(flatmap(lambda input:create_nested(input),input))
    assert_that(nested_results, equal_to([[0],[0,1],[0,1,2],[0,1,2,3]]))
    assert_that(flattened_results, equal_to([0, 0, 1, 0, 1, 2, 0, 1, 2, 3]))




def create_nested(input:int)->List[int]:
    output: List[int]= []
    for i in range(input):
        output.append(i)
    return output