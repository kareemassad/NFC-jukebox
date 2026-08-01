#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON="$SCRIPT_DIR/.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
    echo "Missing $PYTHON. Complete the installation steps first." >&2
    exit 1
fi

cd "$SCRIPT_DIR"
exec sudo /usr/bin/env \
    SPOTIFY_CLIENT_ID="${SPOTIFY_CLIENT_ID-}" \
    SPOTIFY_CLIENT_SECRET="${SPOTIFY_CLIENT_SECRET-}" \
    SPOTIFY_USERNAME="${SPOTIFY_USERNAME-}" \
    PUSHBULLET_API_KEY="${PUSHBULLET_API_KEY-}" \
    "$PYTHON" "$SCRIPT_DIR/Read.py"
