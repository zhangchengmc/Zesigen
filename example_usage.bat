@echo off
REM Zesigen 使用示例脚本 (Windows版本)
REM 展示如何使用 Zesigen 的各种功能

echo === Zesigen 使用示例 ===
echo.

REM 切换到脚本所在目录
cd /d "%~dp0"

REM 检查Python是否可用
where python >nul 2>nul
if errorlevel 1 (
    echo 错误: 未找到 python
    pause
    exit /b 1
)

echo 1. 显示版本信息
echo ------------------------
python src/zesigen.py --version
echo.

echo 2. 显示帮助信息
echo ------------------------
python src/zesigen.py --help
echo.

echo 3. 显示命令行帮助
echo ------------------------
python src/zesigen.py --cli --help
echo.

echo 4. 测试下载器功能
echo ------------------------
REM 创建测试目录
set TEST_DIR=.\test_downloads
if not exist "%TEST_DIR%" mkdir "%TEST_DIR%"

REM 创建测试URL文件
(
    echo # 测试URL文件
    echo https://httpbin.org/image/jpeg
    echo https://httpbin.org/image/png
) > test_urls.txt

echo 创建了测试URL文件: test_urls.txt
echo 测试下载目录: %TEST_DIR%
echo.

echo 5. 运行功能测试
echo ------------------------
python test_core.py
if errorlevel 1 (
    echo ✗ 核心功能测试失败
) else (
    echo ✓ 核心功能测试通过
)
echo.

echo 6. 清理测试文件
echo ------------------------
if exist "%TEST_DIR%" (
    rmdir /s /q "%TEST_DIR%"
    echo 已删除测试目录: %TEST_DIR%
)

if exist "test_urls.txt" (
    del "test_urls.txt"
    echo 已删除测试文件: test_urls.txt
)

echo.
echo === 示例完成 ===
echo.
echo 更多用法请参考:
echo   - README.md - 项目说明和快速开始
echo   - docs\USER_GUIDE.md - 详细用户指南
echo   - docs\DEVELOPER_GUIDE.md - 开发者指南
echo.
echo 常用命令:
echo   REM 从源码运行
echo   python src\zesigen.py --version
echo   python src\zesigen.py --help
echo   python src\zesigen.py --gui
echo   python src\zesigen.py --cli --url URL --output DIR
echo.
echo   REM 构建可执行文件
echo   pip install pyinstaller
echo   pyinstaller --onefile src\zesigen.py
echo.
echo   REM 安装为Python包
echo   pip install -e .
echo.
pause