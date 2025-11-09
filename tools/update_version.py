#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新版本号脚本
从 iparser.__init__ 读取版本号，并更新 resources/version_info 中的版本信息
"""
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
IPARSER_INIT_FILE = PROJECT_ROOT / 'iparser' / '__init__.py'
VERSION_INFO_FILE = PROJECT_ROOT / 'resources' / 'version_info'

def update_version():
	"""
	更新版本号

	从 iparser.__init__ 读取版本号，并更新 resources/version_info 中的版本信息
	"""
	if not IPARSER_INIT_FILE.exists():
		print(f"错误：找不到文件 {IPARSER_INIT_FILE}")
		return False

	try:
		with open(IPARSER_INIT_FILE, 'r', encoding='utf-8') as f:
			content = f.read()
			version_match = re.search(r"__version__\s*=\s*['\"](.*?)['\"]", content)

			if not version_match:
				print("错误：在 iparser.__init__.py 中找不到__version__变量")
				return False

			current_version = version_match.group(1)
			print(f"从 iparser.__init__.py 获取到当前版本号：{current_version}")
	except Exception as e:
		print(f"读取 iparser.__init__.py 文件时出错：{e}")
		return False

	version_parts = current_version.split('.')

	try:
		version_numbers = [int(part) for part in version_parts]
	except ValueError:
		print(f"错误：版本号 {current_version} 格式不正确，必须全部由数字组成")
		return False

	# 对于filevers和prodvers，需要确保是4位数字的元组格式
	while len(version_numbers) < 4:
		version_numbers.append(0)

	version_numbers = version_numbers[:4]
	tuple_version = f"({', '.join(map(str, version_numbers))})"

	if not VERSION_INFO_FILE.exists():
		print(f"错误：找不到文件 {VERSION_INFO_FILE}")
		return False

	try:
		with open(VERSION_INFO_FILE, 'r', encoding='utf-8') as f:
			file_content = f.read()

		# 更新filevers行
		file_content = re.sub(r'filevers=\(.*?\),', f'filevers={tuple_version},',
			file_content)
		# 更新prodvers行
		file_content = re.sub(r'prodvers=\(.*?\),', f'prodvers={tuple_version},',
			file_content)
		# 更新FileVersion行
		file_content = re.sub(
			r'StringStruct\(u\'FileVersion\',\s*u\'.*?\'\),',
			f'StringStruct(u\'FileVersion\', u\'{current_version}\'),',
			file_content)
		# 更新ProductVersion行
		file_content = re.sub(
			r'StringStruct\(u\'ProductVersion\',\s*u\'.*?\'\)\]\)',
			f'StringStruct(u\'ProductVersion\', u\'{current_version}\')])',
			file_content)

		with open(VERSION_INFO_FILE, 'w', encoding='utf-8') as f:
			f.write(file_content)

		print(f"已成功更新 {VERSION_INFO_FILE.name} 文件中的版本信息")
		print(f"  - filevers 和 prodvers 更新为：{tuple_version}")
		print(f"  - FileVersion 和 ProductVersion 更新为：{current_version}")
		return True
	except Exception as e:
		print(f"更新 {VERSION_INFO_FILE.name} 文件时出错：{e}")
		return False

def main():
	"""执行更新版本号的操作的主函数"""
	update_version()


if __name__ == "__main__":
	main()
