from typing import Any

import yaml

from docx_tools.base_classes.yaml_data import YamlDataMapper


class YamlHelper:

    @classmethod
    def read_yaml(cls, file_path: str) -> dict[str, str | int | dict[str, Any] | Any]:
        with open(file_path, 'r') as f:
            yaml_properties: Any = yaml.safe_load(f)
            return yaml_properties

    @classmethod
    def read_yaml_properties_by_key(cls, file_path: str, custom_property_key: str) -> str | int | dict[str, Any] | Any:
        """Mapper for reading a specific property from a YAML file.
        :param file_path: The path to the YAML file.
        :param custom_property_key: The key of the property to read.
        :returns The value of the specified property.
        """
        return cls.read_yaml(file_path).get(custom_property_key)

    @staticmethod
    def to_class(expected_class: YamlDataMapper, yaml_properties: dict[str, Any]) -> Any:
        return expected_class.from_dict(yaml_properties)

    @staticmethod
    def yaml_to_class(file_path: str, custom_property_key: str, expected_class: YamlDataMapper) -> Any:
        """Converts provided properties to the expected class."""
        yaml_properties = YamlHelper.read_yaml_properties_by_key(file_path, custom_property_key)

        return YamlHelper.to_class(expected_class, yaml_properties)

    @classmethod
    def yaml_to_class_list(cls, file_path: str, custom_property_key: str, expected_class: type[YamlDataMapper]) -> list[
        Any]:
        """Converts a YAML mapping under a key into a list of class instances.

        Example YAML:

            revisions:
              rev_1:
                number: "1"
                date: "2026-10-01"
                description: "This is a description"
              rev_2:
                number: "2"
                date: "2026-10-01"
                description: "This is a second description"

        Calling:

            YamlHelper.yaml_to_class_list("file.yaml", "revisions", Revision)

        Returns:

            [
                Revision(number="1", date="2026-10-01", description="This is a description"),
                Revision(number="2", date="2026-10-01", description="This is a second description"),
            ]
        """
        yaml_properties = cls.read_yaml_properties_by_key(file_path, custom_property_key)

        return [
            expected_class.from_dict(item_properties)
            for item_properties in yaml_properties.values()
        ]