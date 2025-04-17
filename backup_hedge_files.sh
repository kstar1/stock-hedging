#!/bin/bash

# Create a backup directory in Downloads if it doesn't exist
BACKUP_DIR="$HOME/Downloads/hedge_backup"
mkdir -p "$BACKUP_DIR"

# List of important files to back up
FILES_TO_BACKUP=(
    "src/sim/put_breakeven_logic.py"
    "src/sim/test_put_breakeven.py"
    "src/sim/analytics.py"
    "src/viz/put_breakeven_plot.py"
    "test_plot_edge_cases_breakeven.py"
    "src/ui/tabs/put_chain_tab.py"
)

echo "Backing up files to $BACKUP_DIR..."

for file in "${FILES_TO_BACKUP[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "$BACKUP_DIR"
        echo "✅ Copied $file"
    else
        echo "⚠️ File not found: $file"
    fi
done

echo "✅ Backup complete."
