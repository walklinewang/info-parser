# Info Parser

<img src="https://img.shields.io/badge/Licence-MIT-green.svg?logo=github" />  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python" />  <img src="https://img.shields.io/badge/Windows-OS-red.svg?logo=windows" />

**Info Parser** 是一款申请人信息智能解析工具，能够从申请人的描述中自动提取机构名称、姓名、身份等关键信息。

## 项目需求

因工作需要，经常要处理一些QQ群入群申请，入群需要回答问题以便确定申请人身份，主要包括院校、姓名和身份。

入群问题如下：

```docs
学校-姓名(学生/教师)
```

鉴于每个人对问题理解的不同，所以回答也是多种多样的，例如：

- **标准（期望）的格式**：`院校-姓名`或`院校-姓名（教师）`（对应`config.yml`中的`formatting.output_pattern_*`）
- **带分隔符的格式**：院校与姓名之间的分隔符可能是空格、中划线、下划线等（对应`config.yml`中的`formatting.separator`）
- **带身份标识的样本**：申请信息中包含`学生`或`教师`字样，也可能是`学`或`教`（对应`config.yml`中的`identity`）
- **使用简称的样本**：多数院校简称是无法直接识别的，需要在配置文件中添加对应关系（对应`config.yml`中的`institution.shortened_names`）
- **不带姓名的样本**：申请信息中不包含姓名，理论上是不会批准入群的（对应`config.yml`中的`formatting.require_name`）
- **同时包含学生和教师姓名的样本**：这是一种特殊情况，目前没有好的方法进行拆分过滤

## 主要功能

- 智能识别和提取申请人信息（机构名称、姓名、身份）
- 支持文本预处理和清理
- 提供简洁易用的 Python API
- 包含图形用户界面（GUI），操作直观
- 支持自定义配置，灵活适应不同场景
- 完善的日志记录，便于调试和问题排查

## 系统要求

- Python 3.10 或更高版本
- Windows 操作系统
- 主要依赖：jieba 分词库、confz 配置管理库

## 安装方法

### 方法一：使用 pip 安装（推荐）

```bash
# 克隆项目
 git clone https://github.com/walklinewang/info-parser.git
 cd info-parser

# 安装项目及其依赖
 pip install -e .
```

### 方法二：使用 Poetry 安装

```bash
# 克隆项目
 git clone https://github.com/walklinewang/info-parser.git
 cd info-parser

# 安装依赖
 poetry install
```

## 使用方法

### 1. 命令行启动 GUI

安装完成后，可以直接通过命令行启动图形界面：

```bash
# 使用 pip 安装的方式
 iparser

# 使用 Poetry 安装的方式
 poetry run iparser
```

### 2. 作为 Python 模块运行

```bash
# 运行 GUI 界面
 python -m iparser.gui.__main__

# 运行命令行测试
 python -m iparser.__main__
```

### 3. API 使用示例

Info Parser 提供了简洁的 Python API，可以轻松集成到其他项目中：

```python
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
```

示例输出：
```docs
输入：天津理工大学计算机科学与工程学院江小白学生
机构：天津理工大学
姓名：江小白
身份：学生
输出：天津理工大学-江小白
```

## 配置说明

项目使用 YAML 格式的配置文件 `config.yml`，包含以下主要配置项：

- **identity**: 身份识别关键词（教师/学生）
- **formatting**: 输出格式配置
- **institution**: 机构识别相关配置
- **name**: 姓名解析相关配置

如果配置文件不存在，系统会自动从项目根目录复制默认配置。

## 核心 API 文档

### Applicant 类

```python
class Applicant(info: str)
```

申请人信息处理的核心类，用于存储和解析申请人信息。

**参数**

- `info`: 原始申请信息字符串

**主要方法**

- `parse()`: 解析申请信息，提取机构、姓名和身份

**主要属性**

- info: 原始申请信息字符串
- split_result: 对清理后的信息进行分词后的结果列表
- institution: 识别出的机构名称
- name: 识别出的申请人姓名
- is_teacher: 身份标识，True表示教师，False表示学生（默认值）

### update_jieba_keywords() 函数

```python
def update_jieba_keywords()
```

更新 Jieba 分词器配置，优化机构和人名识别效果。

## 工作原理

Info Parser 使用结巴分词和关键词匹配技术，结合规则引擎实现信息提取：

1. **文本预处理**：清理输入文本，移除连接符和分隔符
2. **分词处理**：使用结巴分词对文本进行分词
3. **机构识别**：基于预定义的机构后缀和关键词识别机构名称
4. **姓名提取**：提取机构名称后的部分作为申请人姓名
5. **身份识别**：通过关键词匹配判断申请人身份（教师/学生）

## 开发与调试

### 运行测试

```bash
# 使用 pytest 运行测试
 poetry run pytest
```

### 代码规范

项目使用 pylint 进行代码质量检查，配置位于 `pyproject.toml` 文件中。

## 常见问题

### 配置文件找不到

系统会自动检查并复制默认配置文件，确保程序正常运行。

### 解析结果不准确

可以通过修改 `config.yml` 中的配置项来优化解析效果，特别是调整机构关键词和身份标识词。

- 如果出现学院简称，需要在 `config.yml` 中添加该简称，例如：

    ```yaml
    institution:
        shortened_names:
            '哈工大'
    ```

- 如果出现分词错误，例如`某某学院路某某`可能会将`学院路`识别为一个词组导致解释失败，则需要在 `config.yml` 中添加该词组，例如：

    ```yaml
    institution:
        excluded_keywords:
            '学院路'
    ```

> 以上两项修改也可以在主界面的配置区域进行添加删除操作，修改的内容会保存在`custom_config.json`文件中

## 许可证

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件
