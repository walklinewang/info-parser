# Info Parser

<img src="https://img.shields.io/badge/Licence-MIT-green.svg?logo=github" />  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python" />  <img src="https://img.shields.io/badge/Windows-OS-red.svg?logo=windows" />

**Info Parser** 是一款申请人信息解析工具，能够从申请人的描述中提取机构名称、姓名、身份等信息。

## 主要功能

- 支持从申请人描述中提取机构名称、姓名、身份等信息
- 批量处理文件夹中的申请人描述文件
- 自动下载并裁剪封面图片
- 生成符合Kodi等媒体中心标准的NFO文件
- 按机构智能分类整理申请人目录
- 支持登录功能以获取更多内容

## 系统要求

- Python 3.10 或更高版本
- Windows 操作系统

## 使用说明

### 命令行参数

### 使用示例

## 二次开发说明

要进行二次开发，首先需要克隆项目文件到本地

```bash
git clone https://github.com/walklinewang/info-parser.git
cd info-parser
```

然后使用如下方法安装项目依赖项

### 使用 pip 安装依赖项（推荐）

```bash
pip install -e .
parser
```

> 此方法的优点是简单快捷，无需配置环境变量，可在任何位置直接使用`parser`命令，但是会将依赖项安装到全局 Python 环境中。

### 使用 Poetry 安装依赖项

```bash
poetry install
poetry run python -m parser
```

> 此方法的优点是仅在当前环境中安装项目及其依赖，而不会影响全局 Python 环境，缺点是只能在项目目录下使用`parser`命令。

## 工作原理

使用结巴分词和关键词匹配技术，从申请信息中提取机构名称、姓名和身份信息。

解析逻辑包括：

1. 初始化并配置结巴分词器
2. 对清理后的文本进行分词
3. 根据关键词识别机构名称
4. 提取机构名称后的部分作为姓名
5. 识别申请人身份（教师/学生）

## 注意事项

## 常见问题

## 许可证

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件
