#!/bin/bash
# 倒计时提醒器 v2.0 - 系统安装脚本 (适配 Ubuntu 24.04/PEP 668)

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

# 在安装目录创建虚拟环境，解决外部环境管理错误 (PEP 668)
# 使用 --system-site-packages 是为了能直接调用系统安装好的 python3-gi (PyGObject)
python3 -m venv --system-site-packages "$APP_DIR/venv"

# 使用虚拟环境内的 pip 进行安装
"$APP_DIR/venv/bin/pip" install --upgrade pip
"$APP_DIR/venv/bin/pip" install pystray>=0.19.0 Pillow>=8.0.0 PyGObject>=3.36.0

if [ $? -ne 0 ]; then
    echo "❌ Python依赖安装失败"
    exit 1
fi
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

"$APP_DIR/venv/bin/python3" -c "import pystray, PIL, gi; print('✅ 模块导入正常')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "🎉 安装成功！"
    echo "现在可以通过菜单搜索 '倒计时提醒器' 或在终端输入 'countdown-timer' 运行。"
else
    echo "⚠️  警告：环境检查未完全通过，可能是由于缺少特定桌面环境的库。"
fi
