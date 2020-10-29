from __future__ import absolute_import

from typing import Any, Dict, Union

from pydantic import BaseModel

DictIntStrAny = Dict[Union[int, str], Any]


class Base(BaseModel):
    class Config:
        table = ""
        use_enum_values = True
        anystr_strip_whitespace = True
        validate_all = True
        validate_assignment = True
        extra = "forbid"
        arbitrary_types_allowed = True

    def __init__(self, **payload) -> None:
        self.__pre_init__(payload)
        super().__init__(**payload)
        self.__post_init__()
        self.validation_rules()

    def __pre_init__(self, args: DictIntStrAny) -> None:
        """
        Do something with the args
        """

    def __post_init__(self) -> None:
        """
        Do something with the object, change values if needed
        """

    def validation_rules(self) -> None:
        """
        Here you will write validation rules, do not set values here!, use pre or post init for that
        This function will be triggered after init and every time you change the object
        """

    def __setattr__(self, name: str, value: Any) -> None:
        """
        validates a certain attribute by name and value
        NEVER set a value in here! only use this for validation, error checking, assertions
        BE carefull about recursion
        """
        super().__setattr__(name, value)
        self.validation_rules()

    @classmethod
    def from_db(cls, row) -> 'Base':
        row = dict(row)
        return cls(**row)

    def to_db(self) -> DictIntStrAny:
        to_dict = self.dict()
        return to_dict
