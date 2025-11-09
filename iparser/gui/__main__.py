"""
This file is part of the Info Parser project, https://github.com/walklinewang/info-parser
The MIT License (MIT)
Copyright © 2025 Walkline Wang <walkline@gmail.com>
"""
import sys
import tkinter as tk

from iparser.gui.main_window import MainWindow
from iparser.logger import logger, setup_console_logging


def main():
	"""启动GUI应用的主函数"""
	setup_console_logging()

	root = tk.Tk()
	MainWindow(root)

	try:
		root.mainloop()
	except KeyboardInterrupt:
		pass
	except Exception as e:
		logger.error(f'GUI运行出错：{str(e)}')
		sys.exit(1)


if __name__ == '__main__':
	main()
