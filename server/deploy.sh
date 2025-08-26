#!/usr/bin/env bash
set -euo pipefail

# Deploy script for Fetchly server (FastAPI + Uvicorn)
# - Creates a Python venv under .venv
# - Installs dependencies from requirements.txt
# - Verifies ffmpeg and yt-dlp availability
# - Starts the server with uvicorn

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

PY=${PYTHON:-python3}
VENV_DIR="${PROJECT_DIR}/.venv"

log() { echo -e "[deploy] $*"; }

log "Using project dir: $PROJECT_DIR"

if [ ! -d "$VENV_DIR" ]; then
  log "Creating virtual environment in $VENV_DIR"
  "$PY" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

log "Upgrading pip"
python -m pip install --upgrade pip wheel setuptools >/dev/null

log "Installing Python dependencies"
pip install -r requirements.txt

# Optional: install system deps if missing (informative checks)
if ! command -v ffmpeg >/dev/null 2>&1; then
  log "WARNING: ffmpeg not found on PATH. Video/audio conversions and format probing may be limited."
fi

if ! command -v yt-dlp >/dev/null 2>&1; then
  log "yt-dlp not found globally; installing it into the venv"
  pip install yt-dlp
fi

# Create downloads directory inside server if not present
mkdir -p "${PROJECT_DIR}/downloads"

# Export common env vars (customize as needed)
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8000}

log "Starting server on ${HOST}:${PORT}"
exec uvicorn main:app --host "$HOST" --port "$PORT"
