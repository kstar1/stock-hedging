#!/bin/bash

OUTPUT_FILE="code_snapshot.txt"
SRC_DIR="src"
CONFIG_FILE="config/config_filters.json"

# Clear or create output file
echo "Generating code snapshot..." > "$OUTPUT_FILE"

# Add config JSON first
echo -e "\n### config_filters.json\n" >> "$OUTPUT_FILE"
cat "$CONFIG_FILE" >> "$OUTPUT_FILE"

# Add all .py files from src/
for file in "$SRC_DIR"/*.py; do
    echo -e "\n### $(basename "$file")\n" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
done

echo "✅ Code snapshot saved to $OUTPUT_FILE"
