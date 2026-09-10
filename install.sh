#!/usr/bin/env bash
set -euo pipefail
command -v python3 >/dev/null 2>&1 || { echo "python3 is required. Install it, then run this script again." >&2; exit 1; }
exec python3 "$(cd "$(dirname "$0")" && pwd)/kit/ste.py" install "$@"
