#!/bin/bash

BACKUP_DIR="$HOME/Downloads/hedge_backup"

FILES_TO_RESTORE=(
    "put_breakeven_logic.py"
    "test_put_breakeven.py"
    "analytics.py"
    "put_breakeven_plot.py"
    "test_plot_edge_cases_breakeven.py"
    "put_chain_tab.py"
)

DESTINATIONS=(
    "src/sim/"
    "src/sim/"
    "src/sim/"
    "src/viz/"
    "./"
    "src/ui/tabs/"
)

echo "Restoring files from $BACKUP_DIR and staging for commit..."

for i in "${!FILES_TO_RESTORE[@]}"; do
    src="$BACKUP_DIR/${FILES_TO_RESTORE[$i]}"
    dest="${DESTINATIONS[$i]}"
    if [ -f "$src" ]; then
        cp "$src" "$dest"
        git add "$dest${FILES_TO_RESTORE[$i]}"
        echo "✅ Restored and staged: $dest${FILES_TO_RESTORE[$i]}"
    else
        echo "⚠️ Missing backup file: $src"
    fi
done

echo "🚀 Ready to commit your changes."
