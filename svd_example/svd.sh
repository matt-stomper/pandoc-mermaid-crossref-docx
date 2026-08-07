#!/bin/bash

cleanup_working_files() {
    echo "Cleaning up..."
    files=("02-svd.md" "03-svd.md" "mermaid-filter.err" "svd.docx" "bibliography_table.log")

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
template=common/template/reference_doc_3.docx
properties=svd_custom_properties.yaml

echo "Running 01_svd.yaml..."
if pandoc -d 01_svd.yaml --verbose; then
  echo "Error in 01_svd.yaml"
fi

echo "Running 02_svd.yaml..."
if pandoc -d 02_svd.yaml --verbose; then
  echo "Error in 01_svd.yaml"
fi

echo "Running inject-properties.py..."
python3 -m docx_tools.inject_properties combine-properties-document \
  -y $properties \
  -k "custom_properties" \
  -i $docx \
  -t $template \
  -r "revisions_table" \
  -o $final_doc

cleanup_working_files
