#!/bin/bash
# 倒计时提醒器启动脚本
# 此脚本可以从任何位置启动倒计时提醒器

# 应用程序安装路径
APP_DIR="/opt/countdown-timer"
PYTHON_EXEC="$APP_DIR/venv/bin/python3"

# 检查应用程序是否已安装
if [ ! -f "$APP_DIR/countdown_timer.py" ]; then
    echo "❌ 错误: 倒计时提醒器未安装"
    echo "💡 请先运行安装脚本: sudo bash install.sh"
    exit 1
fi

if [ ! -x "$PYTHON_EXEC" ]; then
    echo "❌ 错误: 应用程序虚拟环境不存在"
    echo "💡 请重新运行安装脚本: sudo bash install.sh"
    exit 1
fi

# 检查是否有图形环境
if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
    echo "❌ 错误: 未检测到图形环境"
    echo "💡 请在桌面环境中运行此程序"
    exit 1
fi

# 切换到应用程序目录并启动
cd "$APP_DIR"
exec "$PYTHON_EXEC" countdown_timer.py "$@"
