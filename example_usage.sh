#!/bin/bash
# Zesigen 使用示例脚本
# 展示如何使用 Zesigen 的各种功能

echo "=== Zesigen 使用示例 ==="
echo ""

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 检查Python是否可用
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3"
    exit 1
fi

echo "1. 显示版本信息"
echo "------------------------"
python3 src/zesigen.py --version
echo ""

echo "2. 显示帮助信息"
echo "------------------------"
python3 src/zesigen.py --help
echo ""

echo "3. 显示命令行帮助"
echo "------------------------"
python3 src/zesigen.py --cli --help
echo ""

echo "4. 测试下载器功能"
echo "------------------------"
# 创建测试目录
TEST_DIR="./test_downloads"
mkdir -p "$TEST_DIR"

# 创建测试URL文件
cat > test_urls.txt << EOF
# 测试URL文件
https://httpbin.org/image/jpeg
https://httpbin.org/image/png
EOF

echo "创建了测试URL文件: test_urls.txt"
echo "测试下载目录: $TEST_DIR"
echo ""

echo "5. 运行功能测试"
echo "------------------------"
if python3 test_core.py; then
    echo "✓ 核心功能测试通过"
else
    echo "✗ 核心功能测试失败"
fi
echo ""

echo "6. 清理测试文件"
echo "------------------------"
if [ -d "$TEST_DIR" ]; then
    rm -rf "$TEST_DIR"
    echo "已删除测试目录: $TEST_DIR"
fi

if [ -f "test_urls.txt" ]; then
    rm -f "test_urls.txt"
    echo "已删除测试文件: test_urls.txt"
fi

echo ""
echo "=== 示例完成 ==="
echo ""
echo "更多用法请参考:"
echo "  - README.md - 项目说明和快速开始"
echo "  - docs/USER_GUIDE.md - 详细用户指南"
echo "  - docs/DEVELOPER_GUIDE.md - 开发者指南"
echo ""
echo "常用命令:"
echo "  # 从源码运行"
echo "  python src/zesigen.py --version"
echo "  python src/zesigen.py --help"
echo "  python src/zesigen.py --gui"
echo "  python src/zesigen.py --cli --url URL --output DIR"
echo ""
echo "  # 构建可执行文件"
echo "  pip install pyinstaller"
echo "  pyinstaller --onefile src/zesigen.py"
echo ""
echo "  # 安装为Python包"
echo "  pip install -e ."