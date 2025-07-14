# Release v2.0 描述模板

## 🎉 倒计时提醒器 v2.0 正式发布！

这是一个功能完整的Linux桌面倒计时应用，支持自定义时间、提醒内容和系统托盘功能。

### ✨ 主要功能

- 🕐 **自定义倒计时时间** - 支持小时、分钟、秒的精确设置
- 📝 **自定义提醒内容** - 可设置个性化的提醒文字
- ⏸️ **完整的控制功能** - 暂停/继续/停止/重置
- 🔔 **多种提醒方式** - 声音提醒 + 弹窗提醒 + 窗口置顶
- 📱 **系统托盘支持** - 最小化到托盘后台运行
- ⚡ **预设时间** - 内置常用时间（5分钟、番茄工作法25分钟等）
- 🛡️ **防误关保护** - 智能询问是否最小化到托盘

### 🚀 系统集成特性

- **一键安装** - `sudo bash install.sh` 系统级安装
- **桌面菜单集成** - 自动注册到应用程序菜单
- **全局启动器** - 可从任何位置运行 `countdown-timer`
- **完整卸载** - `sudo bash uninstall.sh` 彻底移除

### 📋 系统要求

- **操作系统**: Linux (Ubuntu 18.04+, Debian 10+等)
- **Python版本**: Python 3.8+
- **桌面环境**: 支持X11的桌面环境（GNOME, KDE, XFCE等）

### 🛠️ 快速安装

```bash
# 下载项目
git clone https://github.com/radical2333/countdown-timer.git
cd countdown-timer

# 系统级安装
sudo bash install.sh
```

安装完成后可通过以下方式启动：
- 应用程序菜单中搜索"倒计时提醒器"
- 命令行运行：`countdown-timer`

### 📦 下载文件

- `countdown-timer-v2.0.tar.gz` - 完整安装包
- 包含所有必需文件和安装脚本
- 解压后运行 `sudo bash install.sh` 即可安装

### 🔧 技术栈

- **GUI框架**: Python Tkinter
- **系统托盘**: PySystemTray + AppIndicator
- **图像处理**: Pillow
- **系统集成**: 标准Linux桌面集成

### 🙏 致谢

感谢所有测试和反馈的用户！如有问题或建议，请通过 Issues 联系。

---

⭐ 如果这个项目对您有帮助，请考虑给它一个 Star！
