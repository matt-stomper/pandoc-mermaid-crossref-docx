from typing import Any
from docx import Document
from docxcompose.composer import Composer
from docxcompose.properties import CustomProperties
import click
import os
import yaml


@click.command()
@click.option('-y', help='yaml files containing custom properties', required=True)
@click.option('-i', help='Input Docx file', required=True)
@click.option('-t', help='Title page docx file')
@click.option('-o', help='Output Docx file')
def combine_properties_document(y, i, t, o):
    if not os.path.exists(i):
        print('Input Docx file does not exist')
        exit()

    if not os.path.exists(y):
        print('Yaml properties file does not exist')
        exit()

    properties = read_properties_from_yaml(y)
    title_doc = inject_properties_into_document(t, properties)
    composer = Composer(title_doc)
    doc = inject_properties_into_document(i, properties)
    composer.append(doc)

    composer.save(o)


def read_properties_from_yaml(file_path) -> Any:
    with open(file_path, 'r') as f:
        properties = yaml.safe_load(f)
        return properties


def inject_properties_into_document(document_path: str, properties: Any) -> Document:
    doc = Document(document_path)
    custom_properties = CustomProperties(doc)

    for key, value in properties.items():
        if custom_properties.get(key) is not None:
            custom_properties[key] = value

            # Assert that the custom property has been set
            assert custom_properties.get(key) == value
        else:
            custom_properties.add(key, value)

        return doc


if __name__ == '__main__':
    combine_properties_document()