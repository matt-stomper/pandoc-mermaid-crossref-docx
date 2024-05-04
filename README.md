# Pandoc-mermaid-crossref

This project aims to combine pandoc, mermaid-cli, pandoc-crossref, pandoc-acro and markdown together to produce 
Microsoft Docx files with a title page and custom properties for use within the docx to create headers and footers 
for example.

This idea was spawned from wanting to write documentation in markdown with Mermaid diagrams and having system
requirements and tests exported from a tool that only exported DOCX or PDF. 

## Dependencies

### Pandoc

[pandoc](https://github.com/jgm/pandoc)

### Figure/Table/Section Referencing

[Pandoc CrossRef](https://github.com/lierdakil/pandoc-crossref)

### Acronyms

[pandoc-acro](https://kprussing.github.io/pandoc-acro/)

### Diagraming

[mermaid-filter](https://github.com/raghur/mermaid-filter)

This project incorporates mermaid.js for diagramming. There is an issue with using pandoc-crossref where a caption is not
added to the image because it just doesn't exist. This is resolved by doing two passes over you document with Pandoc. 
These passes are:
1. Convert with the mermaid-filter the markdown with mermaid to markdown with image (that is built with mermaid)
1. Convert the markdown with images through the remaining filters and convert to docx

#### Example Mermaid with pandoc-crossref caption.

>Note: This mermaid diagram will not render in most previews due to the addition of the caption.
 
```{.mermaid format=png loc=images caption="Class Diagram" #fig:classDiagram}

---
title: Animal example
---
classDiagram
    note "From Duck till Zebra"
    Animal <|-- Duck
    note for Duck "can fly\ncan swim\ncan dive\ncan help in debugging"
    Animal <|-- Fish
    Animal <|-- Zebra
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Animal: +mate()
    class Duck{
        +String beakColor
        +swim()
        +quack()
    }
    class Fish{
        -int sizeInFeet
        -canEat()
    }
    class Zebra{
        +bool is_wild
        +run()
    }

```
>Thanking mermaid.js for the example from https://mermaid.js.org/syntax/classDiagram.html

The class diagram @fig:classDiagram can be referenced in the documentation like this.

## Building the container

> Note: This container is not published.

`docker build . -t [tag_of_your_choice]`

## Running the container

Due to the need to run Pandoc with the mermaid-filter first and then again with all other filters, it is 
recommended to write a script like the example one `example/example.sh`.

`docker run --rm --volume "`pwd`:/data" --entrypoint "/data/example/example.sh" [tag_of_your_choice]`

## Other options

If you are required to combine a DOCX and a markdown before combining with the title page, use docxcompose (installed)
to combine the documents in the following steps:
1. Convert the markdown to docx
2. `docxcompose file1.docx file2.docx -o combined.docx`
3. run inject-properties.py with the title page and the combined.docx
