#!/usr/bin/env bash
set -euo pipefail

THEME_NAME="minima"
DEST_DIR="/usr/share/plymouth/themes/${THEME_NAME}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $EUID -ne 0 ]]; then
    echo "Error: This script must be run as root." >&2
    exit 1
fi

mkdir -p "${DEST_DIR}"
cp -rf "${SCRIPT_DIR}/${THEME_NAME}.plymouth" "${DEST_DIR}/"
cp -rf "${SCRIPT_DIR}/${THEME_NAME}.script" "${DEST_DIR}/"
cp -rf "${SCRIPT_DIR}/assets" "${DEST_DIR}/"

chmod 755 "${DEST_DIR}"
chmod 755 "${DEST_DIR}/assets"
chmod 644 "${DEST_DIR}/${THEME_NAME}.plymouth"
chmod 644 "${DEST_DIR}/${THEME_NAME}.script"
chmod 644 "${DEST_DIR}/assets"/*

if command -v plymouth-set-default-theme &>/dev/null; then
    plymouth-set-default-theme "${THEME_NAME}"
fi

if command -v mkinitcpio &>/dev/null; then
    mkinitcpio -P
elif command -v update-initramfs &>/dev/null; then
    update-initramfs -u
elif command -v dracut &>/dev/null; then
    dracut --force
elif command -v booster &>/dev/null; then
    /usr/lib/booster/regenerate_images
else
    echo "Rebuild your initramfs manually to apply the theme."
fi
