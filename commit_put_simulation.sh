#!/bin/bash

# Navigate to the Git root directory
cd "$(git rev-parse --show-toplevel)" || exit

echo "📦 Staging PUT simulation feature files..."

git add src/ui/tabs/put_chain_tab.py
git add src/sim/put_simulation_logic.py
git add src/viz/put_simulation_plot.py

echo "📝 Committing..."
git commit -m "💡 Added PUT Net P&L Simulator with interactive selection and same-page integration"

echo "🚀 Pushing to branch: $(git rev-parse --abbrev-ref HEAD)"
git push origin "$(git rev-parse --abbrev-ref HEAD)"

echo "✅ Done! Your Net P&L simulation feature is live on GitHub."
