from abc import ABC
from typing import Self


class YamlDataMapper(ABC):

    @classmethod
    def from_dict(cls, yaml_dict: dict) -> Self:
        """Mapper for converting a dictionary to a YamlData object.
        :param yaml_dict: A dictionary containing the YAML data.
        """
        ...

    def to_yaml(self) -> str:
        """Mapper for converting a YamlData object to a YAML string.
        """
        ...