"""
This file is part of the Info Parser project, https://github.com/walklinewang/info-parser
The MIT License (MIT)
Copyright © 2025 Walkline Wang <walkline@gmail.com>
"""
import json
from pathlib import Path
from typing import Optional, Dict, Set, List

import tkinter as tk
from tkinter import ttk, messagebox

from ..__main__ import Applicant
from ..utils import update_jieba_keywords
from ..config import config
from .clipboard_monitor import ClipboardMonitor
from ..logger import logger


class MainWindow:
	"""
	主窗口类，实现剪贴板监听与解析工具的GUI界面
	"""
	def __init__(self, root: tk.Tk):
		"""
		初始化主窗口

		Args:
			root: tkinter根窗口
		"""
		self.root = root
		self.root.title("信息解析工具")
		self.root.geometry("350x167")
		self.root.resizable(False, False)
		self.root.protocol("WM_DELETE_WINDOW", self.on_close)
		self.root.attributes("-topmost", True)

		# 剪贴板监控状态
		self.monitoring_enabled = tk.BooleanVar(value=False)

		# 配置区域显示状态
		self.config_visible = tk.BooleanVar(value=False)

		# 自定义配置文件路径
		self.custom_config_file = Path(__file__).parent.parent.parent / "custom_config.json"

		# 初始化剪贴板监控器，传递主窗口的root
		self.clipboard_monitor = ClipboardMonitor(self.on_clipboard_change, root=self.root)

		# 创建自定义样式，为只读输入框设置灰色背景
		style = ttk.Style()
		style.configure("readonly.TEntry", fieldbackground="#000000")

		self.create_ui()
		self.load_custom_config()
		self.setup_layout()

	def create_ui(self):
		"""创建用户界面组件"""
		# 创建主框架
		self.main_frame = ttk.Frame(self.root, padding=(10, 0))
		self.main_frame.pack(fill=tk.BOTH, expand=True)

		self.create_control_area()
		self.create_display_area()
		self.create_config_area()

	def create_control_area(self):
		"""创建控制区域，包含开关和配置显示切换按钮"""
		control_frame = ttk.Frame(self.main_frame)
		control_frame.pack(fill=tk.X, pady=(5, 10))

		# 监听按钮
		self.monitor_button = ttk.Button(
			control_frame, 
			text="开始监听", 
			command=self.toggle_monitoring,
			width=10
		)
		self.monitor_button.pack(side=tk.LEFT, padx=5)

		# 配置显示切换按钮
		self.config_toggle_button = ttk.Button(
			control_frame,
			text="显示配置",
			command=self.toggle_config_visibility,
			width=10
		)
		self.config_toggle_button.pack(side=tk.LEFT, padx=5)

	def create_display_area(self):
		"""创建内容显示区域，包含原始内容、拆分结果和解析结果输入框"""
		display_frame = ttk.LabelFrame(self.main_frame, text="内容显示", padding="5")
		display_frame.pack(fill=tk.X, pady=(0, 10))

		# 原始内容
		original_frame = ttk.Frame(display_frame)
		original_frame.pack(fill=tk.X, pady=(0, 5))

		ttk.Label(original_frame, text="原始内容: ").pack(side=tk.LEFT, padx=5)
		self.original_entry = ttk.Entry(original_frame, width=20, state="readonly", style="readonly.TEntry")
		self.original_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=5)

		# 拆分结果
		split_frame = ttk.Frame(display_frame)
		split_frame.pack(fill=tk.X, pady=(0, 5))

		ttk.Label(split_frame, text="拆分结果: ").pack(side=tk.LEFT, padx=5)
		self.split_entry = ttk.Entry(split_frame, width=20, state="readonly", style="readonly.TEntry")
		self.split_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=5)

		# 解析结果
		result_frame = ttk.Frame(display_frame)
		result_frame.pack(fill=tk.X, pady=(0, 5))

		ttk.Label(result_frame, text="解析结果: ").pack(side=tk.LEFT, padx=5)
		self.result_entry = ttk.Entry(result_frame, width=20)
		self.result_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=5)

	def create_config_area(self):
		"""创建配置区域，包含机构简称和干扰词输入框以及操作按钮"""
		self.config_frame = ttk.LabelFrame(self.main_frame, text="自定义配置", padding="5")

		# 配置内容区域（左右布局）
		config_content_frame = ttk.Frame(self.config_frame)
		config_content_frame.pack(fill=tk.BOTH, expand=True)

		# 左侧：机构简称
		short_names_frame = ttk.LabelFrame(config_content_frame, text="机构简称", padding="5")
		short_names_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

		self.short_names_text = tk.Text(short_names_frame, height=6, wrap=tk.WORD)
		self.short_names_text.pack(fill=tk.BOTH, expand=True)

		# 添加滚动条
		short_names_scrollbar = ttk.Scrollbar(self.short_names_text, command=self.short_names_text.yview)
		short_names_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.short_names_text.config(yscrollcommand=short_names_scrollbar.set)

		# 右侧：干扰词
		excluded_words_frame = ttk.LabelFrame(config_content_frame, text="干扰词", padding="5")
		excluded_words_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

		self.excluded_words_text = tk.Text(excluded_words_frame, height=6, wrap=tk.WORD)
		self.excluded_words_text.pack(fill=tk.BOTH, expand=True)

		# 添加滚动条
		excluded_words_scrollbar = ttk.Scrollbar(self.excluded_words_text, command=self.excluded_words_text.yview)
		excluded_words_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.excluded_words_text.config(yscrollcommand=excluded_words_scrollbar.set)

		# 按钮区域
		buttons_frame = ttk.Frame(self.config_frame)
		buttons_frame.pack(fill=tk.X, pady=5)

		self.save_button = ttk.Button(buttons_frame, text="保存", command=self.save_custom_config)
		self.save_button.pack(side=tk.RIGHT, padx=5)

		# 示例说明标签
		example_label = ttk.Label(
			self.config_frame,
			text="注：每行输入一个关键词",
			font=(None, 8),
			foreground="gray"
		)
		example_label.pack(side=tk.RIGHT, padx=5)

	def setup_layout(self):
		"""设置窗口布局，配置列和行的权重"""
		# 配置主窗口的网格权重
		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_rowconfigure(0, weight=1)

		# 配置主框架的网格权重
		self.main_frame.grid_columnconfigure(0, weight=1)
		self.main_frame.grid_rowconfigure(0, weight=0)  # 控制区域
		self.main_frame.grid_rowconfigure(1, weight=0)  # 显示区域（不扩展高度）
		self.main_frame.grid_rowconfigure(2, weight=0)  # 配置区域

		# 初始显示配置区域
		if self.config_visible.get():
			self.config_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
		else:
			self.config_frame.pack_forget()

	def toggle_config_visibility(self):
		"""切换配置区域的显示与隐藏状态，并自动调整窗口尺寸"""
		if not self.config_visible.get():
			# 显示配置区域
			self.config_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
			self.config_toggle_button.config(text="隐藏配置")
			self.config_visible.set(True)
			self.root.after(0, self.__resize_window_for_content)
		else:
			# 隐藏配置区域
			self.config_frame.pack_forget()
			self.config_toggle_button.config(text="显示配置")
			self.config_visible.set(False)
			self.root.after(0, self.__resize_window_for_content)

	def __resize_window_for_content(self):
		"""根据内容自动调整窗口尺寸，确保平滑无闪烁"""
		# 更新所有组件的尺寸
		self.root.update_idletasks()

		# 获取当前窗口位置
		x = self.root.winfo_x()
		y = self.root.winfo_y()

		# 根据配置区域显示状态设置固定窗口大小
		if self.config_visible.get():
			# 显示配置区域时，设置较大的固定尺寸
			self.root.geometry(f"350x410+{x}+{y}")
		else:
			# 隐藏配置区域时，设置较小的固定尺寸
			self.root.geometry(f"350x167+{x}+{y}")

		# 强制刷新以确保尺寸正确应用
		self.root.update_idletasks()

	def toggle_monitoring(self):
		"""切换剪贴板监听状态"""
		if not self.monitoring_enabled.get():
			# 开启监听
			self.clipboard_monitor.clear_clipboard()
			self.clipboard_monitor.start()
			self.monitor_button.config(text="停止监听", style="Accent.TButton")
			self.monitoring_enabled.set(True)
			logger.info("已启用剪贴板监听")
		else:
			# 关闭监听
			self.clipboard_monitor.stop()
			self.monitor_button.config(text="开始监听", style="")
			self.monitoring_enabled.set(False)
			logger.info("已禁用剪贴板监听")

	def on_clipboard_change(self, content: str):
		"""
		剪贴板内容变化时的回调函数

		Args:
			content: 新的剪贴板内容
		"""
		logger.debug(f"检测到剪贴板变化: {content}")

		# 更新原始内容输入框（临时允许编辑）
		self.root.after(0, lambda: self.original_entry.config(state="normal", style="TEntry"))
		self.root.after(0, lambda: self.original_entry.delete(0, tk.END))
		self.root.after(0, lambda: self.original_entry.insert(0, content))
		self.root.after(0, lambda: self.original_entry.config(state="readonly", style="readonly.TEntry"))

		# 解析内容
		try:
			applicant = Applicant(content)
			applicant.parse()
			result = applicant.full_info
			split_result = applicant.split_result

			# 更新分割结果输入框
			self.root.after(0, lambda: self.split_entry.config(state="normal", style="TEntry"))
			self.root.after(0, lambda: self.split_entry.delete(0, tk.END))
			self.root.after(0, lambda: self.split_entry.insert(0, ', '.join(split_result)))
			self.root.after(0, lambda: self.split_entry.config(state="readonly", style="readonly.TEntry"))	

			# 更新解析结果输入框
			self.root.after(0, lambda: self.result_entry.delete(0, tk.END))
			self.root.after(0, lambda: self.result_entry.insert(0, result))

			# 复制解析结果到剪贴板
			self.clipboard_monitor.set_last_parsed(result)
			self.clipboard_monitor.set_clipboard_content(result)

			logger.info(f"解析成功: {result}")
		except Exception as e:
			error_msg = f"解析失败: {str(e)}"
			self.root.after(0, lambda: self.result_entry.delete(0, tk.END))
			self.root.after(0, lambda: self.result_entry.insert(0, error_msg))

			# 复制原始内容到剪贴板
			self.clipboard_monitor.set_clipboard_content(content)

			logger.error(error_msg)

	def __refresh_keywords(self):
		"""
		刷新关键词配置，更新jieba分词器
		"""
		try:
			# 获取用户输入的配置
			shortened_names = self.get_shortened_names()
			excluded_keywords = self.get_excluded_keywords()

			# 更新配置
			config.institution.add_shortened_names(shortened_names)
			config.institution.add_excluded_keywords(excluded_keywords)

			update_jieba_keywords()

			# messagebox.showinfo("成功", "关键词配置已刷新")
			logger.info("已刷新关键词配置")

			# 如果当前有原始内容，重新解析
			# original_content = self.original_entry.get()
			# if original_content:
			# 	self.on_clipboard_change(original_content)

		except Exception as e:
			messagebox.showerror("错误", f"刷新配置失败: {str(e)}")
			logger.error(f"刷新配置失败: {str(e)}")

	def save_custom_config(self):
		"""保存自定义配置到JSON文件"""
		try:
			config_data = {
				"shortened_names": self.get_shortened_names(),
				"excluded_keywords": self.get_excluded_keywords()
			}

			with open(self.custom_config_file, 'w', encoding='utf-8') as f:
				json.dump(config_data, f, ensure_ascii=False, indent=4)

			self.__refresh_keywords()
			# messagebox.showinfo("成功", f"配置已保存到 {self.custom_config_file}")
			logger.info(f"已保存配置到 {self.custom_config_file}")

		except Exception as e:
			messagebox.showerror("错误", f"保存配置失败: {str(e)}")
			logger.error(f"保存配置失败: {str(e)}")

	def load_custom_config(self):
		"""从JSON文件加载自定义配置"""
		try:
			if self.custom_config_file.exists():
				with open(self.custom_config_file, 'r', encoding='utf-8') as f:
					config_data = json.load(f)

				# 加载机构简称
				if "shortened_names" in config_data:
					self.set_shortened_names(config_data["shortened_names"])

				# 加载干扰词
				if "excluded_keywords" in config_data:
					self.set_excluded_keywords(config_data["excluded_keywords"])

				self.__refresh_keywords()

				logger.info(f"已加载自定义配置: {self.custom_config_file}")

		except Exception as e:
			logger.error(f"加载自定义配置失败: {str(e)}")
			messagebox.showwarning("警告", f"加载配置失败: {str(e)}")

	def get_shortened_names(self) -> List[str]:
		"""
		获取用户输入的机构简称

		Returns:
			机构简称列表
		"""
		content = self.short_names_text.get("1.0", tk.END)
		return [line.strip() for line in content.splitlines() if line.strip()]

	def set_shortened_names(self, names: List[str]):
		"""
		设置机构简称文本框内容

		Args:
			names: 机构简称列表
		"""
		self.short_names_text.delete("1.0", tk.END)
		for name in names:
			self.short_names_text.insert(tk.END, name + "\n")

	def get_excluded_keywords(self) -> List[str]:
		"""
		获取用户输入的干扰词

		Returns:
			干扰词列表
		"""
		content = self.excluded_words_text.get("1.0", tk.END)
		return [line.strip() for line in content.splitlines() if line.strip()]

	def set_excluded_keywords(self, excluded_keywords: List[str]):
		"""
		设置干扰词文本框内容

		Args:
			excluded_keywords: 干扰词列表
		"""
		self.excluded_words_text.delete("1.0", tk.END)
		for word in excluded_keywords:
			self.excluded_words_text.insert(tk.END, word + "\n")

	def on_close(self):
		"""窗口关闭时的处理"""
		self.clipboard_monitor.stop()
		self.root.destroy()
