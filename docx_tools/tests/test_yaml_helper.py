from pathlib import Path

import pytest
import yaml

from docx_tools.models.revision import Revision
from docx_tools.yaml_helper import YamlHelper
from fakers.test_faker import TestFaker


@pytest.fixture
def revision_yaml_file(test_faker_fixture: TestFaker,
                       tmp_path: Path):

    revisions = test_faker_fixture.generate_revisions(3)

    data = {
        "revisions": {
            f"rev_{revision.number}": revision.__dict__
            for revision in revisions
        }
    }

    yaml_data = yaml.safe_dump(data, sort_keys=False)
    file_path = tmp_path / "test.yaml"
    file_path.write_text(yaml_data)

    return data, file_path

class TestYamlHelper:
    def test_read_yaml_reads_file_when_exists(self,
                                              revision_yaml_file: tuple[dict, Path]):

        data, file_path = revision_yaml_file


        properties = YamlHelper.read_yaml(file_path.as_posix())

        assert properties == data

    def test_read_yaml_raises_file_not_found_error_when_file_does_not_exist(self, tmp_path: Path):
        non_existent_file = tmp_path / "non_existent.yaml"

        with pytest.raises(FileNotFoundError):
            YamlHelper.read_yaml(non_existent_file.as_posix())

    def test_read_yaml_raises_yaml_error_when_file_contains_invalid_yaml(self, tmp_path: Path):
        file_path = tmp_path / "invalid.yaml"
        file_path.write_text("invalid: yaml: content: [unclosed")

        with pytest.raises(yaml.YAMLError):
            YamlHelper.read_yaml(file_path.as_posix())

    def test_read_yaml_returns_none_when_file_is_empty(self, tmp_path: Path):
        file_path = tmp_path / "empty.yaml"
        file_path.write_text("")

        result = YamlHelper.read_yaml(file_path.as_posix())

        assert result is None

    def test_read_yaml_handles_various_data_types(self, tmp_path: Path):
        data = {
            "string_value": "test string",
            "integer_value": 42,
            "float_value": 3.14,
            "boolean_value": True,
            "list_value": [1, 2, 3],
            "nested_dict": {
                "inner_key": "inner_value",
                "inner_list": ["a", "b", "c"]
            }
        }

        yaml_data = yaml.safe_dump(data, sort_keys=False)
        file_path = tmp_path / "various_types.yaml"
        file_path.write_text(yaml_data)

        result = YamlHelper.read_yaml(file_path.as_posix())

        assert result == data
        assert isinstance(result["string_value"], str)
        assert isinstance(result["integer_value"], int)
        assert isinstance(result["float_value"], float)
        assert isinstance(result["boolean_value"], bool)
        assert isinstance(result["list_value"], list)
        assert isinstance(result["nested_dict"], dict)

    def test_read_yaml_handles_null_values(self, tmp_path: Path):
        data = {
            "null_value": None,
            "another_key": "not null"
        }

        yaml_data = yaml.safe_dump(data, sort_keys=False)
        file_path = tmp_path / "null_values.yaml"
        file_path.write_text(yaml_data)

        result = YamlHelper.read_yaml(file_path.as_posix())

        assert result == data
        assert result["null_value"] is None

    def test_read_yaml_handles_special_characters(self, tmp_path: Path):
        data = {
            "special_chars": "String with special: chars & symbols @#$%",
            "unicode": "Unicode: 你好世界 🚀",
            "multiline": "Line 1\nLine 2\nLine 3"
        }

        yaml_data = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
        file_path = tmp_path / "special_chars.yaml"
        file_path.write_text(yaml_data, encoding="utf-8")

        result = YamlHelper.read_yaml(file_path.as_posix())

        assert result == data

    def test_read_yaml_properties_by_key_returns_values(self,
                                                        revision_yaml_file: tuple[dict, Path]):
        data, file_path = revision_yaml_file
        result = YamlHelper.read_yaml_properties_by_key(file_path.as_posix(), "revisions")
        assert result == data.get("revisions")

    def test_to_class_converts_yaml_to_class_list(self, revision_yaml_file: tuple[dict, Path]):
        data, file_path = revision_yaml_file

        rev_count = len([key for key in data["revisions"].keys() if key.startswith("rev_")])
        result = YamlHelper.yaml_to_class_list(file_path.as_posix(),
                                     "revisions",
                                     Revision)
        
        assert len(result) == rev_count