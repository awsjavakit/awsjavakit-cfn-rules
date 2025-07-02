from __future__ import annotations

from hamcrest import assert_that, equal_to

from awsjavakit_cfn_rules.utils.functional import flatmap


def should_return_flattened_result():
    some_input = [1,2,3,4]
    nested_results:list[list[int]] = list(map(lambda input: create_nested(input),some_input))
    flattened_results: list[int] = list(flatmap(lambda input:create_nested(input),some_input))
    assert_that(nested_results, equal_to([[0],[0,1],[0,1,2],[0,1,2,3]]))
    assert_that(flattened_results, equal_to([0, 0, 1, 0, 1, 2, 0, 1, 2, 3]))


def create_nested(inp:int)->list[int]:
    output: list[int]= []
    for i in range(inp):
        output.append(i)
    return output
