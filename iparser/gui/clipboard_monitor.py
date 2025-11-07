"""
This file is part of the Info Parser project, https://github.com/walklinewang/info-parser
The MIT License (MIT)
Copyright © 2025 Walkline Wang <walkline@gmail.com>
"""
import threading
import time
from typing import Callable, Optional
import queue

import tkinter as tk
from tkinter import TclError

from ..logger import logger


class ClipboardMonitor:
	"""
	剪贴板监听类

	负责监控系统剪贴板内容变化，并在检测到新内容时触发回调函数。
	使用线程安全的方式实现，避免CPU占用过高。
	"""
	def __init__(self, on_clipboard_change: Callable[[str], None], poll_interval: float = 0.5, root=None):
		"""
		初始化剪贴板监听器

		Args:
			on_clipboard_change: 剪贴板内容变化时的回调函数
			poll_interval: 轮询间隔，单位为秒，默认0.5秒
			root: tkinter根窗口，优先使用已有的根窗口
		"""
		self._on_clipboard_change = on_clipboard_change
		self._poll_interval = poll_interval
		self._running = False
		self._thread = None
		self.__last_parsed = ""
		self._lock = threading.Lock()
		self._queue = queue.Queue()

		# 使用传入的root或创建新的root
		if root is not None:
			self._root = root
		else:
			self._root = tk.Tk()
			self._root.withdraw()  # 隐藏主窗口

	def start(self):
		"""启动剪贴板监听线程"""
		with self._lock:
			if self._running:
				return

			self._running = True
			self._thread = threading.Thread(target=self.__monitor_loop, daemon=True)
			self._thread.start()
			logger.info("剪贴板监听已启动")

	def stop(self):
		"""停止剪贴板监听线程"""
		with self._lock:
			if not self._running:
				return

			self._running = False
			if self._thread:
				self._thread.join(timeout=1.0)
				self._thread = None
			logger.info("剪贴板监听已停止")

	def get_clipboard_content(self) -> Optional[str]:
		"""
		获取当前剪贴板内容

		Returns:
			剪贴板文本内容，如果获取失败返回None
		"""
		# 确保在主线程中执行剪贴板操作
		if threading.current_thread() is threading.main_thread():
			try:
				return self._root.clipboard_get()
			except TclError:
				# 剪贴板内容不是文本或为空
				return None
			except Exception as e:
				logger.error(f"获取剪贴板内容失败: {str(e)}")
				return None
		else:
			# 在非主线程中，创建临时的Tk实例
			try:
				temp_root = tk.Tk()
				temp_root.withdraw()
				content = temp_root.clipboard_get()
				temp_root.destroy()
				return content
			except TclError:
				# 剪贴板内容不是文本或为空
				return None
			except Exception as e:
				logger.error(f"获取剪贴板内容失败: {str(e)}")
				return None

	def set_clipboard_content(self, content: str):
		"""
		设置剪贴板内容

		Args:
			content: 要设置的文本内容
		"""
		# 确保在主线程中执行剪贴板操作
		if threading.current_thread() is threading.main_thread():
			try:
				self._root.clipboard_clear()
				self._root.clipboard_append(content)
				self._root.update()  # 确保剪贴板更新立即生效
			except Exception as e:
				logger.error(f"设置剪贴板内容失败: {str(e)}")
		else:
			# 在非主线程中，创建临时的Tk实例
			try:
				temp_root = tk.Tk()
				temp_root.withdraw()
				temp_root.clipboard_clear()
				temp_root.clipboard_append(content)
				temp_root.update()
				temp_root.destroy()
			except Exception as e:
				logger.error(f"设置剪贴板内容失败: {str(e)}")

	def clear_clipboard(self):
		"""
		清除剪贴板内容
		"""
		# 确保在主线程中执行剪贴板操作
		if threading.current_thread() is threading.main_thread():
			try:
				self._root.clipboard_clear()
				self._root.update()  # 确保剪贴板更新立即生效
				logger.info("剪贴板已清除")
			except Exception as e:
				logger.error(f"清除剪贴板内容失败: {str(e)}")
		else:
			# 在非主线程中，创建临时的Tk实例
			try:
				temp_root = tk.Tk()
				temp_root.withdraw()
				temp_root.clipboard_clear()
				temp_root.update()
				temp_root.destroy()
				logger.info("剪贴板已清除")
			except Exception as e:
				logger.error(f"清除剪贴板内容失败: {str(e)}")

	def __monitor_loop(self):
		"""剪贴板监听主循环"""
		while self._running:
			try:
				content = self.get_clipboard_content()

				# 检查内容是否变化且不为空
				if content and content != self.__last_parsed:
					# 将新内容放入队列
					self._queue.put(content)
					# 请求主线程处理
					if hasattr(self._root, 'after_idle'):
						self._root.after_idle(self.__process_queue)
			except Exception as e:
				logger.error(f"监听剪贴板时出错: {str(e)}")

			# 等待下一次轮询
			time.sleep(self._poll_interval)

	def set_last_parsed(self, content: str):
		"""
		设置上次解析的内容

		Args:
			content: 要设置的解析内容
		"""
		self.__last_parsed = content

	def __process_queue(self):
		"""
		处理队列中的剪贴板内容（在主线程中执行）
		"""
		while not self._queue.empty():
			try:
				content = self._queue.get_nowait()
				self._on_clipboard_change(content)
			except Exception as e:
				logger.error(f"处理剪贴板内容时出错: {str(e)}")
			finally:
				self._queue.task_done()

	def __del__(self):
		"""析构函数，确保线程停止"""
		self.stop()
		if hasattr(self, '_root'):
			try:
				self._root.destroy()
			except:
				pass
