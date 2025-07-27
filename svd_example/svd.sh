#!/bin/bash

docx=svd.docx
final_doc=final_svd.docx
template=reference_doc.docx
properties=svd_custom_properties.yaml

pandoc -d 01_svd.yaml
pandoc -d 02_svd.yaml
pandoc -d 03_svd.yaml

python3 /app/inject-properties.py -y $properties -i $docx -t $template -o $final_doc