#!/usr/bin/env bash

# K-65P Certification Preparation Script
# Combines all relevant code and documentation into a single digest file for LLM Auditors.

OUTPUT_FILE="K65P_DIGEST.txt"

echo "Creating K-65P Certification Digest..."
> "$OUTPUT_FILE"

append_file() {
	local file=$1
	if [ -f "$file" ]; then
		echo "Appending $file..."
		echo -e "\n\n================================================================" >> "$OUTPUT_FILE"
		echo "FILE: $file" >> "$OUTPUT_FILE"
		echo "================================================================" >> "$OUTPUT_FILE"
		cat "$file" >> "$OUTPUT_FILE"
	fi
}

# Documentation & Configs at root
append_file "README.md"
append_file "CHANGELOG.md"
append_file "CONVENTIONS.md"
append_file "pyproject.toml"

# Deep Documentation
find docs -type f -name "*.md" 2>/dev/null | sort | while read -r line; do
	append_file "$line"
done

# Source Files
find src -type f -name "*.py" 2>/dev/null | sort | while read -r line; do
	append_file "$line"
done

# Unit & Integration Tests
find tests -type f -name "*.py" 2>/dev/null | sort | while read -r line; do
	append_file "$line"
done

echo "Done! The digest is ready at $OUTPUT_FILE."
echo "Total payload: $(wc -l < "$OUTPUT_FILE") lines."
