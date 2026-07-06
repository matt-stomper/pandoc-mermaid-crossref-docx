# docx_tools

`docx_tools` is a small Python CLI utility for working with Microsoft Word `.docx` files and custom document properties.

It can:

- Read custom properties from a YAML file.
- Inject those properties into a `.docx` document.
- Update existing custom properties when they already exist.
- Add missing custom properties when they do not exist.
- Update fields that reference custom properties in the document.
- Combine a title page document with a main document after applying the same custom properties to both.

## Features

### Inject custom properties into a DOCX file

The tool opens a `.docx` document, applies custom properties, and updates all property fields in the document.

For each property:

- If the property already exists, its value is updated.
- If the property does not exist, it is added.
- The document fields are refreshed using the updated custom properties.

### Combine a title page and document

The `combine-properties-document` command applies custom properties to both:

1. A title page `.docx`
2. A main input `.docx`

It then appends the main document to the title page and saves the combined result.

This is useful when generating Word documents that use custom properties in headers, footers, title pages, or document metadata fields.

## Requirements

This package uses:

- `click` for the command-line interface
- `pyyaml` for reading YAML files
- `python-docx` for opening Word documents
- `docxcompose` for custom properties and document composition

## YAML properties file

Custom properties should be provided as a YAML mapping.

Example:

```yaml
DocumentTitle: System Design Document 
DocumentNumber: SDD-001 
Revision: A 
Author: Jane Smith 
ProjectName: Example Project
```

```bash 
python src/docx_tools/inject_properties.py combine-properties-document
-y properties.yaml
-i input.docx
-t title-page.docx
-o output.docx
```