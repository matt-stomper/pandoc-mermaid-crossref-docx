#!/bin/bash

docx=README_final.docx
final_doc=final_doco.docx
template=example/title_page.docx
properties=example/example_custom_properties.yaml

cd /data
pandoc -d example/example_pandoc_mermaid.yaml --verbose
pandoc -d example/example_pandoc.yaml --verbose
python3 inject-properties.py -y $properties -i $docx -t $template -o $final_doc