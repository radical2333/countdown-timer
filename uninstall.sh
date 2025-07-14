#!/bin/bash
# 倒计时提醒器 v2.0 - 卸载脚本

echo "🗑️ 倒计时提醒器 v2.0 - 卸载程序"
echo "======================================="
echo "这将从您的系统中完全移除倒计时提醒器"
echo ""

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用sudo权限运行此脚本："
    echo "   sudo bash uninstall.sh"
    exit 1
fi

# 确认卸载
read -p "❓ 确定要卸载倒计时提醒器吗？ (y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "❌ 卸载已取消"
    exit 0
fi

echo ""
echo "📁 步骤 1/4: 移除应用程序文件..."

# 移除应用程序目录
if [ -d "/opt/countdown-timer" ]; then
    rm -rf /opt/countdown-timer
    echo "✅ 已删除 /opt/countdown-timer"
else
    echo "💡 /opt/countdown-timer 目录不存在"
fi

# 移除全局启动器
if [ -f "/usr/local/bin/countdown-timer" ]; then
    rm -f /usr/local/bin/countdown-timer
    echo "✅ 已删除全局启动器"
else
    echo "💡 全局启动器不存在"
fi

echo ""
echo "🗂️ 步骤 2/4: 移除桌面菜单项..."

# 移除桌面文件
DESKTOP_FILE="/usr/share/applications/countdown-timer.desktop"
if [ -f "$DESKTOP_FILE" ]; then
    rm -f "$DESKTOP_FILE"
    echo "✅ 已删除桌面菜单项"
else
    echo "💡 桌面菜单项不存在"
fi

echo ""
echo "🔄 步骤 3/4: 更新桌面数据库..."

# 更新桌面数据库
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications
    echo "✅ 桌面数据库已更新"
else
    echo "💡 跳过桌面数据库更新"
fi

echo ""
echo "🧹 步骤 4/4: 清理缓存..."

# 清理可能的缓存文件
if [ -d "/home/*/.cache/countdown-timer" ]; then
    rm -rf /home/*/.cache/countdown-timer 2>/dev/null
fi

echo "✅ 清理完成"
echo ""
echo "🎉 倒计时提醒器已成功卸载！"
echo ""
echo "💡 提示："
echo "   - Python依赖包(pystray, Pillow等)仍保留在系统中"
echo "   - 如需完全清理，可手动运行: pip3 uninstall pystray Pillow PyGObject"
echo "   - 感谢您的使用！"
