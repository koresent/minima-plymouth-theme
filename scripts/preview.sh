#!/usr/bin/env bash
set -euo pipefail

DURATION="${1:-6}"
TTY_DEV="${2:-/dev/tty}"

if [[ $EUID -ne 0 ]]; then
    echo "Error: Preview requires root privileges." >&2
    exit 1
fi

plymouthd --tty="${TTY_DEV}" --debug || true
plymouth --show-splash
sleep "${DURATION}"

if [[ "${3:-}" == "--test-dialog" ]]; then
    plymouth ask-for-password --prompt="Passphrase" || true
fi

plymouth quit
pkill -9 plymouthd || true
