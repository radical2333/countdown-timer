#!/bin/bash
# 倒计时提醒器 v2.0 - 项目打包脚本

echo "📦 倒计时提醒器 v2.0 - 打包脚本"
echo "======================================"
echo ""

# 检查必要文件
required_files=("countdown_timer.py" "requirements.txt" "install.sh" "uninstall.sh" "launcher.sh" "create_icon.py" "countdown-timer.desktop" "README.md")

echo "🔍 检查必要文件..."
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少必要文件: $file"
        exit 1
    fi
    echo "✅ $file"
done

# 生成图标
echo ""
echo "🎨 生成应用程序图标..."
python3 create_icon.py
if [ $? -eq 0 ]; then
    echo "✅ 图标生成成功"
else
    echo "❌ 图标生成失败"
    exit 1
fi

# 检查权限
echo ""
echo "🔐 设置执行权限..."
chmod +x install.sh uninstall.sh launcher.sh countdown_timer.py
echo "✅ 权限设置完成"

# 创建发布目录
RELEASE_DIR="countdown-timer-v2.0"
if [ -d "$RELEASE_DIR" ]; then
    rm -rf "$RELEASE_DIR"
fi
mkdir "$RELEASE_DIR"

# 复制文件到发布目录
echo ""
echo "📋 复制文件到发布目录..."
cp countdown_timer.py requirements.txt install.sh uninstall.sh launcher.sh "$RELEASE_DIR/"
cp create_icon.py icon.png countdown-timer.desktop README.md "$RELEASE_DIR/"

if [ -f "LICENSE" ]; then
    cp LICENSE "$RELEASE_DIR/"
fi

echo "✅ 文件复制完成"

# 创建压缩包
echo ""
echo "🗜️ 创建压缩包..."
tar -czf "countdown-timer-v2.0.tar.gz" "$RELEASE_DIR"
echo "✅ 压缩包创建完成: countdown-timer-v2.0.tar.gz"

# 创建安装说明
cat > "$RELEASE_DIR/INSTALL.txt" << 'EOF'
倒计时提醒器 v2.0 - 安装说明
===============================

系统要求:
- Linux操作系统 (Ubuntu 18.04+, Debian 10+等)
- Python 3.8+
- 支持X11的桌面环境

快速安装:
1. 解压文件包
2. 进入目录: cd countdown-timer-v2.0
3. 运行安装: sudo bash install.sh

使用方法:
- 应用程序菜单中找到"倒计时提醒器"
- 或命令行运行: countdown-timer

卸载方法:
- 运行: sudo bash uninstall.sh

更多信息请查看 README.md
EOF

echo ""
echo "📄 安装说明已创建: $RELEASE_DIR/INSTALL.txt"

echo ""
echo "🎉 打包完成！"
echo "======================================"
echo "📦 发布目录: $RELEASE_DIR"
echo "📄 压缩包: countdown-timer-v2.0.tar.gz"
echo ""
echo "分发说明:"
echo "1. 将压缩包发送给用户"
echo "2. 用户解压: tar -xzf countdown-timer-v2.0.tar.gz"
echo "3. 用户安装: cd countdown-timer-v2.0 && sudo bash install.sh"
echo ""
