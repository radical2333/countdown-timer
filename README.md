# 倒计时提醒器

一个功能完整的桌面倒计时应用，支持自定义时间、提醒内容和系统托盘功能。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Linux-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ 功能特性

- 🕐 **自定义倒计时时间** - 支持小时、分钟、秒的精确设置
- 📝 **自定义提醒内容** - 可设置个性化的提醒文字
- ⏸️ **暂停/继续功能** - 随时暂停和恢复倒计时
- 🔄 **停止/重置功能** - 完整的计时器控制
- 🔔 **多种提醒方式** - 声音提醒 + 弹窗提醒 + 窗口置顶
- 📱 **系统托盘支持** - 最小化到托盘后台运行
- ⚡ **预设时间快捷设置** - 内置常用时间（番茄工作法等）
- 🛡️ **防误关保护** - 关闭窗口时智能询问
- 🎨 **现代化界面** - 简洁美观的用户界面

## 📋 系统要求

- **操作系统**: Linux (Ubuntu 18.04+, Debian 10+等)
- **Python版本**: Python 3.8+
- **桌面环境**: 支持X11的桌面环境（GNOME, KDE, XFCE等）

## 🚀 快速开始

### 1. 系统依赖安装

```bash
# Ubuntu/Debian系统
sudo apt update
sudo apt install python3-pip python3-tk python3-gi libgirepository1.0-dev pkg-config

# CentOS/RHEL系统  
sudo yum install python3-pip python3-tkinter gobject-introspection-devel pkg-config

# Arch Linux
sudo pacman -S python-pip tk python-gobject
```

### 2. 一键系统安装（推荐）

```bash
# 下载项目
git clone https://github.com/radical2333/countdown-timer.git
cd countdown-timer

# 系统级安装（需要sudo权限）
sudo bash install.sh
```

安装完成后，您可以：
- 在应用菜单中找到"倒计时提醒器"
- 直接运行命令：`countdown-timer`（全局启动器）
- 或运行：`/opt/countdown-timer/countdown_timer.py`

### 3. 开发者模式安装

如果您想在本地开发或测试：

```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 直接运行
python3 countdown_timer.py
```

## 📖 使用说明

### 基本操作

1. **设置时间**: 在"设置倒计时时间"区域输入小时、分钟、秒
2. **设置提醒**: 在"提醒内容"框中输入自定义提醒文字
3. **开始倒计时**: 点击"开始倒计时"按钮
4. **暂停/继续**: 倒计时中点击"暂停"可暂停，点击"继续"恢复
5. **停止**: 点击"停止"按钮立即停止倒计时
6. **重置**: 点击"重置"按钮重置为初始状态

### 高级功能

- **预设时间**: 使用菜单"设置" → "预设时间"快速设置常用时间
- **系统托盘**: 点击菜单"文件" → "最小化到托盘"可后台运行
- **托盘控制**: 右键托盘图标可进行基本操作
- **防误关**: 关闭窗口时会询问是否最小化到托盘

### 快捷预设

- 5分钟、10分钟、15分钟
- 25分钟（番茄工作法）
- 30分钟、45分钟、1小时

## 🔧 故障排除

### 系统托盘不显示

```bash
# 检查托盘支持
ps aux | grep "indicator"

# 安装额外依赖
sudo apt install gir1.2-appindicator3-0.1

# 重启桌面环境或重新登录
```

### 图形界面无法启动

```bash
# 检查DISPLAY变量
echo $DISPLAY

# 检查X11权限
xhost +local:

# 安装Tkinter
sudo apt install python3-tk
```

### 声音提醒无声

```bash
# 检查音频系统
pulseaudio --check -v

# 安装音频工具
sudo apt install pulseaudio-utils alsa-utils
```

## �️ 卸载程序

如果您通过系统安装方式安装了程序，可以使用卸载脚本完全移除：

```bash
# 运行卸载脚本
sudo bash uninstall.sh
```

卸载脚本将：
- 移除 `/opt/countdown-timer/` 目录及所有文件
- 删除桌面菜单项
- 更新系统桌面数据库
- 清理相关缓存

> 注意：Python依赖包将保留在系统中，如需手动清理可运行：
> `pip3 uninstall pystray Pillow PyGObject`

## �📁 项目结构

```
countdown-timer/
├── countdown_timer.py      # 主程序文件
├── requirements.txt        # Python依赖清单
├── install.sh             # 系统安装脚本
├── uninstall.sh           # 卸载脚本
├── launcher.sh            # 全局启动器脚本
├── create_icon.py         # 图标生成脚本
├── icon.png              # 应用程序图标
├── countdown-timer.desktop # 桌面菜单文件
├── README.md             # 项目说明文档
└── LICENSE               # 开源许可证
```

## 🛠️ 开发信息

- **开发语言**: Python 3.8+
- **GUI框架**: Tkinter
- **托盘库**: PySystemTray
- **图像处理**: Pillow
- **系统集成**: PyGObject

## 📝 更新日志

### v2.0 (2025-07-14)
- ✅ 重构代码架构，提升稳定性
- ✅ 优化系统托盘兼容性（支持Unity/GNOME）
- ✅ 改进提醒窗口（强制置顶，去除闪烁）
- ✅ 增强错误处理和用户提示
- ✅ 完善安装和启动脚本

### v1.0
- ✅ 基础倒计时功能
- ✅ 图形用户界面
- ✅ 系统托盘支持

## 🤝 贡献指南

欢迎提交问题报告、功能请求或代码贡献：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -am '添加新功能'`)
4. 推送到分支 (`git push origin feature/新功能`)
5. 创建 Pull Request

### 开发者工具

项目包含以下开发者工具：

- `package.sh` - 项目打包脚本，生成发布版本
- `create_icon.py` - 图标生成脚本
- `launcher.sh` - 全局启动器脚本

打包发布版本：
```bash
bash package.sh
```

## 📄 开源许可

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 💡 致谢

- 感谢 [PySystemTray](https://github.com/moses-palmer/pystray) 提供系统托盘支持
- 感谢 [Pillow](https://pillow.readthedocs.io/) 提供图像处理功能
- 感谢所有贡献者和用户的支持

---

📧 **联系方式**: 如有问题或建议，请通过 GitHub Issues 联系。

⭐ 如果这个项目对您有帮助，请考虑给它一个 Star！
