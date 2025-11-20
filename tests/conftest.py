"""pytest 共享配置和 fixture"""
import os
import sys
from typing import Any, Dict, List

import pytest

from iparser.logger import disable_logging
from iparser.utils import update_jieba_keywords


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
disable_logging()
update_jieba_keywords()

def pytest_html_results_table_header(cells):
	"""HTML 结果表格头"""
	cells[:] = cells[:-2]

def pytest_html_results_table_row(cells):
	"""HTML 结果表格行"""
	cells[:] = cells[:-2]

@pytest.fixture
def samples_normal() -> List[Dict[str, Any]]:
	"""普通样本"""
	return [
		# 不带分隔符的样本
		{'input': '河南科技职业大学杨怡宁', 'expected': {
			'institution': '河南科技职业大学', 'name': '杨怡宁', 'is_teacher': False}},
		{'input': '白城师范学院钱佳乐', 'expected': {
			'institution': '白城师范学院', 'name': '钱佳乐', 'is_teacher': False}},


		# 带分隔符的样本
		{'input': '黄淮学院—潘豫皖', 'expected': {
			'institution': '黄淮学院', 'name': '潘豫皖', 'is_teacher': False}},
		{'input': '新乡学院－刘菲菲', 'expected': {
			'institution': '新乡学院', 'name': '刘菲菲', 'is_teacher': False}},
		{'input': '长春电子科技学院/司马飞鸟', 'expected': {
			'institution': '长春电子科技学院', 'name': '司马飞鸟', 'is_teacher': False}},

		# 带身份标识的样本
		{'input': '河南科技职业大学游一晨（学生）', 'expected': {
			'institution': '河南科技职业大学', 'name': '游一晨', 'is_teacher': False}},
		{'input': '长春工业大学李佳美学生', 'expected': {
			'institution': '长春工业大学', 'name': '李佳美', 'is_teacher': False}},
		{'input': '吉林财经大学范德瑞（学）', 'expected': {
			'institution': '吉林财经大学', 'name': '范德瑞', 'is_teacher': False}},

		# 带身份标识和分隔符的样本
		{'input': '河南工业大学-赵晨光学生', 'expected': {
			'institution': '河南工业大学', 'name': '赵晨光', 'is_teacher': False}},
		{'input': '黄淮学院—张淑怡（学生）', 'expected': {
			'institution': '黄淮学院', 'name': '张淑怡', 'is_teacher': False}},
		{'input': '吉林工程技术师范学院，宋琪琪(学生)', 'expected': {
			'institution': '吉林工程技术师范学院', 'name': '宋琪琪', 'is_teacher': False}},
		{'input': '河南工学院-郭自强（教师）', 'expected': {
			'institution': '河南工学院', 'name': '郭自强', 'is_teacher': True}},
		{'input': '河南财经政法大学——侯小娟（学生）', 'expected': {
			'institution': '河南财经政法大学', 'name': '侯小娟', 'is_teacher': False}},
		{'input': '新乡学院-赵学敏-学生', 'expected': {
			'institution': '新乡学院', 'name': '赵学敏', 'is_teacher': False}},
		{'input': '新乡学院丶王化学生', 'expected': {
			'institution': '新乡学院', 'name': '王化', 'is_teacher': False}},
		{'input': '商丘学院-学生栗肃', 'expected': {
			'institution': '商丘学院', 'name': '栗肃', 'is_teacher': False}},

		# 带空格的样本
		{'input': '河南科技职业大学     曹铁琳', 'expected': {
			'institution': '河南科技职业大学', 'name': '曹铁琳', 'is_teacher': False}},
		{'input': '河南财经政法大学 李炳浩', 'expected': {
			'institution': '河南财经政法大学', 'name': '李炳浩', 'is_teacher': False}},

		# 带空格和身份标识的样本
		{'input': '新乡学院 汤唯鑫(学生)', 'expected': {
			'institution': '新乡学院', 'name': '汤唯鑫', 'is_teacher': False}},
		{'input': '黄淮学院刘佳晨 学生', 'expected': {
			'institution': '黄淮学院', 'name': '刘佳晨', 'is_teacher': False}},
		{'input': '河南科技职业大学 王明玥 学生', 'expected': {
			'institution': '河南科技职业大学', 'name': '王明玥', 'is_teacher': False}},
	]

@pytest.fixture
def samples_without_name() -> List[Dict[str, Any]]:
	"""不带姓名的样本"""
	return [
		# 不带姓名的样本'
		{'input': '河南财经政法大学 学生', 'expected': {
			'institution': '河南财经政法大学', 'name': '无名无姓', 'is_teacher': False}},
		{'input': '河南师范大学 教师', 'expected': {
			'institution': '河南师范大学', 'name': '无名无姓', 'is_teacher': True}},
		{'input': '商丘学院-李老师', 'expected': {
			'institution': '商丘学院', 'name': '李老师', 'is_teacher': True}},
	]

@pytest.fixture
def samples_without_secondary_college() -> List[Dict[str, Any]]:
	"""预期结果不带二级学院的样本"""
	return [
		# 带二级学院的样本
		{'input': '天津理工大学计算机科学与工程学院江小白学生', 'expected': {
			'institution': '天津理工大学', 'name': '江小白', 'is_teacher': False}},	
		{'input': '商丘学院应用科技学院李金灿', 'expected': {
			'institution': '商丘学院应用科技学院', 'name': '李金灿', 'is_teacher': False}},
		{'input': '长春大学旅游学院 刘诗诗教师', 'expected': {
			'institution': '长春大学旅游学院', 'name': '刘诗诗', 'is_teacher': True}},
		{'input': '武汉大学-计算机学院-软件工程系-赵六', 'expected': {
			'institution': '武汉大学计算机学院软件工程系', 'name': '赵六', 'is_teacher': False}},
	]

@pytest.fixture
def samples_with_secondary_college() -> List[Dict[str, Any]]:
	"""预期结果带二级学院的样本"""
	return [
		# 带二级学院的样本
		{'input': '天津理工大学计算机科学与工程学院江小白学生', 'expected': {
			'institution': '天津理工大学计算机科学与工程学院', 'name': '江小白', 'is_teacher': False}},	
		{'input': '商丘学院应用科技学院李金灿', 'expected': {
			'institution': '商丘学院应用科技学院', 'name': '李金灿', 'is_teacher': False}},
		{'input': '长春大学旅游学院 刘诗诗教师', 'expected': {
			'institution': '长春大学旅游学院', 'name': '刘诗诗', 'is_teacher': True}},
		{'input': '武汉大学-计算机学院-软件工程系-赵六', 'expected': {
			'institution': '武汉大学计算机学院软件工程系', 'name': '赵六', 'is_teacher': False}},
	]

@pytest.fixture
def samples_others() -> List[Dict[str, Any]]:
	"""其他样本"""
	return [
		# 同时带学生、教师姓名的样本
		{'input': '哈理工   王老五，刘老六', 'expected': {
			'institution': '哈理工', 'name': '王老五刘老六', 'is_teacher': False}},

		# 使用简称的样本
		{'input': '洛理王鹏翔', 'expected': {
			'institution': '洛理', 'name': '王鹏翔', 'is_teacher': False}},
		{'input': '河工大-陈立柱', 'expected': {
			'institution': '河工大', 'name': '陈立柱', 'is_teacher': False}},
		{'input': '商科院-白百万', 'expected': {
			'institution': '商科院', 'name': '白百万', 'is_teacher': False}},

		# 带干扰词的样本
		{'input': '安阳学院路飞燕', 'expected': {
			'institution': '安阳学院', 'name': '路飞燕', 'is_teacher': False}},
	]
