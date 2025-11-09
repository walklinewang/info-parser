#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复Python文件中的空行缩进问题

用法:
  python fix_indentation.py          # 处理当前目录及其子目录下所有Python文件
  python fix_indentation.py <folder> # 处理指定目录及其子目录下所有Python文件
  python fix_indentation.py <file>   # 处理单个Python文件
"""
import argparse
import re
from pathlib import Path
from typing import List


def fix_indentation_in_file(file_path) -> bool:
	"""
	修复指定文件中的空行缩进

	Args:
		file_path: 文件路径
	"""
	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			content = f.read()

		# 使用正则表达式移除所有缩进字符（包括制表符和空格）
		new_content = re.sub(r'^[ \t]+(?=\r?\n|$)', '', content, flags=re.MULTILINE)

		with open(file_path, 'w', encoding='utf-8') as f:
			f.write(new_content)

		print(f'已修复 {file_path} 中的空行缩进')
		return True
	except Exception as e:
		print(f'修复 {file_path} 失败：{str(e)}')
		return False

def find_python_files(directory) -> List[str]:
	"""
	递归查找目录下所有Python文件，排除虚拟环境目录

	Args:
		directory: 要搜索的目录路径

	Returns:
		包含所有Python文件路径的列表
	"""
	py_files = []
	dir_path = Path(directory)

	for path in dir_path.rglob('*.py'):
		if '.venv' not in str(path.parent):
			py_files.append(str(path))
	return py_files

def main():
	"""主函数，解析命令行参数并处理指定的文件或目录"""
	parser = argparse.ArgumentParser(description='修复Python文件中的空行缩进问题')
	parser.add_argument('path', nargs='?', default='.', help='要处理的文件或目录路径（默认：当前目录）')
	args = parser.parse_args()

	py_files = []
	path_obj = Path(args.path)

	# 检查路径是否存在
	if not path_obj.exists():
		print(f'错误：路径 "{args.path}" 不存在')
		return

	# 根据路径类型处理
	if path_obj.is_file():
		# 处理单个文件
		if path_obj.suffix == '.py':
			py_files.append(str(path_obj))
		else:
			print(f'警告：文件 "{args.path}" 不是Python文件，跳过处理')
			return
	else:
		# 处理目录
		py_files = find_python_files(args.path)
		print(f'在目录 "{args.path}" 中找到 {len(py_files)} 个Python文件')

	# 处理所有找到的Python文件
	success_count = 0
	error_count = 0

	for py_file in py_files:
		if fix_indentation_in_file(py_file):
			success_count += 1
		else:
			error_count += 1

	print(f'处理完成：成功 {success_count} 个文件，失败 {error_count} 个文件')


if __name__ == '__main__':
	main()
