from pathlib import Path

import click
import yaml

from docx import Document
from docx.document import Document as DocumentObject
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docxcompose.composer import Composer
from docxcompose.properties import CustomProperties
from typing import Any

from docx_tools.revision_table import update_docx_revisions_table
from docx_tools.yaml_helper import YamlHelper


@click.group()
def cli():
    """A CLI tool for working with docx files and custom properties."""
    pass

@cli.command()
@click.option('-y', type=click.Path(exists=True), help='yaml files containing custom properties', required=True)
@click.option('-k', help='Key containing the custom properties', required=False)
@click.option('-i', type=click.Path(exists=True), help='Input Docx file', required=True)
@click.option('-o', help='Output Docx file', required=True)
@click.option('-t', type=click.Path(exists=True), help='Template or title page docx file')
@click.option('-r', help='Revisions table key in the custom properties', required=False)
@click.option('-u', help='Force updates in the word document', is_flag=True, default=True)
def combine_properties_document(y, k, i, t, o, r, u):
    """
    This function takes a title page and a docx file and adds in custom properties to both documents
    before appending the input docx into the title page docx.
    :param y: Yaml file containing custom properties
    :param i: Docx input containing the main content of the document
    :param t: Docx title page
    :param o: Save location of final document
    :param r: Revisions table key in the custom properties
    :param u: Trigger updates in the word document
    :return: None
    """
    input_docx = Path(i)
    title_docx = Path(t)
    custom_properties = Path(y)
    update_fields = bool(u)

    if not _validate_input_files(input_docx, required=True):
        exit()

    if not _validate_input_files(custom_properties, required=True):
        exit()

    properties = read_properties_from_yaml(y, k)
    doc: DocumentObject = _inject_properties(i, properties)

    if t:
        _validate_input_files(title_docx, required=True)
        title_doc: DocumentObject = _inject_properties(document_path=t, properties=properties)
        if update_fields:
            _mark_fields_for_update_on_open(title_doc)
        composer: Composer = Composer(title_doc)
        composer.append(doc, remove_property_fields=False)
    else:
        composer: Composer = Composer(input_docx)

    composer.save(o)

    if r:
        revisions_table = YamlHelper.read_yaml_properties_by_key(y, r)
        print(revisions_table)
        if isinstance(revisions_table, dict):

            update_docx_revisions_table(
                input_docx=o,
                output_docx=o,
                revisions_metadata=revisions_table,
            )


def _mark_fields_for_update_on_open(doc: DocumentObject) -> None:
    """
    Request Word to update all document fields when the file is opened.

    This includes fields used by tables of contents, tables of figures,
    cross-references, page numbers, and similar Word-generated content.
    """
    settings = doc.settings.element
    update_fields = settings.find(qn('w:updateFields'))

    if update_fields is None:
        update_fields = OxmlElement('w:updateFields')
        settings.append(update_fields)

    update_fields.set(qn('w:val'), 'true')


def read_properties_from_yaml(file_path, custom_property_key: str | None = None) -> Any:
    """
    This function takes a yaml file and returns a list of custom properties
    :param file_path: path to yaml file containing custom properties
    :param custom_property_key: key in yaml file containing the properties
    :return: Any object returned from safe_load, but generally a dict of key|value pairs
    """

    if custom_property_key is None:
        print("No custom property key provided.")
        return YamlHelper.read_yaml(file_path=file_path)

    return YamlHelper.read_yaml_properties_by_key(file_path=file_path,
                                                  custom_property_key=custom_property_key)

def _inject_properties(document_path: str, properties: Any) -> DocumentObject:
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