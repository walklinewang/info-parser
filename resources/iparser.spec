# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import glob


def hiddenimports():
	imports = []
	for file in glob.glob('iparser/*.py', recursive=False):
		name, ext = Path(file).stem, Path(file).suffix
		if ext == '.py':
			imports.append('iparser.' + name)

	for file in glob.glob('iparser/gui/*.py', recursive=False):
		name, ext = Path(file).stem, Path(file).suffix
		if ext == '.py':
			imports.append('iparser.gui.' + name)

	print(imports)
	return imports

a = Analysis(
	['../iparser/gui/__main__.py'],  # 主运行文件路径
	pathex=['..'],  # 搜索路径列表，添加项目根目录以查找所有模块
	binaries=[],  # 额外的二进制文件列表
	datas=[
		('../config.yml', '.'),  # 包含配置文件
		('../resources/icon.ico', '.'),  # 包含图标文件
		('../resources/version_info', '.'),  # 包含版本信息文件
	],  # 数据文件列表
	hiddenimports=hiddenimports(), # 隐式导入的模块列表
	hookspath=[],  # 自定义hook脚本的路径
	hooksconfig={},  # hook配置选项
	runtime_hooks=[],  # 运行时钩子脚本列表
	excludes=[
		'tkinter.test',
		'tkinter.tix',
		'tkinter.ttk.test',
	],  # 排除不必要的模块以减小体积
	noarchive=False,
	optimize=2,  # 使用最高级别优化
	cipher=None,
)
pyz = PYZ(a.pure)

exe = EXE(
	pyz,  # 打包后的Python字节码对象
	a.scripts,  # 脚本文件列表
	a.binaries,  # 二进制文件列表
	a.datas,  # 数据文件列表
	options=[],  # 额外选项列表
	name='iparser',  # 生成的可执行文件名
	debug=False,  # 是否启用调试模式
	bootloader_ignore_signals=False,  # 是否忽略引导加载器信号
	strip=False,  # Windows不支持strip命令
	runtime_tmpdir=None,  # 运行时临时目录
	console=False,  # 是否显示控制台窗口
	disable_windowed_traceback=False,  # 是否禁用窗口模式下的回溯
	argv_emulation=False,  # 是否模拟argv参数
	codesign_identity=None,  # 代码签名身份
	entitlements_file=None,  # 授权文件
	version='version_info',  # 版本信息文件（已在datas中包含）
	icon='icon.ico',  # 应用图标文件（已在datas中包含）
)
