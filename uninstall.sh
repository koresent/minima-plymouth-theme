#!/usr/bin/env bash
set -euo pipefail

THEME_NAME="minima"
DEST_DIR="/usr/share/plymouth/themes/${THEME_NAME}"

if [[ $EUID -ne 0 ]]; then
    echo "Error: This script must be run as root." >&2
    exit 1
fi

rm -rf "${DEST_DIR}"

if command -v plymouth-set-default-theme &>/dev/null; then
    if plymouth-set-default-theme --list | grep -q "^bgrt$"; then
        plymouth-set-default-theme bgrt
    elif plymouth-set-default-theme --list | grep -q "^spinner$"; then
        plymouth-set-default-theme spinner
    fi
fi

if command -v mkinitcpio &>/dev/null; then
    mkinitcpio -P
elif command -v update-initramfs &>/dev/null; then
    update-initramfs -u
elif command -v dracut &>/dev/null; then
    dracut --force
fi
