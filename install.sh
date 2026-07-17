#!/bin/bash
# 倒计时提醒器 v2.0 - 系统安装脚本 (适配 Ubuntu 24.04/PEP 668)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🎯 倒计时提醒器 v2.0 - 系统安装"
echo "======================================="
echo "这将把倒计时提醒器安装到您的Linux系统中"

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用sudo权限运行此脚本："
    echo "   sudo bash install.sh"
    exit 1
fi

# 检查Python版本
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "🐍 检测到 Python 版本: $PYTHON_VERSION"

echo ""
echo "📦 步骤 1/5: 安装系统依赖包..."

# 安装必要的系统库（包含之前报错缺失的 libgirepository 和 cairo）
if command -v apt &> /dev/null; then
    apt update
    apt install -y python3 python3-pip python3-venv python3-tk python3-gi libgirepository1.0-dev pkg-config desktop-file-utils libcairo2-dev
elif command -v yum &> /dev/null; then
    yum install -y python3 python3-pip python3-tkinter gobject-introspection-devel pkg-config desktop-file-utils
elif command -v pacman &> /dev/null; then
    pacman -S --noconfirm python python-pip tk python-gobject desktop-file-utils
fi

echo "✅ 系统依赖安装完成"
echo ""
echo "📁 步骤 2/5: 创建应用程序目录..."

APP_DIR="/opt/countdown-timer"
mkdir -p "$APP_DIR"
echo "✅ 应用程序目录创建完成: $APP_DIR"

echo ""
echo "📦 步骤 3/5: 创建隔离的虚拟环境并安装依赖..."

# 使用隔离环境，避免新版发行版的 PEP 668 系统 Python 限制。
# system-site-packages 允许复用包管理器安装的 PyGObject。
python3 -m venv --system-site-packages "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install -r requirements.txt
echo "✅ Python依赖在虚拟环境中安装完成"

echo ""
echo "📋 步骤 4/5: 复制文件并生成快捷方式..."

cp countdown_timer.py "$APP_DIR/"
chmod +x "$APP_DIR/countdown_timer.py"

if [ -f "icon.png" ]; then
    cp icon.png "$APP_DIR/"
fi

# 创建桌面快捷方式，Exec 指向虚拟环境的 Python 解释器
cat > /usr/share/applications/countdown-timer.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=倒计时提醒器
Comment=自定义倒计时时间和提醒内容的桌面应用
Comment[en]=Desktop countdown timer with custom time and reminder messages
Exec=$APP_DIR/venv/bin/python3 $APP_DIR/countdown_timer.py
Icon=$APP_DIR/icon.png
Terminal=false
StartupNotify=true
Categories=Utility;Office;
EOF

# 创建全局命令行启动脚本
cat > /usr/local/bin/countdown-timer << EOF
#!/bin/bash
$APP_DIR/venv/bin/python3 $APP_DIR/countdown_timer.py "\$@"
EOF
chmod +x /usr/local/bin/countdown-timer

update-desktop-database /usr/share/applications/ 2>/dev/null

echo "✅ 应用程序安装完成"

echo ""
echo "🧪 步骤 5/5: 环境兼容性检查..."

# 测试程序是否可以正常导入
"$APP_DIR/venv/bin/python3" -c "
import importlib.util
import sys
sys.path.insert(0, '$APP_DIR')
import tkinter as tk
assert importlib.util.find_spec('pystray') is not None
from PIL import Image
print('✅ 所有模块导入成功')
"

echo "✅ 安装测试通过"

echo ""
echo "🎉 安装完成！"
echo "======================================="
echo ""
echo "📱 启动方式："
echo "   1. 在应用程序菜单中搜索 '倒计时提醒器'"
echo "   2. 命令行运行: countdown-timer"
echo "   3. 或直接运行: $APP_DIR/countdown_timer.py"
echo ""
echo "🗑️  卸载方式："
echo "   运行项目目录下的: sudo bash uninstall.sh"
echo ""
echo "💡 功能特色："
echo "   • 自定义倒计时时间和提醒内容"
echo "   • 支持暂停/继续/停止/重置"
echo "   • 系统托盘后台运行"
echo "   • 预设常用时间（番茄工作法等）"
echo "   • 多种提醒方式（声音+弹窗+置顶）"
echo ""
echo "📚 更多帮助: https://github.com/radical2333/countdown-timer"
echo ""

# 提示用户重新登录或更新桌面环境
echo "💡 如果在应用程序菜单中找不到程序，请："
echo "   1. 注销并重新登录"
echo "   2. 或重启桌面环境"
echo ""
