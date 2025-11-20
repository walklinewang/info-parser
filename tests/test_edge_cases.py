"""
边界情况和异常测试

此模块测试Applicant类在边界情况和异常输入下的行为，确保代码的健壮性。
"""
import pytest

from iparser.api.applicant import Applicant
from iparser.config import config


class TestEdgeCases:
	"""边界情况和异常测试类"""

	def test_empty_input(self):
		"""测试空输入情况"""
		applicant = Applicant('')
		applicant.parse()

		# 空输入应该返回默认值
		assert applicant.institution == config.institution.default_name
		assert applicant.name == config.name.default_name
		assert applicant.is_teacher is False

	def test_whitespace_input(self):
		"""测试仅包含空白字符的输入"""
		whitespace_cases = [' ', '\t', '\n', '  \t  \n  ']

		for case in whitespace_cases:
			applicant = Applicant(case)
			applicant.parse()

			# 空白输入应该返回默认值
			assert applicant.institution == config.institution.default_name
			assert applicant.name == config.name.default_name
			assert applicant.is_teacher is False

	def test_only_identity(self):
		"""测试仅包含身份标识的输入"""
		identities = config.identity.teacher.union(config.identity.student)

		for identity in identities:
			applicant = Applicant(identity)
			applicant.parse()

			# 只有身份标识的输入应该返回默认机构和姓名
			assert applicant.institution == config.institution.default_name
			assert applicant.name == config.name.default_name

			# 身份标识应该被正确识别
			if identity in config.identity.teacher:
				assert applicant.is_teacher is True
			else:
				assert applicant.is_teacher is False

	def test_only_institution(self):
		"""测试仅包含机构名称的输入"""
		institutions = ['河南科技职业大学', '北京大学', '清华大学', '哈理工']

		for institution in institutions:
			applicant = Applicant(institution)
			applicant.parse()

			# 机构应该被正确识别
			assert applicant.institution == institution
			# 姓名应该返回默认值
			assert applicant.name == config.name.default_name
			assert applicant.is_teacher is False

	@pytest.mark.xfail(reason='当前无法正确识别单独的姓名')
	def test_only_name(self):
		"""测试仅包含姓名的输入"""
		names = ['张三', '李四', '王五', '赵六']

		for name in names:
			applicant = Applicant(name)
			applicant.parse()

			# 机构应该返回默认值
			assert applicant.institution == config.institution.default_name
			# 姓名应该被正确识别
			assert applicant.name == name
			assert applicant.is_teacher is False

	def test_special_characters(self):
		"""测试包含特殊字符的输入"""
		special_cases = [
			'河南科技职业大学-#￥%……&*()杨怡宁',
			'北京大学@!李四',
			'清华大学$%^赵六',
			'哈理工&*()钱七',
		]

		for case in special_cases:
			applicant = Applicant(case)
			applicant.parse()

			# 检查解析不会崩溃
			assert applicant.institution is not None
			assert applicant.name is not None

	def test_long_input(self):
		"""测试超长输入情况"""
		# 创建一个很长的输入
		long_institution = '河南科技职业大学' * 10
		long_name = '杨怡宁' * 20
		long_input = f'{long_institution}{long_name}学生'

		applicant = Applicant(long_input)
		applicant.parse()

		# 检查解析不会崩溃
		assert applicant.institution is not None
		assert applicant.name is not None

	def test_duplicate_identity(self):
		"""测试包含重复身份标识的输入"""
		duplicate_marker_cases = [
			'河南科技职业大学杨怡宁学生学生',
			'河南工学院郭学强教师老师',
			'北京大学李四学生学',
		]

		for case in duplicate_marker_cases:
			applicant = Applicant(case)
			applicant.parse()

			# 检查解析不会崩溃
			assert applicant.institution is not None
			assert applicant.name is not None

			# 身份应该被正确识别
			if '教师' in case or '老师' in case:
				assert applicant.is_teacher is True
			else:
				assert applicant.is_teacher is False

	def test_conflicting_identity(self):
		"""测试包含冲突身份标识的输入（同时包含学生和教师标识）"""
		conflicting_cases = [
			'河南科技职业大学杨怡宁学生教师',
			'河南工学院郭学强教师学生',
		]

		for case in conflicting_cases:
			applicant = Applicant(case)
			applicant.parse()

			# 检查解析不会崩溃
			assert applicant.institution is not None
			assert applicant.name is not None

			# 根据实现，应该识别到教师标识
			assert applicant.is_teacher is True

	def test_mixed_cases(self):
		"""测试混合大小写的输入"""
		mixed_cases = [
			'河南科技职业大学杨怡宁',
			'河NAN科JI职业大学杨怡宁',
			'HENAN科技职YE大学杨怡宁',
			'HENAN KEJI ZHIYE UNIVERSITY杨怡宁',
		]

		for case in mixed_cases:
			applicant = Applicant(case)
			applicant.parse()

			# 检查解析不会崩溃
			assert applicant.institution is not None
			assert applicant.name is not None

	def test_multiple_institutions(self):
		"""测试包含多个机构名称的输入"""
		multiple_institution_cases = [
			'河南科技职业大学北京大学杨怡宁',
			'北京大学清华大学李四',
			'哈理工河工大王五',
		]

		for case in multiple_institution_cases:
			applicant = Applicant(case)
			applicant.parse()

			# 检查解析不会崩溃
			assert applicant.institution is not None
			assert applicant.name is not None

			# 根据解析逻辑，应该识别第一个机构
			if '河南科技职业大学' in case:
				assert applicant.institution == '河南科技职业大学'
			elif '北京大学' in case:
				assert applicant.institution == '北京大学'
			elif '哈理工' in case:
				assert applicant.institution == '哈理工'
