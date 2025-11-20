"""
Applicant类的基本功能测试

此模块测试Applicant类的核心功能，包括初始化、解析和各种基本场景。
"""
from iparser.api.applicant import Applicant
from iparser.config import config


class TestApplicant:
	"""测试Applicant类的基本功能"""

	def test_basic_parsing_cases(self, samples_normal):
		"""
		测试基本的解析场景

		Args:
			samples_normal: 测试fixture提供的测试用例列表
		"""
		for case in samples_normal:
			applicant = Applicant(case['input'])
			applicant.parse()

			# 验证解析结果
			assert applicant.institution == case['expected']['institution']
			assert applicant.name == case['expected']['name']
			assert applicant.is_teacher == case['expected']['is_teacher']

	def test_parsing_without_name(self, samples_without_name):
		"""
		测试不带姓名的解析场景

		Args:
			sample_without_name: 测试fixture提供的测试用例列表
		"""
		for case in samples_without_name:
			applicant = Applicant(case['input'])
			applicant.parse()

			# 验证解析结果
			assert applicant.institution == case['expected']['institution']
			assert applicant.name == case['expected']['name']
			assert applicant.is_teacher == case['expected']['is_teacher']

	def test_with_secondary_college(self, samples_with_secondary_college,
		samples_without_secondary_college):
		"""测试带二级学院的解析场景"""
		include_secondary_college = config.formatting.include_secondary_college

		test_cases = samples_with_secondary_college if include_secondary_college\
			else samples_without_secondary_college

		for case in test_cases:
			applicant = Applicant(case['input'])
			applicant.parse()

			# 验证解析结果
			assert applicant.institution == case['expected']['institution']
			assert applicant.name == case['expected']['name']
			assert applicant.is_teacher == case['expected']['is_teacher']

	def test_parsing_others(self, samples_others):
		"""测试其他特殊场景的解析"""
		for case in samples_others:
			applicant = Applicant(case['input'])
			applicant.parse()

			# 验证解析结果
			assert applicant.institution == case['expected']['institution']
			assert applicant.name == case['expected']['name']
			assert applicant.is_teacher == case['expected']['is_teacher']
