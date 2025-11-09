"""
This file is part of the Info Parser project, https://github.com/walklinewang/info-parser
The MIT License (MIT)
Copyright © 2025 Walkline Wang <walkline@gmail.com>
"""
from pathlib import Path
from typing import Set

from confz import BaseConfig, FileSource

from iparser.logger import logger
from iparser.utils import resource_path


class Identity(BaseConfig):
	"""身份解析配置"""
	teacher: Set[str] # 教师身份关键词
	student: Set[str] # 学生身份关键词


class Formatting(BaseConfig):
	"""格式化配置"""
	output_pattern_teacher: str     # 教师输出格式
	output_pattern_student: str     # 学生输出格式
	connectors: Set[str]            # 连接符和分隔符
	include_secondary_college: bool # 是否包含二级学院


class Institution(BaseConfig):
	"""机构解析配置"""
	suffixes: Set[str]          # 机构后缀关键词
	shortened_names: Set[str]       # 机构简称
	excluded_keywords: Set[str] # 排除的关键词
	default_name: str           # 默认机构名称

	def add_shortened_names(self, names: Set[str]):
		"""添加机构简称"""
		self.shortened_names.update(names)

	def add_excluded_keywords(self, keywords: Set[str]):
		"""添加排除的关键词"""
		self.excluded_keywords.update(keywords)

	@property
	def all_suffixes(self) -> Set[str]:
		"""获取所有机构后缀和简称关键词"""
		return self.suffixes.union(self.shortened_names)


class Name(BaseConfig):
	"""姓名解析配置"""
	default_name: str # 默认姓名


def get_config_source():
	"""获取配置文件源"""
	sources = []
	source = resource_path('config.yml')

	if not source.exists():
		logger.warning(f'配置文件 {source} 不存在，将创建一个默认配置文件')

		with open(Path(__file__).parent.parent / 'config.yml', 'rb') as input_file:
			with open(source, 'wb') as output_file:
				output_file.write(input_file.read())

	sources.append(FileSource(file=source))

	return sources

class Config(BaseConfig):
	"""信息解析器主配置"""
	identity: Identity
	formatting: Formatting
	institution: Institution
	name: Name
	CONFIG_SOURCES = get_config_source()


config = Config()
