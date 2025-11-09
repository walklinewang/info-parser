"""
This file is part of the Info Parser project, https://github.com/walklinewang/info-parser
The MIT License (MIT)
Copyright © 2025 Walkline Wang <walkline@gmail.com>
"""
import sys
from pathlib import Path
from typing import List


DEFAULT_SAMPLE_FILE = 'samples.txt'

def load_samples_from_file(file_path: str = DEFAULT_SAMPLE_FILE) -> List[str]:
	"""
	从外部文件加载样本信息

	Args:
		file_path: 样本文件路径

	Returns:
		包含样本信息的列表

	Raises:
		FileNotFoundError: 当文件不存在时
		IOError: 当文件读取失败时
	"""
	samples = []

	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			for line in f:
				line = line.strip()
				if line and not line.startswith('#'):
					samples.append(line)
		return samples
	except FileNotFoundError:
		print(f'错误：样本文件 {file_path} 不存在')
		raise
	except IOError as e:
		print(f'错误：读取文件 {file_path} 失败：{str(e)}')
		raise
	except Exception as e:
		print(f'错误：处理文件 {file_path} 时发生未知错误：{str(e)}')
		raise

def resource_path(path: str) -> Path:
	"""获取一个随代码打包的文件在解压后的路径"""
	if getattr(sys, 'frozen', False):
		return Path(path)

	path_joined = Path(__file__).parent.parent / path
	return path_joined
