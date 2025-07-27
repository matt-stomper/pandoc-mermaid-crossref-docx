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
    """
    This function takes a title page and a docx file and adds in custom properties to both documents
    before appending the input docx into the title page docx.
    :param y: Yaml file containing custom properties
    :param i: Docx input containing the main content of the document
    :param t: Docx title page
    :param o: Save location of final document
    :return: None
    """
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
    """
    This function takes a yaml file and returns back a list of custom properties
    :param file_path: path to yaml file containing custom properties
    :return: Any object returned from safe_load
    """
    with open(file_path, 'r') as f:
        properties = yaml.safe_load(f)
        return properties


def inject_properties_into_document(document_path: str, properties: Any) -> Document:
    """
    This function injects custom properties into a docx using docxcompose
    :param document_path: path to docx
    :param properties: List of custom properties
    :return: docxcompose document with injected custom properties
    """
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