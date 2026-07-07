from typing import Any

from docx import Document
from docx.document import Document as DocumentObject
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph


REVISIONS_TABLE_YAML_KEY = "revisions_table"
RESERVED_REVISIONS_TABLE_KEYS = {
    "caption",
    "bookmark",
}


def revision_sort_key(item: tuple[str, Any]) -> tuple[int, str]:
    key, _ = item

    if key.startswith("rev_"):
        suffix = key.removeprefix("rev_")
        if suffix.isdigit():
            return int(suffix), key

    return 999_999, key


def collect_revisions(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        value
        for key, value in sorted(metadata.items(), key=revision_sort_key)
        if key not in RESERVED_REVISIONS_TABLE_KEYS and isinstance(value, dict)
    ]


def collect_columns(revisions: list[dict[str, Any]]) -> list[str]:
    columns: list[str] = []

    for revision in revisions:
        for column_name in revision:
            if column_name not in columns:
                columns.append(column_name)

    return columns


def get_bookmark_name(metadata: dict[str, Any]) -> str:
    bookmark = metadata.get("bookmark")

    if bookmark is None or not str(bookmark).strip():
        raise ValueError("The revisions YAML does not define a bookmark.")

    return str(bookmark).strip()


def iter_block_items(document: DocumentObject):
    body = document.element.body

    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, document)
        elif child.tag == qn("w:tbl"):
            yield Table(child, document)


def paragraph_contains_bookmark(paragraph: Paragraph, bookmark_name: str) -> bool:
    for bookmark in paragraph._element.iter(qn("w:bookmarkStart")):
        if bookmark.get(qn("w:name")) == bookmark_name:
            return True

    return False


def find_next_table_after_bookmark(document: DocumentObject, bookmark_name: str) -> Table:
    found_bookmark = False

    for block in iter_block_items(document):
        if isinstance(block, Paragraph) and paragraph_contains_bookmark(block, bookmark_name):
            found_bookmark = True
            continue

        if found_bookmark and isinstance(block, Table):
            return block

    raise ValueError(f"Could not find a table after bookmark '{bookmark_name}'.")


def add_revision_rows_to_table(
    table: Table,
    revisions: list[dict[str, Any]],
    columns: list[str],
) -> None:
    for revision in revisions:
        row = table.add_row()

        for index, column in enumerate(columns):
            if index >= len(row.cells):
                break

            row.cells[index].text = str(revision.get(column, ""))


def update_docx_revisions_table(
    input_docx: str,
    output_docx: str,
    revisions_metadata: dict[str, Any],
) -> None:
    bookmark_name = get_bookmark_name(revisions_metadata)

    revisions = collect_revisions(revisions_metadata)
    columns = collect_columns(revisions)

    document = Document(input_docx)
    table = find_next_table_after_bookmark(document, bookmark_name)

    add_revision_rows_to_table(
        table=table,
        revisions=revisions,
        columns=columns,
    )

    document.save(output_docx)