#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
倒计时提醒器 v2.0
作者: Radical_3
功能: 自定义倒计时时间和提醒内容的桌面应用，支持系统托盘
安装位置: /opt/countdown-timer/
"""

import tkinter as tk
from tkinter import messagebox
import threading
import queue
import math
import time
import subprocess
import sys
import os

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
    print("✅ 系统托盘功能已启用")
except Exception:
    TRAY_AVAILABLE = False
    print("💡 提示: 系统托盘功能不可用")
    print("   可能需要安装: sudo apt install python3-gi libgirepository1.0-dev")
    print("   然后运行: pip install PyGObject pystray pillow")


def current_time():
    """返回包含系统挂起时间的单调时钟（平台支持时）。"""
    if hasattr(time, "CLOCK_BOOTTIME"):
        return time.clock_gettime(time.CLOCK_BOOTTIME)
    return time.monotonic()


class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("倒计时提醒器")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # 系统托盘相关
        self.tray_icon = None
        self.tray_ready = False
        self.is_minimized_to_tray = False
        self.is_quitting = False
        
        # 防止意外关闭
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # 倒计时相关变量
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.remaining_duration = 0.0
        self.end_time = None
        self.is_running = False
        self.is_paused = False
        self.timer_after_id = None

        # pystray 的菜单回调不在 Tk 主线程中执行。
        self.ui_queue = queue.Queue()
        self.root.after(100, self.process_ui_queue)
        
        # 居中窗口
        self.center_window()
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建界面
        self.create_widgets()
        
        # 初始化系统托盘
        if TRAY_AVAILABLE:
            self.create_tray_icon()
            
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        if TRAY_AVAILABLE:
            file_menu.add_command(label="最小化到托盘", command=self.minimize_to_tray)
            file_menu.add_separator()
        
        file_menu.add_command(label="退出", command=self.quit_application)
        
        # 设置菜单
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="设置", menu=settings_menu)
        
        # 常用时间预设
        preset_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="预设时间", menu=preset_menu)
        
        preset_menu.add_command(label="5分钟", command=lambda: self.set_preset_time(0, 5, 0))
        preset_menu.add_command(label="10分钟", command=lambda: self.set_preset_time(0, 10, 0))
        preset_menu.add_command(label="15分钟", command=lambda: self.set_preset_time(0, 15, 0))
        preset_menu.add_command(label="25分钟 (番茄工作法)", command=lambda: self.set_preset_time(0, 25, 0))
        preset_menu.add_command(label="30分钟", command=lambda: self.set_preset_time(0, 30, 0))
        preset_menu.add_command(label="45分钟", command=lambda: self.set_preset_time(0, 45, 0))
        preset_menu.add_command(label="1小时", command=lambda: self.set_preset_time(1, 0, 0))
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)
        
    def set_preset_time(self, hours, minutes, seconds):
        """设置预设时间"""
        if not self.is_running:
            self.hours_var.set(str(hours))
            self.minutes_var.set(str(minutes))
            self.seconds_var.set(str(seconds))
        else:
            messagebox.showwarning("警告", "倒计时进行中，无法修改时间设置")
            
    def show_help(self):
        """显示使用说明"""
        help_text = """倒计时提醒器使用说明：

1. 设置时间：在"设置倒计时时间"区域设置小时、分钟、秒
2. 设置提醒：在"提醒内容"框中输入自定义提醒文字
3. 开始倒计时：点击"开始倒计时"按钮
4. 暂停/继续：倒计时中点击"暂停"可暂停，点击"继续"恢复
5. 停止：点击"停止"按钮立即停止倒计时
6. 重置：点击"重置"按钮重置倒计时

特殊功能：
• 最小化到托盘：程序可最小化到系统托盘后台运行
• 预设时间：使用"设置"→"预设时间"快速设置常用时间
• 防误关：关闭窗口时会询问是否最小化到托盘
• 自动弹出：倒计时结束时自动显示提醒窗口"""
        
        messagebox.showinfo("使用说明", help_text)
        
    def show_about(self):
        """显示关于信息"""
        about_text = """倒计时提醒器 v2.0

功能特性：
✓ 自定义倒计时时间和提醒内容
✓ 暂停/继续/停止/重置功能
✓ 系统托盘支持
✓ 预设常用时间
✓ 声音和视觉提醒
✓ 防误关闭保护

开发者：Radical_3
适用系统：Linux (Ubuntu, Debian, etc.)
技术栈：Python + Tkinter + PyTray

开源软件，自由使用"""
        
        messagebox.showinfo("关于倒计时提醒器", about_text)
        
    def create_widgets(self):
        """创建界面组件"""
        # 使用更安全的字体设置
        title_font = ("TkDefaultFont", 20, "bold")
        label_font = ("TkDefaultFont", 12, "bold")
        input_font = ("TkDefaultFont", 11)
        button_font = ("TkDefaultFont", 11, "bold")
        display_font = ("TkFixedFont", 32, "bold")
        
        # 标题
        title_label = tk.Label(self.root, text="倒计时提醒器", 
                              font=title_font, fg="#2c3e50")
        title_label.pack(pady=15)
        
        # 时间设置框架
        time_frame = tk.LabelFrame(self.root, text="设置倒计时时间", 
                                  font=label_font, fg="#34495e")
        time_frame.pack(pady=8, padx=20, fill="x")
        
        # 时间输入
        time_input_frame = tk.Frame(time_frame)
        time_input_frame.pack(pady=10)
        
        # 小时
        tk.Label(time_input_frame, text="小时:", font=input_font).grid(row=0, column=0, padx=5)
        self.hours_var = tk.StringVar(value="0")
        hours_spinbox = tk.Spinbox(time_input_frame, from_=0, to=23, width=5, 
                                  textvariable=self.hours_var, font=input_font)
        hours_spinbox.grid(row=0, column=1, padx=5)
        
        # 分钟
        tk.Label(time_input_frame, text="分钟:", font=input_font).grid(row=0, column=2, padx=5)
        self.minutes_var = tk.StringVar(value="5")
        minutes_spinbox = tk.Spinbox(time_input_frame, from_=0, to=59, width=5, 
                                    textvariable=self.minutes_var, font=input_font)
        minutes_spinbox.grid(row=0, column=3, padx=5)
        
        # 秒
        tk.Label(time_input_frame, text="秒:", font=input_font).grid(row=0, column=4, padx=5)
        self.seconds_var = tk.StringVar(value="0")
        seconds_spinbox = tk.Spinbox(time_input_frame, from_=0, to=59, width=5, 
                                    textvariable=self.seconds_var, font=input_font)
        seconds_spinbox.grid(row=0, column=5, padx=5)
        
        # 提醒内容框架
        message_frame = tk.LabelFrame(self.root, text="提醒内容", 
                                     font=label_font, fg="#34495e")
        message_frame.pack(pady=8, padx=20, fill="x")
        
        # 提醒内容输入
        self.message_var = tk.StringVar(value="时间到了！该休息一下了~")
        message_entry = tk.Entry(message_frame, textvariable=self.message_var, 
                                font=input_font, width=40)
        message_entry.pack(pady=10)
        
        # 显示框架
        display_frame = tk.LabelFrame(self.root, text="倒计时显示", 
                                     font=label_font, fg="#34495e")
        display_frame.pack(pady=8, padx=20, fill="x")
        
        # 倒计时显示
        self.countdown_label = tk.Label(display_frame, text="00:05:00", 
                                       font=display_font, fg="#e74c3c")
        self.countdown_label.pack(pady=15)
        
        # 状态显示
        self.status_label = tk.Label(display_frame, text="准备就绪", 
                                    font=input_font, fg="#27ae60")
        self.status_label.pack(pady=5)
        
        # 按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15, fill="x", padx=20)
        
        # 创建内部框架用于居中按钮
        button_inner_frame = tk.Frame(button_frame)
        button_inner_frame.pack(expand=True)
        
        # 开始/暂停按钮
        self.start_button = tk.Button(button_inner_frame, text="开始倒计时", 
                                     command=self.toggle_countdown, 
                                     font=button_font, 
                                     bg="#27ae60", fg="white", 
                                     width=10, height=2)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        # 停止按钮
        self.stop_button = tk.Button(button_inner_frame, text="停止", 
                                    command=self.stop_countdown, 
                                    font=button_font, 
                                    bg="#e74c3c", fg="white", 
                                    width=10, height=2, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        
        # 重置按钮
        self.reset_button = tk.Button(button_inner_frame, text="重置", 
                                     command=self.reset_countdown, 
                                     font=button_font, 
                                     bg="#f39c12", fg="white", 
                                     width=10, height=2)
        self.reset_button.grid(row=0, column=2, padx=5, pady=5)
        
    def format_time(self, seconds):
        """将秒数格式化为时:分:秒"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def get_configured_seconds(self):
        """读取并校验时间输入。"""
        hours = int(self.hours_var.get())
        minutes = int(self.minutes_var.get())
        seconds = int(self.seconds_var.get())
        if not 0 <= hours <= 23 or not 0 <= minutes <= 59 or not 0 <= seconds <= 59:
            raise ValueError
        return hours * 3600 + minutes * 60 + seconds
        
    def toggle_countdown(self):
        """开始/暂停倒计时切换"""
        if not self.is_running:
            self.start_countdown()
        else:
            if self.is_paused:
                self.resume_countdown()
            else:
                self.pause_countdown()
                
    def start_countdown(self):
        """开始倒计时"""
        try:
            if self.remaining_duration <= 0:
                self.total_seconds = self.get_configured_seconds()
                
                if self.total_seconds <= 0:
                    messagebox.showwarning("警告", "请设置一个有效的倒计时时间！")
                    return
                    
                self.remaining_duration = float(self.total_seconds)
                self.remaining_seconds = self.total_seconds
            
            self.is_running = True
            self.is_paused = False
            self.end_time = current_time() + self.remaining_duration
            
            # 更新按钮状态
            self.start_button.config(text="暂停", bg="#f39c12")
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="倒计时进行中...", fg="#e67e22")
            
            self.update_display()
            self.schedule_countdown_tick()
                
        except ValueError:
            messagebox.showerror("错误", "请输入有效时间：小时 0-23，分钟和秒 0-59。")
            
    def pause_countdown(self):
        """暂停倒计时"""
        self.sync_remaining_time()
        if self.remaining_duration <= 0:
            self.countdown_finished()
            return
        self.is_paused = True
        self.end_time = None
        self.cancel_countdown_tick()
        self.start_button.config(text="继续", bg="#3498db")
        self.status_label.config(text="已暂停", fg="#f39c12")
        
    def resume_countdown(self):
        """继续倒计时"""
        if self.remaining_duration <= 0:
            return
        self.is_paused = False
        self.end_time = current_time() + self.remaining_duration
        self.start_button.config(text="暂停", bg="#f39c12")
        self.status_label.config(text="倒计时进行中...", fg="#e67e22")
        self.schedule_countdown_tick()

    def schedule_countdown_tick(self):
        """在 Tk 主线程中安排下一次计时。"""
        if self.timer_after_id is None and self.is_running and not self.is_paused:
            remaining = max(0.0, self.end_time - current_time())
            displayed_seconds = math.ceil(remaining)
            delay = remaining - max(0, displayed_seconds - 1)
            delay_ms = max(10, math.ceil(delay * 1000))
            self.timer_after_id = self.root.after(delay_ms, self.countdown_tick)

    def cancel_countdown_tick(self):
        """取消尚未执行的计时，避免停止或重置后继续减秒。"""
        if self.timer_after_id is not None:
            self.root.after_cancel(self.timer_after_id)
            self.timer_after_id = None

    def countdown_tick(self):
        """执行一次倒计时。"""
        self.timer_after_id = None
        if not self.is_running or self.is_paused:
            return

        self.sync_remaining_time()
        self.update_display()
        if self.remaining_duration <= 0:
            self.countdown_finished()
        else:
            self.schedule_countdown_tick()

    def sync_remaining_time(self):
        """根据单调时钟同步剩余时间，避免休眠或界面卡顿造成漂移。"""
        if self.end_time is None:
            return
        self.remaining_duration = max(0.0, self.end_time - current_time())
        self.remaining_seconds = math.ceil(self.remaining_duration)
            
    def update_display(self):
        """更新倒计时显示"""
        time_str = self.format_time(self.remaining_seconds)
        self.countdown_label.config(text=time_str)
        
        # 最后10秒时变红色
        if self.remaining_seconds <= 10:
            self.countdown_label.config(fg="#e74c3c")
        else:
            self.countdown_label.config(fg="#2c3e50")
            
        # 更新托盘提示
        self.update_tray_tooltip()
            
    def countdown_finished(self):
        """倒计时结束处理"""
        self.is_running = False
        self.is_paused = False
        self.remaining_duration = 0.0
        self.end_time = None
        self.timer_after_id = None
        self.countdown_label.config(text="00:00:00", fg="#e74c3c")
        self.status_label.config(text="时间到！", fg="#e74c3c")
        
        # 恢复按钮状态
        self.start_button.config(text="开始倒计时", bg="#27ae60")
        self.stop_button.config(state=tk.DISABLED)
        
        # 如果窗口被最小化到托盘，自动显示窗口
        if self.is_minimized_to_tray:
            self.show_window()
            
        # 显示提醒
        self.show_notification()
        
        # 更新托盘提示
        self.update_tray_tooltip()
        
    def show_notification(self):
        """显示提醒通知"""
        message = self.message_var.get()
        
        # 创建提醒窗口
        notification_window = tk.Toplevel(self.root)
        notification_window.title("时间到了！")
        notification_window.geometry("400x200")
        notification_window.resizable(False, False)
        
        # 设置窗口置顶
        notification_window.transient(self.root)
        notification_window.grab_set()
        notification_window.focus_set()
        notification_window.attributes('-topmost', True)  # 强制置顶
        notification_window.lift()  # 提升到最前面
        
        # 居中通知窗口
        x = (notification_window.winfo_screenwidth() // 2) - 200
        y = (notification_window.winfo_screenheight() // 2) - 100
        notification_window.geometry(f"400x200+{x}+{y}")
        
        # 使用安全的字体
        try:
            icon_font = ("TkDefaultFont", 48)
            msg_font = ("TkDefaultFont", 14, "bold")
            btn_font = ("TkDefaultFont", 12, "bold")
        except:
            icon_font = None
            msg_font = None
            btn_font = None
        
        # 通知内容
        tk.Label(notification_window, text="⏰", font=icon_font).pack(pady=20)
        tk.Label(notification_window, text=message, 
                font=msg_font, fg="#e74c3c", 
                wraplength=350).pack(pady=10)
        
        # 确定按钮
        tk.Button(notification_window, text="知道了", 
                 command=notification_window.destroy, 
                 font=btn_font, 
                 bg="#3498db", fg="white", 
                 width=10).pack(pady=20)
        
        # 播放提示音，避免外部音频命令阻塞 Tk 主线程。
        self.play_notification_sound()
        
        # 强制获取焦点
        notification_window.after(100, lambda: self.focus_notification(notification_window))

    @staticmethod
    def focus_notification(window):
        try:
            if window.winfo_exists():
                window.focus_force()
        except tk.TclError:
            pass
        
    def play_notification_sound(self):
        """播放提示音"""
        threading.Thread(target=self._play_notification_sound, daemon=True).start()

    @staticmethod
    def _play_notification_sound():
        """在后台尝试可用的声音播放器。"""
        sound_file = "/usr/share/sounds/alsa/Front_Left.wav"
        commands = (["paplay", sound_file], ["aplay", sound_file], ["beep"])
        for command in commands:
            try:
                result = subprocess.run(command, check=False, capture_output=True, timeout=5)
                if result.returncode == 0:
                    return
            except (OSError, subprocess.TimeoutExpired):
                continue
        print("\a")
                    
    def flash_window(self, window):
        """使窗口闪烁"""
        def toggle_color():
            current_bg = window.cget('bg')
            new_bg = '#ffcccc' if current_bg == window.master.cget('bg') else window.master.cget('bg')
            window.config(bg=new_bg)
            
        # 闪烁5次
        for i in range(10):
            window.after(i * 300, toggle_color)
            
    def stop_countdown(self):
        """停止倒计时"""
        self.sync_remaining_time()
        self.is_running = False
        self.is_paused = False
        self.end_time = None
        self.cancel_countdown_tick()
        self.start_button.config(text="开始倒计时", bg="#27ae60")
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="已停止", fg="#e74c3c")
        
    def reset_countdown(self):
        """重置倒计时"""
        self.is_running = False
        self.is_paused = False
        self.cancel_countdown_tick()
        self.remaining_duration = 0.0
        self.remaining_seconds = 0
        try:
            display_text = self.format_time(self.get_configured_seconds())
        except ValueError:
            display_text = "00:00:00"
        self.countdown_label.config(text=display_text, fg="#2c3e50")
        self.start_button.config(text="开始倒计时", bg="#27ae60")
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="准备就绪", fg="#27ae60")
        
        
    def create_tray_icon(self):
        """创建系统托盘图标"""
        if not TRAY_AVAILABLE:
            return
            
        try:
            # 创建一个简单的图标
            image = Image.new('RGB', (64, 64), color='white')
            draw = ImageDraw.Draw(image)
            
            # 绘制时钟图标
            draw.ellipse([8, 8, 56, 56], fill='#3498db', outline='#2c3e50', width=3)
            draw.line([32, 20, 32, 32], fill='#2c3e50', width=3)  # 时针
            draw.line([32, 32, 42, 32], fill='#2c3e50', width=2)  # 分针
            draw.ellipse([30, 30, 34, 34], fill='#2c3e50')  # 中心点
            
            # 创建托盘菜单
            menu = pystray.Menu(
                pystray.MenuItem("显示主窗口", self.tray_show_window),
                pystray.MenuItem("开始倒计时", self.tray_start_countdown),
                pystray.MenuItem("停止倒计时", self.tray_stop_countdown),
                pystray.MenuItem("重置倒计时", self.tray_reset_countdown),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("退出程序", self.tray_quit_application)
            )
            
            # 创建托盘图标
            self.tray_icon = pystray.Icon(
                "countdown_timer",
                image,
                "倒计时提醒器",
                menu
            )
            
            # 在单独线程中运行托盘
            tray_thread = threading.Thread(target=self._run_tray_safe, daemon=True)
            tray_thread.start()
            
        except Exception as e:
            print(f"创建系统托盘失败: {e}")
            self.tray_icon = None
            
    def _run_tray_safe(self):
        """安全运行系统托盘"""
        try:
            if self.tray_icon:
                self.tray_icon.run(setup=self._setup_tray_safe)
                if not self.is_quitting:
                    self.ui_queue.put(lambda: self.handle_tray_failure("托盘服务已停止"))
        except Exception as e:
            print(f"❌ 托盘运行错误: {e}")
            print("💡 可能的原因:")
            print("   1. 系统托盘管理器未运行")
            print("   2. 桌面环境不支持托盘")
            print("   3. 需要重新登录桌面环境")
            self.ui_queue.put(
                lambda message=str(e): self.handle_tray_failure(message)
            )

    def _setup_tray_safe(self, icon):
        """等待后端就绪后再允许窗口隐藏到托盘。"""
        try:
            icon.visible = True
            self.ui_queue.put(self.mark_tray_ready)
        except Exception as e:
            self.ui_queue.put(
                lambda message=str(e): self.handle_tray_failure(message)
            )

    def mark_tray_ready(self):
        self.tray_ready = True

    def handle_tray_failure(self, message):
        """在 Tk 主线程恢复可能已隐藏的窗口。"""
        if self.is_quitting:
            return
        print(f"系统托盘不可用: {message}")
        self.tray_ready = False
        self.tray_icon = None
        if self.is_minimized_to_tray:
            self.show_window()
            messagebox.showwarning("系统托盘不可用", "托盘启动失败，主窗口已恢复。")
            
    def on_window_close(self):
        """处理窗口关闭事件"""
        if self.is_running:
            # 如果倒计时正在进行，询问用户
            result = messagebox.askyesnocancel(
                "倒计时提醒器", 
                "倒计时正在进行中，是否要：\n\n"
                "• 点击'是'：最小化到系统托盘继续运行\n"
                "• 点击'否'：停止倒计时并退出程序\n"
                "• 点击'取消'：返回程序"
            )
            if result is True:  # 最小化到托盘
                self.minimize_to_tray()
            elif result is False:  # 退出程序
                self.quit_application()
            # result is None: 取消，不做任何操作
        else:
            # 如果没有倒计时，询问是否最小化到托盘
            if TRAY_AVAILABLE:
                result = messagebox.askyesno(
                    "倒计时提醒器",
                    "是否最小化到系统托盘？\n\n点击'否'将完全退出程序。"
                )
                if result:
                    self.minimize_to_tray()
                else:
                    self.quit_application()
            else:
                self.quit_application()
                
    def minimize_to_tray(self):
        """最小化到系统托盘"""
        if TRAY_AVAILABLE and self.tray_icon and self.tray_ready:
            self.root.withdraw()  # 隐藏主窗口
            self.is_minimized_to_tray = True
            self.update_tray_tooltip()
        else:
            messagebox.showinfo("提示", "系统托盘尚未就绪，程序将最小化到任务栏")
            self.root.iconify()
            
    def show_window(self, icon=None, item=None):
        """显示主窗口"""
        self.root.deiconify()  # 恢复窗口
        self.root.lift()       # 置顶
        self.root.focus_force() # 获取焦点
        self.is_minimized_to_tray = False

    def process_ui_queue(self):
        """在 Tk 主线程中执行来自托盘线程的操作。"""
        try:
            while True:
                callback = self.ui_queue.get_nowait()
                callback()
                if self.is_quitting:
                    return
        except queue.Empty:
            pass

        try:
            self.root.after(100, self.process_ui_queue)
        except tk.TclError:
            pass
        
    def update_tray_tooltip(self):
        """更新托盘图标提示文字"""
        if self.tray_icon and TRAY_AVAILABLE:
            if self.is_running:
                time_str = self.format_time(self.remaining_seconds)
                if self.is_paused:
                    tooltip = f"倒计时提醒器 - 已暂停 {time_str}"
                else:
                    tooltip = f"倒计时提醒器 - 剩余 {time_str}"
            else:
                tooltip = "倒计时提醒器 - 准备就绪"
            self.tray_icon.title = tooltip
            
    def tray_start_countdown(self, icon=None, item=None):
        """从托盘开始倒计时"""
        self.ui_queue.put(self.start_countdown_from_tray)

    def start_countdown_from_tray(self):
        if not self.is_running:
            self.start_countdown()
            
    def tray_stop_countdown(self, icon=None, item=None):
        """从托盘停止倒计时"""
        self.ui_queue.put(self.stop_countdown_from_tray)

    def stop_countdown_from_tray(self):
        if self.is_running:
            self.stop_countdown()
            
    def tray_reset_countdown(self, icon=None, item=None):
        """从托盘重置倒计时"""
        self.ui_queue.put(self.reset_countdown)

    def tray_show_window(self, icon=None, item=None):
        self.ui_queue.put(self.show_window)

    def tray_quit_application(self, icon=None, item=None):
        self.ui_queue.put(self.quit_application)
        
    def quit_application(self, icon=None, item=None):
        """完全退出应用程序"""
        self.is_running = False
        self.is_quitting = True
        self.tray_ready = False
        self.cancel_countdown_tick()
        if self.tray_icon and TRAY_AVAILABLE:
            self.tray_icon.stop()
        self.root.quit()
        self.root.destroy()

def main():
    """主函数"""
    # 检查图形环境
    try:
        # 检查DISPLAY环境变量
        if not os.environ.get('DISPLAY') and not os.environ.get('WAYLAND_DISPLAY'):
            print("❌ 错误: 未检测到图形环境")
            print("💡 请在桌面环境中运行此程序")
            return 1
            
        root = tk.Tk()
        
        # 设置基本属性避免字体问题
        root.option_add('*Font', 'TkDefaultFont')
        
    except Exception as e:
        print(f"❌ 图形界面初始化失败: {e}")
        print("💡 可能的解决方案:")
        print("1. 检查是否安装了 python3-tk: sudo apt install python3-tk")
        print("2. 检查X11转发是否正常")
        print("3. 确认当前终端可以启动图形应用")
        return 1
    
    try:
        app = CountdownTimer(root)
        
        # 设置窗口图标（如果有的话）
        try:
            root.iconbitmap('timer.ico')
        except:
            pass
        
        # 窗口关闭处理已在CountdownTimer.__init__中设置
        
        # 启动主循环
        root.mainloop()
        return 0
        
    except Exception as e:
        print(f"❌ 程序运行错误: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
