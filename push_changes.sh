#!/bin/bash

# Step 1: Navigate to your repo
cd /Users/kshitijdutt/stock-hedging || exit

# Step 2: Stage updated files
git add src/ui/tabs/put_chain_tab.py

# Step 3: Commit with a message
git commit -m "💄 UI: Compact contract filters + premium display + dynamic hedge cost panel"

# Step 4: Push to remote
git push origin main
