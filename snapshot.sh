#!/bin/bash
LABEL=${1:-"snapshot"}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DIR="snapshots/${TIMESTAMP}_${LABEL}"
mkdir -p "$DIR"
cp build.py "$DIR/"
cp theme/base.html "$DIR/"
cp data/pages.json "$DIR/"
cp Master_Report.json "$DIR/"
echo "✅ Snapshot saved to $DIR"
