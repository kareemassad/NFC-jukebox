#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON="$SCRIPT_DIR/.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
    echo "Missing $PYTHON. Complete the installation steps first." >&2
    exit 1
fi

cd "$SCRIPT_DIR"
exec sudo -E "$PYTHON" "$SCRIPT_DIR/Read.py"
