#!/bin/bash

# Ensure you're in the repo root
cd "$(git rev-parse --show-toplevel)"

echo "📦 Adding updated files to Git..."

git add src/sim/put_breakeven_logic.py
git add src/sim/analytics.py
git add src/ui/tabs/put_chain_tab.py
git add src/ui/sidebar.py 2>/dev/null || echo "ℹ️ sidebar.py not found or unchanged (optional)"

echo "📝 Committing..."
git commit -m "🔁 Added toggle for initial capital (market vs. average price); refactored breakeven logic"

echo "🚀 Pushing to branch: $(git rev-parse --abbrev-ref HEAD)"
git push origin "$(git rev-parse --abbrev-ref HEAD)"

echo "✅ Done!"
