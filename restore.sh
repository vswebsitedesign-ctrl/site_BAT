#!/bin/bash
DIR=$1
if [ -z "$DIR" ]; then echo "ERROR: specify snapshot dir e.g. bash restore.sh snapshots/20260611_120000_label"; exit 1; fi
cp "$DIR/build.py" build.py
cp "$DIR/base.html" theme/base.html
cp "$DIR/pages.json" data/pages.json
cp "$DIR/Master_Report.json" Master_Report.json
echo "✅ Restored from $DIR"
