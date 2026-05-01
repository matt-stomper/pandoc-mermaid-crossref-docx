from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from docx_tools.inject_properties import (
    _inject_properties,
    _validate_input_files,
    combine_properties_document,
    read_properties_from_yaml,
)


def test_read_properties_from_yaml_returns_safe_loaded_yaml():
    yaml_content = """
title: Example Document
version: 1
published: true
"""

    with patch("builtins.open", mock_open(read_data=yaml_content)) as mocked_open:
        result = read_properties_from_yaml("properties.yaml")

    mocked_open.assert_called_once_with("properties.yaml", "r")
    assert result == {
        "title": "Example Document",
        "version": 1,
        "published": True,
    }


def test_validate_input_files_returns_true_when_file_exists(tmp_path):
    existing_file = tmp_path / "example.docx"
    existing_file.write_text("content")

    assert _validate_input_files(existing_file) is True


def test_validate_input_files_raises_when_required_file_does_not_exist(tmp_path):
    missing_file = tmp_path / "missing.docx"

    with pytest.raises(FileNotFoundError, match=f"File {missing_file} does not exist"):
        _validate_input_files(missing_file, required=True)


def test_validate_input_files_returns_false_when_optional_file_does_not_exist(tmp_path):
    missing_file = tmp_path / "optional.yaml"

    assert _validate_input_files(missing_file, required=False) is False


@patch("docx_tools.inject_properties.CustomProperties")
@patch("docx_tools.inject_properties.Document")
def test_inject_properties_adds_missing_custom_properties(mock_document, mock_custom_properties):
    document = MagicMock()
    custom_properties = MagicMock()
    properties = {
        "Title": "Example Document",
        "Version": 1,
    }

    mock_document.return_value = document
    mock_custom_properties.return_value = custom_properties
    custom_properties.get.return_value = None

    result = _inject_properties("input.docx", properties)

    mock_document.assert_called_once_with("input.docx")
    mock_custom_properties.assert_called_once_with(document)
    custom_properties.add.assert_any_call("Title", "Example Document")
    custom_properties.add.assert_any_call("Version", 1)
    assert custom_properties.add.call_count == 2
    assert custom_properties.update_all.call_count == 2
    assert result is document


@patch("docx_tools.inject_properties.CustomProperties")
@patch("docx_tools.inject_properties.Document")
def test_inject_properties_updates_existing_custom_properties(mock_document, mock_custom_properties):
    document = MagicMock()
    custom_properties = MagicMock()
    properties = {
        "Title": "Updated Title",
    }

    mock_document.return_value = document
    mock_custom_properties.return_value = custom_properties
    custom_properties.get.side_effect = ["Existing Title", "Updated Title"]

    result = _inject_properties("input.docx", properties)

    custom_properties.__setitem__.assert_called_once_with("Title", "Updated Title")
    custom_properties.add.assert_not_called()
    custom_properties.update_all.assert_called_once()
    assert result is document


@patch("docx_tools.inject_properties.Composer")
@patch("docx_tools.inject_properties._inject_properties")
@patch("docx_tools.inject_properties.read_properties_from_yaml")
@patch("docx_tools.inject_properties._validate_input_files")
def test_combine_properties_document_injects_appends_and_saves(
    mock_validate_input_files,
    mock_read_properties_from_yaml,
    mock_inject_properties,
    mock_composer,
):
    properties = {
        "Title": "Example Document",
    }
    title_document = MagicMock()
    input_document = MagicMock()
    composer = MagicMock()

    mock_validate_input_files.return_value = True
    mock_read_properties_from_yaml.return_value = properties
    mock_inject_properties.side_effect = [title_document, input_document]
    mock_composer.return_value = composer

    combine_properties_document.callback(
        y="properties.yaml",
        i="input.docx",
        t="title.docx",
        o="output.docx",
    )

    mock_validate_input_files.assert_any_call(Path("input.docx"), required=True)
    mock_validate_input_files.assert_any_call(Path("properties.yaml"), required=False)
    mock_validate_input_files.assert_any_call(Path("title.docx"), required=False)

    mock_read_properties_from_yaml.assert_called_once_with("properties.yaml")
    mock_inject_properties.assert_any_call(document_path="title.docx", properties=properties)
    mock_inject_properties.assert_any_call("input.docx", properties)

    mock_composer.assert_called_once_with(title_document)
    composer.append.assert_called_once_with(input_document, remove_property_fields=False)
    composer.save.assert_called_once_with("output.docx")


@patch("docx_tools.inject_properties.exit")
@patch("docx_tools.inject_properties._validate_input_files")
def test_combine_properties_document_exits_when_optional_yaml_is_missing(
    mock_validate_input_files,
    mock_exit,
):
    mock_validate_input_files.side_effect = [True, False, True]
    mock_exit.side_effect = SystemExit

    with pytest.raises(SystemExit):
        combine_properties_document.callback(
            y="missing.yaml",
            i="input.docx",
            t="title.docx",
            o="output.docx",
        )

    mock_exit.assert_called_once()