"""
This file is part of the Info Parser project, https://github.com/walklinewang/info-parser
The MIT License (MIT)
Copyright © 2025 Walkline Wang <walkline@gmail.com>
"""
import queue
import threading
import time
import tkinter as tk
from tkinter import TclError
from typing import Callable, Optional

from iparser.logger import logger


class ClipboardMonitor:
	"""
	剪贴板监听类

	负责监控系统剪贴板内容变化，并在检测到新内容时触发回调函数。
	使用线程安全的方式实现，避免CPU占用过高。
	"""
	def __init__(self, root: tk.Tk,
		on_clipboard_change: Callable[[str], None],
		poll_interval: float = 0.3):
		"""
		初始化剪贴板监听器

		Args:
			on_clipboard_change: 剪贴板内容变化时的回调函数
			poll_interval: 轮询间隔，单位为秒，默认0.5秒
			root: tkinter根窗口，优先使用已有的根窗口
		"""
		assert root is not None, 'root不能为空'

		self.__root = root
		self.__on_clipboard_change = on_clipboard_change
		self._poll_interval = poll_interval
		self.__running = False
		self.__thread = None
		self.__last_parsed = ''
		self.__lock = threading.Lock()
		self.__queue = queue.Queue()

	def __del__(self):
		"""析构函数，确保线程停止"""
		self.stop()

		if hasattr(self, '__root'):
			try:
				self.__root.destroy()
			except Exception:
				pass

	def start(self) -> bool:
		"""启动剪贴板监听线程"""
		with self.__lock:
			if self.__running:
				return False

			self.__running = True

			if self.__thread is None or not self.__thread.is_alive():
				self.__thread = threading.Thread(target=self.monitor_loop, daemon=True)
				self.__thread.start()
				logger.debug('剪贴板监听已启动')

			return True

	def stop(self) -> bool:
		"""停止剪贴板监听线程"""
		with self.__lock:
			if not self.__running:
				return False

			self.__running = False
			if self.__thread:
				self.__thread.join(timeout=1.0)
				self.__thread = None
				logger.debug('剪贴板监听已停止')

			return True

	def get_clipboard(self) -> Optional[str | None]:
		"""
		获取当前剪贴板内容

		Returns:
			剪贴板文本内容，如果获取失败返回None
		"""
		if threading.current_thread() is threading.main_thread():
			try:
				return self.__root.clipboard_get()
			except TclError:
				# 剪贴板内容不是文本或为空
				return None
			except Exception as e:
				logger.error(f'获取剪贴板内容失败：{str(e)}')
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
				logger.error(f'获取剪贴板内容失败：{str(e)}')
				return None

	def set_clipboard(self, content: str):
		"""
		设置剪贴板内容

		Args:
			content: 要设置的剪贴板内容
		"""
		if threading.current_thread() is threading.main_thread():
			try:
				self.__root.clipboard_clear()
				self.__root.clipboard_append(content)
				self.__root.update() # 确保剪贴板更新立即生效
			except Exception as e:
				logger.error(f'设置剪贴板内容失败：{str(e)}')
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
				logger.error(f'设置剪贴板内容失败：{str(e)}')

	def clear_clipboard(self):
		"""清除剪贴板内容"""
		if threading.current_thread() is threading.main_thread():
			try:
				self.__root.clipboard_clear()
				self.__root.update()  # 确保剪贴板更新立即生效
			except Exception as e:
				logger.error(f'清除剪贴板内容失败：{str(e)}')
		else:
			# 在非主线程中，创建临时的Tk实例
			try:
				temp_root = tk.Tk()
				temp_root.withdraw()
				temp_root.clipboard_clear()
				temp_root.update()
				temp_root.destroy()
			except Exception as e:
				logger.error(f'清除剪贴板内容失败：{str(e)}')

	def monitor_loop(self):
		"""剪贴板监听主循环"""
		while self.__running:
			try:
				content = self.get_clipboard()

				# 检查内容是否变化且不为空
				with self.__lock:
					if content and content != self.__last_parsed:
						self.__queue.put(content)

						if hasattr(self.__root, 'after_idle'):
							self.__root.after_idle(self.process_queue)
			except Exception as e:
				logger.error(f'监听剪贴板时出错：{str(e)}')
			finally:
				time.sleep(self._poll_interval)

	def process_queue(self):
		"""处理队列中的剪贴板内容"""
		while not self.__queue.empty():
			try:
				content = self.__queue.get_nowait()
				self.__on_clipboard_change(content)
			except Exception as e:
				logger.error(f'处理剪贴板内容时出错：{str(e)}')
			finally:
				self.__queue.task_done()

	@property
	def last_parsed(self) -> str:
		"""获取/设置上次解析的内容"""
		return self.__last_parsed

	@last_parsed.setter
	def last_parsed(self, content: str):
		self.__last_parsed = content
