"""
This file is part of the Info Parser project, https://github.com/walklinewang/info-parser
The MIT License (MIT)
Copyright © 2025 Walkline Wang <walkline@gmail.com>
"""
import sys
import tkinter as tk

from ..logger import setup_console_logging, logger
from .main_window import MainWindow


def main():
	"""启动GUI应用的主函数"""
	setup_console_logging()
	logger.info("启动信息解析工具GUI...")

	root = tk.Tk()
	MainWindow(root)

	try:
		# sv_ttk.set_theme("light")
		root.mainloop()
	except KeyboardInterrupt:
		logger.info("用户中断程序")
	except Exception as e:
		logger.error(f"GUI运行出错: {str(e)}")
		sys.exit(1)
	finally:
		logger.info("程序已退出")


if __name__ == "__main__":
	main()
