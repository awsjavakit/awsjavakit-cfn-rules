from attrs import define


@define(repr=False, str=False)
class RuleId:
    rule_id: str

    def __str__(self) -> str:
        return self.rule_id

    def __repr__(self) -> str:
        return self.__str__()