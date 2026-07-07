from dataclasses import dataclass
from typing import Self

import yaml

from docx_tools.base_classes.yaml_data import YamlDataMapper


@dataclass
class Revision(YamlDataMapper):
    """A revision object containing the revision number, date, and description."""
    number: str
    date: str
    description: str

    @classmethod
    def from_dict(cls, revision_dict: dict[str, str]) -> Self:
        """Mapper for converting a dictionary to a Revision object.
        :param revision_dict: A dictionary containing the revision number, date, and description.
        :returns A revision object.
        """
        return cls(
            number=revision_dict["number"],
            date=revision_dict["date"],
            description=revision_dict["description"]
        )


    def to_yaml(self) -> str:
        """Returns a string of Yaml"""

        return yaml.safe_dump(self.__dict__, sort_keys=False)