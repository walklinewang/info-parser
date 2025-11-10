"""
This file is part of the Info Parser project, https://github.com/walklinewang/info-parser
The MIT License (MIT)
Copyright © 2025 Walkline Wang <walkline@gmail.com>
"""
import logging
import sys
from pathlib import Path

import jieba
jieba.setLogLevel(logging.INFO)

from iparser.logger import logger


def resource_path(path: str) -> Path:
	"""获取一个随代码打包的文件在解压后的路径"""
	if getattr(sys, 'frozen', False):
		return Path(path)

	path_joined = Path(__file__).parent.parent / path
	return path_joined

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
	from iparser.config import config

	logger.debug('开始更新Jieba分词器配置...')
	logger.debug(f'  当前机构关键词总数（含简称）：{len(config.institution.all_suffixes)}')

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
	logger.debug('Jieba分词器配置更新完成')
