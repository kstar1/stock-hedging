#!/bin/bash

cd "$(git rev-parse --show-toplevel)" || exit

echo "📦 Generating TSLA app code snapshot..."

output_file="/Users/kshitijdutt/Downloads/tsla_app_snapshot.txt"
echo "=== TSLA App Snapshot: $(date) ===" > "$output_file"

find . -name "*.py" | while read -r file; do
    echo -e "\n\n===== $file =====" >> "$output_file"
    cat "$file" >> "$output_file"
done

echo "✅ Done. Snapshot saved to: $output_file"
