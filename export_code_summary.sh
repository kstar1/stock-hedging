#!/bin/bash

# Define output file
OUTPUT_FILE="tsla_app_snapshot.txt"
TEMP_FILE="/tmp/$OUTPUT_FILE"
DEST="/Users/kshitijdutt/Downloads/$OUTPUT_FILE"

# Start fresh
echo "🔄 Exporting all relevant Python files..." > "$TEMP_FILE"

# Include streamlit_app.py
echo -e "\n\n===== FILE: streamlit_app.py =====\n" >> "$TEMP_FILE"
cat streamlit_app.py >> "$TEMP_FILE"

# Include sidebar
if [ -f src/ui/sidebar.py ]; then
  echo -e "\n\n===== FILE: src/ui/sidebar.py =====\n" >> "$TEMP_FILE"
  cat src/ui/sidebar.py >> "$TEMP_FILE"
fi

# Include all tab files
for file in src/ui/tabs/*.py; do
  echo -e "\n\n===== FILE: $file =====\n" >> "$TEMP_FILE"
  cat "$file" >> "$TEMP_FILE"
done

# Include config/settings.py
if [ -f config/settings.py ]; then
  echo -e "\n\n===== FILE: config/settings.py =====\n" >> "$TEMP_FILE"
  cat config/settings.py >> "$TEMP_FILE"
fi

# Include any data providers
for file in src/data/*.py; do
  echo -e "\n\n===== FILE: $file =====\n" >> "$TEMP_FILE"
  cat "$file" >> "$TEMP_FILE"
done

# Move final file to Downloads
mv "$TEMP_FILE" "$DEST"
echo "✅ Export complete: $DEST"
