#!/bin/bash
# 倒计时提醒器 v2.0 - 系统安装脚本

echo "🎯 倒计时提醒器 v2.0 - 系统安装"
echo "======================================="
echo "这将把倒计时提醒器安装到您的Linux系统中"
echo ""

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用sudo权限运行此脚本："
    echo "   sudo bash install.sh"
    exit 1
fi

# 检测操作系统
if ! command -v apt &> /dev/null && ! command -v yum &> /dev/null && ! command -v pacman &> /dev/null; then
    echo "❌ 错误: 不支持的Linux发行版"
    echo "💡 此脚本支持: Ubuntu/Debian, CentOS/RHEL, Arch Linux"
    exit 1
fi

# 检查Python版本
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "🐍 检测到 Python 版本: $PYTHON_VERSION"

echo ""
echo "📦 步骤 1/5: 安装系统依赖包..."

# 根据不同发行版安装依赖
if command -v apt &> /dev/null; then
    # Ubuntu/Debian
    apt update
    apt install -y python3 python3-pip python3-venv python3-tk python3-gi libgirepository1.0-dev pkg-config desktop-file-utils
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    yum install -y python3 python3-pip python3-tkinter gobject-introspection-devel pkg-config desktop-file-utils
elif command -v pacman &> /dev/null; then
    # Arch Linux
    pacman -S --noconfirm python python-pip tk python-gobject desktop-file-utils
fi

if [ $? -ne 0 ]; then
    echo "❌ 系统依赖安装失败"
    exit 1
fi

echo "✅ 系统依赖安装完成"
echo ""
echo "📁 步骤 2/5: 创建应用程序目录..."

# 创建应用程序安装目录
APP_DIR="/opt/countdown-timer"
mkdir -p "$APP_DIR"

echo "✅ 应用程序目录创建完成: $APP_DIR"
echo ""
echo "📦 步骤 3/5: 安装Python依赖..."

# 安装Python依赖到系统
pip3 install pystray>=0.19.0 Pillow>=8.0.0 PyGObject>=3.36.0

if [ $? -ne 0 ]; then
    echo "❌ Python依赖安装失败"
    exit 1
fi

echo "✅ Python依赖安装完成"
echo ""
echo "📋 步骤 4/5: 复制应用程序文件..."

# 复制主程序文件
cp countdown_timer.py "$APP_DIR/"
chmod +x "$APP_DIR/countdown_timer.py"

# 复制启动器到系统路径（可选）
if [ -f "launcher.sh" ]; then
    cp launcher.sh /usr/local/bin/countdown-timer
    chmod +x /usr/local/bin/countdown-timer
    echo "✅ 全局启动器已安装: countdown-timer"
fi

# 复制图标文件
if [ -f "icon.png" ]; then
    cp icon.png "$APP_DIR/"
else
    echo "⚠️  警告: 图标文件不存在，将使用默认图标"
fi

# 创建桌面文件
cat > /usr/share/applications/countdown-timer.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=倒计时提醒器
Name[en]=Countdown Timer
Comment=自定义倒计时时间和提醒内容的桌面应用
Comment[en]=Desktop countdown timer with custom time and reminder messages
Exec=$APP_DIR/countdown_timer.py
Icon=$APP_DIR/icon.png
Terminal=false
StartupNotify=true
Categories=Utility;Office;
Keywords=timer;countdown;reminder;productivity;
StartupWMClass=CountdownTimer
EOF

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications/
fi

echo "✅ 应用程序文件安装完成"
echo ""
echo "🧪 步骤 5/5: 测试安装..."

# 测试程序是否可以正常导入
python3 -c "
import sys
sys.path.insert(0, '$APP_DIR')
import tkinter as tk
import pystray
from PIL import Image
print('✅ 所有模块导入成功')
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ 安装测试通过"
else
    echo "⚠️  安装测试未完全通过，但应用程序应该可以使用"
fi

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
