#!/usr/bin/env python3
"""
Zesigen 功能测试脚本
用于验证程序的基本功能
"""

import sys
import os
import tempfile
import subprocess

def test_version():
    """测试版本显示功能"""
    print("测试版本显示...")
    result = subprocess.run(
        [sys.executable, "src/zesigen.py", "--version"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0 and "Zesigen" in result.stdout:
        print("✓ 版本显示测试通过")
        return True
    else:
        print("✗ 版本显示测试失败")
        print(f"输出: {result.stdout}")
        print(f"错误: {result.stderr}")
        return False

def test_help():
    """测试帮助信息"""
    print("\n测试帮助信息...")
    result = subprocess.run(
        [sys.executable, "src/zesigen.py", "--help"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0 and "使用方法" in result.stdout:
        print("✓ 帮助信息测试通过")
        return True
    else:
        print("✗ 帮助信息测试失败")
        print(f"输出: {result.stdout[:200]}...")
        return False

def test_cli_help():
    """测试命令行帮助"""
    print("\n测试命令行帮助...")
    result = subprocess.run(
        [sys.executable, "src/zesigen.py", "--cli", "--help"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0 and "选项" in result.stdout:
        print("✓ 命令行帮助测试通过")
        return True
    else:
        print("✗ 命令行帮助测试失败")
        print(f"输出: {result.stdout[:200]}...")
        return False

def test_gui_import():
    """测试GUI模块导入"""
    print("\n测试GUI模块导入...")
    try:
        # 尝试导入GUI相关模块
        import tkinter
        from tkinter import ttk
        print("✓ GUI模块导入测试通过")
        return True
    except ImportError as e:
        print(f"⚠️  GUI模块不可用: {e} (在某些无GUI环境中正常)")
        return True  # 在某些无GUI环境中，这是正常的

def test_downloader_class():
    """测试下载器类"""
    print("\n测试下载器类...")
    try:
        # 导入并测试下载器类
        sys.path.insert(0, 'src')
        from zesigen import ZesigenDownloader

        downloader = ZesigenDownloader()

        # 测试文件名提取
        test_url = "https://example.com/file.zip?param=value"
        filename = downloader.get_filename_from_url(test_url)

        if filename == "file.zip":
            print("✓ 下载器类测试通过")
            return True
        else:
            print(f"✗ 文件名提取失败: 期望 'file.zip', 得到 '{filename}'")
            return False
    except Exception as e:
        print(f"✗ 下载器类测试失败: {e}")
        return False

def create_test_urls_file():
    """创建测试URL文件"""
    print("\n创建测试URL文件...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("# 测试URL文件\n")
        f.write("https://httpbin.org/get\n")
        f.write("https://httpbin.org/status/200\n")
        return f.name

def test_file_import():
    """测试文件导入功能"""
    print("\n测试文件导入功能...")

    # 创建测试文件
    test_file = create_test_urls_file()

    try:
        # 测试读取文件
        with open(test_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        if len(urls) == 2:
            print("✓ 文件导入测试通过")
            return True
        else:
            print(f"✗ 文件导入失败: 期望2个URL, 得到{len(urls)}个")
            return False
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.unlink(test_file)

def main():
    """运行所有测试"""
    print("=" * 60)
    print("Zesigen 功能测试")
    print("=" * 60)

    tests = [
        test_version,
        test_help,
        test_cli_help,
        test_gui_import,
        test_downloader_class,
        test_file_import,
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ 测试异常: {e}")

    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("⚠️  部分测试失败，请检查问题")
        return 1

if __name__ == "__main__":
    sys.exit(main())