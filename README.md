# Zesigen - 跨平台下载管理器

![GitHub Actions Workflow](https://github.com/zhangchengmc/Zesigen/actions/workflows/build-all-platforms.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

Zesigen 是一个功能强大的跨平台下载管理器，支持命令行和图形界面两种模式。它提供了多线程下载、断点续传、批量下载等高级功能。

## ✨ 特性

- **跨平台支持**: Windows, macOS, Linux 全平台支持
- **双模式界面**: 命令行(CLI)和图形界面(GUI)两种使用方式
- **多线程下载**: 支持多线程并发下载，提高下载速度
- **批量下载**: 支持从文件导入URL列表进行批量下载
- **进度显示**: 实时显示下载进度和速度
- **断点续传**: 支持下载中断后继续下载
- **用户友好**: 简洁直观的界面设计

## 📦 安装

### 方法一：下载预编译版本

从 [Releases](https://github.com/zhangchengmc/Zesigen/releases) 页面下载对应平台的预编译版本：

- **Windows**: `zesigen-windows.exe`
- **macOS**: `zesigen-macos`
- **Linux**: `zesigen-linux`

### 方法二：从源码运行

1. 克隆仓库：
   ```bash
   git clone https://github.com/zhangchengmc/Zesigen.git
   cd Zesigen
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序：
   ```bash
   python src/zesigen.py
   ```

### 方法三：使用 PyInstaller 自行编译

```bash
# 安装 PyInstaller
pip install pyinstaller

# 编译为单文件可执行程序
pyinstaller --onefile src/zesigen.py

# 编译为文件夹形式（包含依赖）
pyinstaller src/zesigen.py
```

## 🚀 使用方法

### 命令行模式 (CLI)

```bash
# 显示版本信息
zesigen --version

# 显示帮助信息
zesigen --help

# 下载单个文件
zesigen --cli --url https://example.com/file.zip --output ./downloads

# 从文件批量下载
zesigen --cli --file urls.txt --output ./downloads --threads 8

# 使用多线程下载
zesigen --cli --url https://example.com/largefile.iso --threads 4
```

### 图形界面模式 (GUI)

```bash
# 启动图形界面
zesigen --gui
```

或者在程序中直接双击运行（如果已编译为可执行文件）。

### 命令行参数

| 参数 | 简写 | 描述 | 示例 |
|------|------|------|------|
| `--help` | `-h` | 显示帮助信息 | `zesigen -h` |
| `--version` | `-v` | 显示版本信息 | `zesigen -v` |
| `--gui` | `-g` | 启动图形界面 | `zesigen -g` |
| `--cli` | `-c` | 使用命令行界面 | `zesigen -c` |
| `--url` | `-u` | 指定下载URL | `zesigen -u https://example.com/file.zip` |
| `--file` | `-f` | 从文件读取URL列表 | `zesigen -f urls.txt` |
| `--output` | `-o` | 指定输出目录 | `zesigen -o ./downloads` |
| `--threads` | `-t` | 指定线程数（默认：4） | `zesigen -t 8` |

## 📁 项目结构

```
Zesigen/
├── src/                    # 源代码目录
│   └── zesigen.py         # 主程序文件
├── docs/                  # 文档目录
│   ├── USER_GUIDE.md      # 用户指南
│   └── DEVELOPER_GUIDE.md # 开发者指南
├── assets/               # 资源文件目录
├── .github/workflows/    # GitHub Actions 工作流
│   ├── build-all-platforms.yml  # 全平台构建工作流
│   ├── quick-build.yml          # 快速构建工作流
│   └── test-windows.yml         # Windows测试工作流
├── requirements.txt      # Python依赖
├── LICENSE              # 许可证文件
└── README.md           # 项目说明
```

## 🔧 开发

### 环境设置

1. 确保已安装 Python 3.8+
2. 安装开发依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 运行测试

```bash
# 运行主程序测试
python src/zesigen.py --version

# 测试命令行模式
python src/zesigen.py --cli --help

# 测试图形界面
python src/zesigen.py --gui
```

### 构建可执行文件

项目使用 GitHub Actions 自动构建跨平台可执行文件。您也可以本地构建：

```bash
# Windows
pyinstaller --onefile --name zesigen-windows src/zesigen.py

# macOS/Linux
pyinstaller --onefile --name zesigen src/zesigen.py
chmod +x dist/zesigen
```

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 添加适当的注释和文档
- 确保跨平台兼容性
- 编写测试用例

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

- 提交 Issue: [GitHub Issues](https://github.com/zhangchengmc/Zesigen/issues)
- 查看文档: [docs/](docs/)
- 电子邮件: 项目维护者邮箱

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

**Zesigen** - 让下载更简单、更快速！