#!/bin/bash

cleanup_working_files() {
    echo "Cleaning up..."
    files=("02-svd.md" "03-svd.md" "mermaid-filter.err" "svd.docx")

    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            echo "Deleted $file"
        fi
    done
    exit 1
}

docx=svd.docx
final_doc=final_svd.docx
template=reference_doc.docx
properties=svd_custom_properties.yaml

echo "Running 01_svd.yaml..."
pandoc -d 01_svd.yaml || cleanup_working_files

echo "Running 02_svd.yaml..."
pandoc -d 02_svd.yaml || cleanup_working_files

echo "Running 03_svd.yaml..."
pandoc -d 03_svd.yaml || cleanup_working_files

echo "Running inject-properties.py..."
python3 -m docx_tools.inject_properties combine-properties-document -y $properties -i $docx -t $template -o $final_doc

cleanup_working_files


