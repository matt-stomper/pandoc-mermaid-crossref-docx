# Pandoc-mermaid-crossref

This project aims to combine pandoc, mermaid-cli, pandoc-crossref, pandoc-acro, pandoc-include and markdown together to produce 
Microsoft Docx files with a title page and custom properties for use within the docx to create headers and footers 
for example.

This idea was spawned for a few reasons:

1. Incorporating the documentation into development instead of it being at the end.
2. Version control design documents with `git`. We can now write documentation in Markdown with Mermaid diagrams
3. System requirements and tests exported from a tool that only exported DOCX or PDF can be appended to documents or incorporated within the document.
4. Latex is great, and this tool is partially trying to do what Latex does; but having managers in the corporate space trying to write Latex for minor revisions
is too much of a learning curve.
5. Other tools (such as Jira) export to CSV or have API where queries can be run and then parsed into Markdown.
This Markdown can then be included in the original Markdown document and rendered into a Microsoft Docx file.

## Dependencies

### Pandoc

[pandoc](https://github.com/jgm/pandoc)

### Figure/Table/Section Referencing

[Pandoc CrossRef](https://github.com/lierdakil/pandoc-crossref)

### Acronyms

[pandoc-acro](https://kprussing.github.io/pandoc-acro/)

### Diagramming

[mermaid-filter](https://github.com/raghur/mermaid-filter)

This project incorporates mermaid.js for diagramming. There is an issue with using pandoc-crossref where a caption is not
added to the image because it just doesn't exist. This is resolved by doing two passes over the document with Pandoc. 
These passes are:
1. Convert with the mermaid-filter the Markdown with mermaid to Markdown with image (that is built with mermaid)
2. Convert the Markdown with images through the remaining filters and convert to docx

## Building the container

```shell
uv venv # or  
python3 -m venv .venv
```

```shell
source .venv/bin/activate
```

```shell
uv pip install poethepoet # or
pip install poethepoet
```

```shell
poe build-docker
```

The breakdown or what is in this command is in [poe_tasks.toml](poe_tasks.toml)

## Running the container

From the `svd_example`, the build process is staged to allow for success of the different filters to run.

01_svd.yaml runs `pandoc_include` and `pandoc_acro`
02_svd.yaml runs mermaid filter
03_svd.yaml runs the final conversion to docx

03_svd.yaml can be substituted for an HTML or PDF. 

Compile the DOCX with `docker compose run --rm pandoc-mermaid-crossref`

## Other options

If you are required to combine a DOCX and a Markdown before combining with the title page, use docxcompose (installed)
to combine the documents in the following steps:
1. Convert the Markdown to docx
2. `docxcompose file1.docx file2.docx -o combined.docx`
3. run inject-properties.py with the title page and the combined.docx

## Syntax

### Referencing from Pandoc Crossref

 - {#fig:image_reference} to create the reference and @fig:reference to reference the figure
 - {#tble:table_reference} to create the reference and @tble:table_reference to reference the table
 - {#sec:section_reference} to create the reference and @sec:section_reference to reference the section
 - {lst:listing_reference} to create the reference and @lst:listing_reference to reference the listing

### Mermaid Images

Including mermaid diagrams in the Markdown file requires the mermaid filter to be run before pandoc-crossref. 
Mermaid filter needs to create the image first before it can be referenced by pandoc-crossref.

Combining the Mermaid with pandoc-crossref requires the following syntax:

```markdown
```{.mermaid caption="Mermaid image caption" #fig:mermaid_reference}
flowchart TD
  ...
```
### Acronyms

[pandoc-acro](https://kprussing.github.io/pandoc-acro/) uses the acronym.yaml to define the acronyms. They are referenced as `+acro` with the `+` defining the acronym.

The version of pandoc-acro in the Docker container uses some extra YAML keys to allow the user to define the acronym as a list or a table with a caption.
This container uses this PR for the code. [pandoc-acro PR](https://github.com/matt-stomper/pandoc-acro). I'm not sure if it will get merged or not.

```yaml
acronym-list:
  format: table
  caption: List of acronyms {#tbl:list-acronyms} 
```

## more-pandoc-filters

This container uses a few extra filters to create the engineering documentation to match the DI-IPSC-814** specs.

### Landscape filter

The landscape filter is a docx filter that allows the user to mark a section as landscape. It creates a section break making the new section landscape.
At the end of the `div`, it creates another break returning the document to portait.

```markdown
::: landscape
:::
```

### Level 1 heading break filter

This filter puts a page break before each level 1 heading.

### Bibliography Table Filter

This filter takes the references from pandoc-citeproc and puts the references in a single column table.
This filter is still going through some improvements.

### Table Column Filter

This filter reads in the column widths from the table attributes and applies the widths to each column.
The widths are in percentages.
The Column Width Filter works with pandoc-crossref.

```markdown
| Col 1  | Col 2  |
|--------|--------|
| Data 1 | Data 2 |

: Example Table {#tbl:example_table colWidths="10 90"}
```

## Docx_tools

Read about [docx_tools here](docx_tools/README.md)
