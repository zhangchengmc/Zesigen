# Zesigen 用户指南

欢迎使用 Zesigen 下载管理器！本指南将帮助您了解如何使用 Zesigen 的各种功能。

## 目录

1. [快速开始](#快速开始)
2. [命令行模式](#命令行模式)
3. [图形界面模式](#图形界面模式)
4. [高级功能](#高级功能)
5. [常见问题](#常见问题)
6. [故障排除](#故障排除)

## 快速开始

### 首次使用

1. **下载程序**：
   - 从 [Releases](https://github.com/zhangchengmc/Zesigen/releases) 页面下载适合您操作系统的版本
   - 或者从源码运行（需要 Python 环境）

2. **基本命令**：
   ```bash
   # 显示版本信息
   zesigen --version

   # 显示帮助
   zesigen --help
   ```

3. **选择模式**：
   - 使用 `--gui` 启动图形界面
   - 使用 `--cli` 使用命令行界面

## 命令行模式

命令行模式适合批量操作和自动化任务。

### 基本用法

```bash
# 下载单个文件
zesigen --cli --url "https://example.com/file.zip" --output "./downloads"

# 下载多个文件（从文件读取URL列表）
zesigen --cli --file "urls.txt" --output "./downloads"

# 使用多线程下载
zesigen --cli --url "https://example.com/largefile.iso" --threads 8 --output "./downloads"
```

### URL 文件格式

创建一个文本文件（如 `urls.txt`），每行一个 URL：

```txt
# 这是一个URL列表文件
# 注释以 # 开头
https://example.com/file1.zip
https://example.com/file2.pdf
https://example.com/file3.mp4

# 支持HTTP和HTTPS
http://example.com/file4.txt
```

### 命令行参数详解

| 参数 | 必需 | 默认值 | 描述 |
|------|------|--------|------|
| `--help`, `-h` | 否 | - | 显示帮助信息 |
| `--version`, `-v` | 否 | - | 显示版本信息 |
| `--gui`, `-g` | 否 | - | 启动图形界面 |
| `--cli`, `-c` | 否 | - | 使用命令行界面 |
| `--url`, `-u` | 条件 | - | 下载单个URL（与 `--file` 二选一） |
| `--file`, `-f` | 条件 | - | 从文件读取URL列表（与 `--url` 二选一） |
| `--output`, `-o` | 否 | 当前目录 | 指定输出目录 |
| `--threads`, `-t` | 否 | 4 | 指定下载线程数（1-16） |

### 使用示例

**示例 1：批量下载图片**
```bash
# 创建URL文件 images.txt
echo "https://example.com/image1.jpg" > images.txt
echo "https://example.com/image2.jpg" >> images.txt
echo "https://example.com/image3.jpg" >> images.txt

# 批量下载
zesigen --cli --file images.txt --output "./pictures" --threads 4
```

**示例 2：下载大文件**
```bash
# 使用更多线程加速下载
zesigen --cli --url "https://example.com/ubuntu-22.04.iso" --threads 8 --output "./isos"
```

**示例 3：结合其他命令**
```bash
# 从剪贴板读取URL并下载
pbpaste | zesigen --cli --file - --output "./downloads"

# Linux/Mac: 从管道读取
echo "https://example.com/file.zip" | zesigen --cli --file - --output "./downloads"
```

## 图形界面模式

图形界面模式提供直观的操作体验，适合普通用户。

### 启动图形界面

```bash
zesigen --gui
```

或者直接双击可执行文件（如果已编译）。

### 界面介绍

图形界面包含以下区域：

1. **URL输入区**：
   - 手动输入URL，每行一个
   - 支持从文件导入（点击"从文件导入"按钮）
   - 可以清空输入（点击"清空"按钮）

2. **设置区**：
   - **输出目录**：选择文件保存位置
   - **线程数**：设置并发下载线程数（1-16）

3. **控制按钮**：
   - **开始下载**：开始下载任务
   - **暂停**：暂停当前下载（功能开发中）
   - **关于**：显示程序信息

4. **下载进度区**：
   - 显示每个文件的下载进度
   - 显示文件名、进度百分比和状态

5. **日志区**：
   - 显示详细的操作日志
   - 包括下载开始、进度更新、完成等信息

### 使用步骤

1. **输入URL**：
   - 在URL输入区手动输入下载链接
   - 或点击"从文件导入"选择包含URL列表的文本文件

2. **设置参数**：
   - 点击"浏览"选择保存目录
   - 调整线程数（默认4个，根据网络情况调整）

3. **开始下载**：
   - 点击"开始下载"按钮
   - 在进度区查看下载进度
   - 在日志区查看详细信息

4. **完成下载**：
   - 下载完成后会弹出提示
   - 所有文件保存在指定目录

### 导入URL文件

1. 点击"从文件导入"按钮
2. 选择包含URL列表的文本文件
3. 程序会自动读取文件内容并填充到URL输入区

支持的文件格式：
- 纯文本文件（.txt）
- 每行一个URL
- 支持#开头的注释行

## 高级功能

### 多线程下载

Zesigen 支持多线程下载，可以显著提高下载速度：

```bash
# 使用8个线程下载
zesigen --cli --url "https://example.com/largefile.zip" --threads 8
```

**建议**：
- 小文件：1-2个线程
- 中等文件：4个线程
- 大文件：8-16个线程（根据网络带宽调整）

### 批量下载

批量下载支持多种方式：

1. **从文件导入**：
   ```bash
   zesigen --cli --file "url_list.txt" --output "./batch_downloads"
   ```

2. **使用通配符**（需要脚本配合）：
   ```bash
   # 生成URL列表
   seq 1 10 | awk '{print "https://example.com/file" $1 ".zip"}' > urls.txt
   zesigen --cli --file urls.txt
   ```

### 输出目录管理

程序会自动创建不存在的目录：

```bash
# 如果 ./downloads/new_folder 不存在，会自动创建
zesigen --cli --url "https://example.com/file.zip" --output "./downloads/new_folder"
```

### 进度显示

- 命令行模式：使用 tqdm 进度条
- 图形界面：实时进度百分比和状态显示

## 常见问题

### Q1: 下载速度慢怎么办？
- 检查网络连接
- 增加线程数：`--threads 8`
- 尝试不同的输出目录（避免系统盘）

### Q2: 下载中断怎么办？
- 重新运行下载命令，程序会覆盖已下载的部分
- 确保有足够的磁盘空间
- 检查URL是否有效

### Q3: 如何下载需要认证的文件？
当前版本不支持需要HTTP认证的下载。如果需要此功能，请提交Issue。

### Q4: 支持哪些协议？
- HTTP
- HTTPS
- 未来计划支持FTP

### Q5: 最大支持多少线程？
- 理论上最多16个线程
- 实际建议根据网络带宽调整（通常4-8个线程最佳）

### Q6: 如何查看下载日志？
- 命令行模式：直接在终端查看
- 图形界面：在日志区域查看

## 故障排除

### 错误：无法连接到服务器
```
错误：无法连接到服务器
```

**解决方案**：
1. 检查网络连接
2. 验证URL是否正确
3. 尝试使用其他网络

### 错误：磁盘空间不足
```
错误：写入文件失败
```

**解决方案**：
1. 清理磁盘空间
2. 更换输出目录到有足够空间的磁盘
3. 检查文件权限

### 错误：无效的URL
```
错误：无效的URL格式
```

**解决方案**：
1. 检查URL格式是否正确
2. 确保URL包含协议（http:// 或 https://）
3. 移除URL中的多余空格

### 错误：线程数无效
```
错误：线程数必须在1-16之间
```

**解决方案**：
1. 使用有效的线程数：`--threads 4`
2. 不要超过16个线程

### 程序崩溃或无响应
**解决方案**：
1. 重启程序
2. 减少线程数
3. 检查系统资源使用情况
4. 提交Issue报告问题

## 获取帮助

如果遇到问题无法解决：

1. **查看日志**：程序会记录详细的操作日志
2. **提交Issue**：[GitHub Issues](https://github.com/zhangchengmc/Zesigen/issues)
3. **查阅文档**：查看其他文档文件
4. **联系开发者**：通过GitHub联系项目维护者

---

希望本指南能帮助您更好地使用 Zesigen！如果有任何建议或发现问题，欢迎反馈。