#!/bin/bash
# 创建倒计时提醒器发布压缩包。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="${1:-2.0}"
PACKAGE_NAME="countdown-timer-v${VERSION}"
ARCHIVE_PATH="$SCRIPT_DIR/${PACKAGE_NAME}.tar.gz"
BUILD_DIR="$(mktemp -d)"
RELEASE_DIR="$BUILD_DIR/$PACKAGE_NAME"
trap 'rm -rf "$BUILD_DIR"' EXIT

required_files=(
    countdown_timer.py requirements.txt install.sh uninstall.sh launcher.sh
    create_icon.py icon.png countdown-timer.desktop README.md INSTALL.txt LICENSE
)

for file in "${required_files[@]}"; do
    if [ ! -f "$SCRIPT_DIR/$file" ]; then
        echo "缺少必要文件: $file" >&2
        exit 1
    fi
done

mkdir -p "$RELEASE_DIR"
cp "${required_files[@]/#/$SCRIPT_DIR/}" "$RELEASE_DIR/"
chmod +x "$RELEASE_DIR/countdown_timer.py" "$RELEASE_DIR/install.sh" \
    "$RELEASE_DIR/uninstall.sh" "$RELEASE_DIR/launcher.sh"

tar -czf "$ARCHIVE_PATH" -C "$BUILD_DIR" "$PACKAGE_NAME"
echo "发布包已生成: $ARCHIVE_PATH"
