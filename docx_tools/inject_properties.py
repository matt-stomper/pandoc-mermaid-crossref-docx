from pathlib import Path

import click
import yaml

from docx import Document
from docxcompose.composer import Composer
from docxcompose.properties import CustomProperties
from typing import Any


@click.group()
def cli():
    """A CLI tool for working with docx files and custom properties."""
    pass

@cli.command()
@click.option('-y', help='yaml files containing custom properties', required=True)
@click.option('-i', help='Input Docx file', required=True)
@click.option('-t', help='Title page docx file')
@click.option('-o', help='Output Docx file')
def combine_properties_document(y, i, t, o):
    """
    This function takes a title page and a docx file and adds in custom properties to both documents
    before appending the input docx into the title page docx.
    :param y: Yaml file containing custom properties
    :param i: Docx input containing the main content of the document
    :param t: Docx title page
    :param o: Save location of final document
    :return: None
    """
    input_docx = Path(i)
    title_docx = Path(t)
    output_docx = Path(o)
    custom_properties = Path(y)

    if not _validate_input_files(input_docx, required=True):
        exit()

    if not _validate_input_files(custom_properties, required=False):
        exit()

    if not _validate_input_files(title_docx, required=False):
        exit()

    properties = read_properties_from_yaml(y)
    title_doc = _inject_properties(document_path=t, properties=properties)
    composer = Composer(title_doc)
    doc = _inject_properties(i, properties)
    composer.append(doc, remove_property_fields=False)

    composer.save(o)


def read_properties_from_yaml(file_path) -> Any:
    """
    This function takes a yaml file and returns back a list of custom properties
    :param file_path: path to yaml file containing custom properties
    :return: Any object returned from safe_load
    """
    with open(file_path, 'r') as f:
        properties = yaml.safe_load(f)
        return properties

@cli.command
@click.option('-document-path', help='.docx document needing the custom properties.', required=True)
@click.option('-properties', help='yaml files containing custom properties.', required=True)
def inject_properties_into_document(document_path: str, properties: Any) -> Document:
    """
    This function injects custom properties into a docx using docxcompose
    :param document_path: path to docx
    :param properties: List of custom properties
    :return: docxcompose document with injected custom properties
    """
    return _inject_properties(document_path, properties)

def _inject_properties(document_path: str, properties: Any):
    doc = Document(document_path)
    custom_properties = CustomProperties(doc)

    for key, value in properties.items():
        print(f'Injecting custom properties {key}: {value}')
        if custom_properties.get(key) is not None:
            custom_properties[key] = value

            # Assert that the custom property has been set
            assert custom_properties.get(key) == value
        else:
            custom_properties.add(key, value)

        custom_properties.update_all()
    return doc

def _validate_input_files(path: Path, required: bool = True) -> bool:
    if not path.exists():
        if required:
            raise FileNotFoundError(f'File {path} does not exist')
        else:
            return False
    return True


if __name__ == '__main__':
    try:
        cli()
    except FileNotFoundError as e:
        print(e)