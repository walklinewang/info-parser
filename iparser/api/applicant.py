"""
This file is part of the Info Parser project, https://github.com/walklinewang/info-parser
The MIT License (MIT)
Copyright © 2025 Walkline Wang <walkline@gmail.com>

申请信息解析API

此模块提供了对申请人信息（如机构名称、姓名、身份等）的智能解析功能。
主要功能包括机构名称识别、姓名提取和身份标识（教师/学生）。

使用示例：

from iparser.api.applicant import Applicant
from iparser.utils import update_jieba_keywords


# 更新结巴分词关键词
update_jieba_keywords()

# 创建申请人对象
applicant = Applicant('天津理工大学计算机科学与工程学院江小白学生')

# 解析信息
applicant.parse()

# 获取解析结果
print(f'输入：{applicant.info}')
print(f'机构：{applicant.institution}')
print(f'姓名：{applicant.name}')
print(f'身份：{'教师' if applicant.is_teacher else '学生'}')
print(f'输出：{applicant.full_info}')

示例输出：
	输入：天津理工大学计算机科学与工程学院江小白学生
	机构：天津理工大学
	姓名：江小白
	身份：学生
	输出：天津理工大学-江小白
"""
from typing import List, Optional, Set

import jieba

from iparser.config import config
from iparser.logger import logger


TEACHER_IDENTITY: Set[str] = set(config.identity.teacher)
STUDENT_IDENTITY: Set[str] = set(config.identity.student)


class Applicant:
	"""
	申请人信息类

	用于存储和处理申请人的信息，包括原始信息、清理后的信息、机构、姓名和身份标识。

	Attributes:
		info: 原始申请信息字符串
		split_result: 对清理后的信息进行分词后的结果列表
		institution: 识别出的机构名称
		name: 识别出的申请人姓名
		is_teacher: 身份标识，True表示教师，False表示学生（默认值）
	"""
	def __init__(self, info: str):
		"""
		初始化申请人对象

		Args:
			info: 原始申请信息字符串
		"""
		self.__info: str = info
		self.__split_result: Optional[List[str]] = None
		self.__institution: Optional[str] = None
		self.__name: Optional[str] = None
		self.__is_teacher: bool = False

	def __str__(self):
		"""返回格式化的申请人信息字符串"""
		return self.full_info

	def __clean_info(self, info: str) -> str:
		"""
		清理字符串信息

		移除信息中的常见连接符和分隔符。

		Returns:
			str: 清理后的字符串
		"""
		for connector in set(config.formatting.connectors):
			info = info.replace(connector, '')

		info = info.strip()
		return info

	def parse(self):
		"""
		智能解析申请信息

		使用结巴分词和关键词匹配技术，从申请信息中提取机构名称、姓名和身份信息。
		解析逻辑包括：
		1. 初始化并配置结巴分词器
		2. 对清理后的文本进行分词
		3. 根据关键词识别机构名称
		4. 提取机构名称后的部分作为姓名
		5. 识别申请人身份（教师/学生）
		"""
		# 对清理后的文本进行分词
		segments = jieba.lcut(self.__info)
		self.__split_result = segments
		logger.debug(f'分词结果：{segments}')

		found_institution_end = False
		found_teacher_identity = False
		institution_parts = []
		name_parts = []

		# 遍历分词结果，识别机构、姓名和身份
		for segment in segments:
			segment = segment.strip()
			if not segment:
				continue

			logger.debug(f'处理分词：{segment}')

			# 识别教师身份
			if not found_teacher_identity:
				for identity in TEACHER_IDENTITY:
					if identity in segment:
						self.__is_teacher = True
						found_teacher_identity = True

						logger.info(f'识别到教师身份标识：{identity}')
						break

			# 识别机构
			if not found_institution_end:
				institution_parts.append(segment)
				logger.debug(f'添加到机构部分：{segment}')

				for keyword in config.institution.shortened_names:
					if keyword in segment:
						found_institution_end = True
						break

				for keyword in config.institution.suffixes:
					if keyword in segment:
						if len(institution_parts) > 1 or len(segment) > 2:
							found_institution_end = True
						else:
							institution_parts.pop()
						break

			# 识别姓名
			elif segment not in TEACHER_IDENTITY.union(STUDENT_IDENTITY):
				# 检查是否包含机构后缀关键词（可能是错误识别）
				has_institution_suffix = False
				for keyword in config.institution.all_suffixes:
					if keyword in segment:
						has_institution_suffix = True

						# 是否保留二级学院名称
						if config.formatting.include_secondary_college:
							name_parts.append(segment)
							institution_parts.extend(name_parts)

						name_parts = [] # 重置姓名识别
						logger.debug(f'姓名部分包含机构后缀：{keyword}，重置姓名识别')
						break

				if not has_institution_suffix:
					name_parts.append(segment)
					logger.debug(f'添加到姓名部分：{segment}')

		# 设置识别结果
		if found_institution_end and institution_parts:
			self.__institution = self.__clean_info(''.join(institution_parts))
			logger.debug(f'成功识别机构：{self.__institution}')
		else:
			self.__institution = config.institution.default_name
			logger.warning(f'  未能识别机构，设置为：{self.__institution}')

		self.__name = self.__clean_info(''.join(name_parts))
		if self.__name:
			logger.debug(f'成功识别姓名：{self.__name}')
		else:
			self.__name = config.name.default_name
			logger.warning(f'  未能识别姓名，设置为：{self.__name}')

	#region Properties
	@property
	def full_info(self) -> str:
		"""获取格式化的申请人信息字符串"""
		output_pattern = config.formatting.output_pattern_teacher \
			if self.__is_teacher else config.formatting.output_pattern_student
		output = {
			'institution': self.__institution,
			'name': self.__name,
		}

		return output_pattern.format(**output)

	@property
	def info(self) -> str:
		"""获取原始申请信息字符串"""
		return self.__info

	@property
	def split_result(self) -> Optional[List[str]]:
		"""获取分词结果"""
		return self.__split_result

	@property
	def institution(self) -> Optional[str]:
		"""获取机构名称"""
		return self.__institution

	@property
	def name(self) -> Optional[str]:
		"""获取申请人姓名"""
		return self.__name

	@property
	def is_teacher(self) -> bool:
		"""
		获取身份标识

		- True: 表示教师
		- False: 表示学生（默认值）
		"""
		return self.__is_teacher
	#endregion Properties
