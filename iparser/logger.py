"""
This file is part of the Info Parser project, https://github.com/walklinewang/info-parser
The MIT License (MIT)
Copyright © 2025 Walkline Wang <walkline@gmail.com>
"""
import logging


logger = logging.getLogger(__name__)

def setup_logging():
	"""
	配置日志系统

	设置日志级别、处理器和格式化器，确保日志能正确写入文件并具有适当的格式。
	日志级别设为DEBUG，会捕获所有级别的日志信息。

	Returns:
		配置好的logger对象
	"""
	logger.setLevel(logging.DEBUG)

	# 清除已有的处理器
	for handler in logger.handlers:
		logger.removeHandler(handler)

	# 创建文件处理器
	file_handler = logging.FileHandler('iparser.log', encoding='utf-8')
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(
		logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S')
	)
	logger.addHandler(file_handler)

def setup_console_logging():
	"""配置控制台日志输出"""
	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.INFO)
	console_handler.setFormatter(logging.Formatter('%(message)s'))
	logger.addHandler(console_handler)

setup_logging()
