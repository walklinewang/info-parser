"""
This file is part of the Info Parser project, https://github.com/walklinewang/info-parser
The MIT License (MIT)
Copyright © 2025 Walkline Wang <walkline@gmail.com>
"""
import logging
from typing import List, Set

import jieba
jieba.setLogLevel(logging.INFO)

from .config import config
from .logger import logger


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
		print(f'错误：样本文件 "{file_path}" 不存在')
		raise
	except IOError as e:
		print(f'错误：读取文件 "{file_path}" 失败: {str(e)}')
		raise
	except Exception as e:
		print(f'错误：处理文件 "{file_path}" 时发生未知错误: {str(e)}')
		raise

def update_jieba_keywords():
	"""
	更新Jieba分词器配置

	将机构后缀和特殊机构名称添加到分词器中，并移除需要排除的关键词，
	以提高机构名称和人名识别的准确性。

	操作包括：
	- 将特殊机构名称合并到机构后缀集合中
	- 为所有机构关键词设置分词频率
	- 删除需要排除的关键词
	"""
	logger.debug('开始更新Jieba分词器配置...')

	# 合并特殊机构名称到机构后缀集合
	logger.debug(f'  已合并特殊机构，当前机构关键词总数：{len(config.institution.all_suffixes)}')

	# 添加机构关键词到分词器
	added_count = 0
	for keyword in config.institution.all_suffixes:
		jieba.add_word(keyword)
		jieba.suggest_freq(keyword, True)
		added_count += 1
	logger.debug(f'  已添加 {added_count} 个机构关键词到分词器')

	# 删除干扰关键词
	deleted_count = 0
	for keyword in set(config.institution.excluded_keywords):
		jieba.del_word(keyword)
		deleted_count += 1
	logger.debug(f'  已删除 {deleted_count} 个干扰关键词')
