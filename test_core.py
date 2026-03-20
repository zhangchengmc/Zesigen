#!/usr/bin/env python3
"""
Zesigen 核心功能测试
测试不依赖GUI的核心功能
"""

import sys
import os

def test_core_import():
    """测试核心模块导入"""
    print("测试核心模块导入...")
    try:
        # 将src目录添加到Python路径
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

        # 尝试导入核心模块（不导入GUI部分）
        import zesigen

        # 检查版本信息
        print(f"✓ 成功导入 Zesigen v{zesigen.__version__}")
        print(f"✓ 作者: {zesigen.__author__}")
        print(f"✓ 许可证: {zesigen.__license__}")

        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_downloader():
    """测试下载器类"""
    print("\n测试下载器类...")
    try:
        from zesigen import ZesigenDownloader

        downloader = ZesigenDownloader()

        # 测试文件名提取
        test_cases = [
            ("https://example.com/file.zip", "file.zip"),
            ("https://example.com/path/to/file.pdf", "file.pdf"),
            ("https://example.com/file.zip?param=value&other=123", "file.zip"),
            ("https://example.com/file.tar.gz", "file.tar.gz"),
        ]

        all_passed = True
        for url, expected in test_cases:
            result = downloader.get_filename_from_url(url)
            if result == expected:
                print(f"  ✓ {url} -> {result}")
            else:
                print(f"  ✗ {url} -> {result} (期望: {expected})")
                all_passed = False

        if all_passed:
            print("✓ 下载器类测试通过")
            return True
        else:
            print("✗ 下载器类测试失败")
            return False

    except Exception as e:
        print(f"✗ 下载器测试失败: {e}")
        return False

def test_argument_parsing():
    """测试参数解析"""
    print("\n测试参数解析...")
    try:
        from zesigen import main

        # 保存原始参数
        original_argv = sys.argv

        # 测试版本参数
        sys.argv = ['zesigen.py', '--version']
        try:
            main()
            print("✓ 版本参数测试通过")
        except SystemExit:
            print("✓ 版本参数测试通过 (正常退出)")

        # 测试帮助参数
        sys.argv = ['zesigen.py', '--help']
        try:
            main()
            print("✓ 帮助参数测试通过")
        except SystemExit:
            print("✓ 帮助参数测试通过 (正常退出)")

        # 恢复原始参数
        sys.argv = original_argv
        return True

    except Exception as e:
        print(f"✗ 参数解析测试失败: {e}")
        return False

def test_cli_interface():
    """测试命令行界面"""
    print("\n测试命令行界面...")
    try:
        from zesigen import CommandLineInterface

        cli = CommandLineInterface()

        # 测试版本显示
        print("测试版本显示:")
        cli.show_version()

        # 测试帮助显示
        print("\n测试帮助显示:")
        cli.show_help()

        print("✓ 命令行界面测试通过")
        return True

    except Exception as e:
        print(f"✗ 命令行界面测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("=" * 60)
    print("Zesigen 核心功能测试")
    print("=" * 60)

    tests = [
        test_core_import,
        test_downloader,
        test_argument_parsing,
        test_cli_interface,
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
        print("🎉 所有核心功能测试通过！")
        return 0
    else:
        print("⚠️  部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())