#!/usr/bin/env python3
"""
Zesigen 构建测试脚本
测试PyInstaller构建过程
"""

import os
import sys
import subprocess
import tempfile
import shutil

def test_pyinstaller_available():
    """测试PyInstaller是否可用"""
    print("测试PyInstaller是否可用...")
    try:
        import PyInstaller
        print(f"✓ PyInstaller版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("✗ PyInstaller未安装")
        print("安装命令: pip install pyinstaller")
        return False

def test_build_onefile():
    """测试单文件构建"""
    print("\n测试单文件构建...")

    # 创建临时构建目录
    build_dir = tempfile.mkdtemp(prefix="zesigen_build_")
    dist_dir = os.path.join(build_dir, "dist")

    try:
        # 运行PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name", "zesigen-test",
            "--distpath", dist_dir,
            "--workpath", os.path.join(build_dir, "build"),
            "--specpath", build_dir,
            "src/zesigen.py"
        ]

        print(f"运行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            # 检查生成的可执行文件
            exe_path = os.path.join(dist_dir, "zesigen-test.exe")
            if os.path.exists(exe_path):
                print(f"✓ 单文件构建成功: {exe_path}")

                # 测试运行可执行文件
                print("测试运行构建的可执行文件...")
                test_result = subprocess.run(
                    [exe_path, "--version"],
                    capture_output=True,
                    text=True
                )

                if test_result.returncode == 0 and "Zesigen" in test_result.stdout:
                    print("✓ 构建的可执行文件运行正常")
                    return True
                else:
                    print("✗ 构建的可执行文件运行失败")
                    print(f"输出: {test_result.stdout}")
                    print(f"错误: {test_result.stderr}")
                    return False
            else:
                print("✗ 可执行文件未生成")
                return False
        else:
            print("✗ PyInstaller构建失败")
            print(f"错误输出: {result.stderr}")
            return False

    finally:
        # 清理临时目录
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir, ignore_errors=True)

def test_build_folder():
    """测试文件夹构建"""
    print("\n测试文件夹构建...")

    # 创建临时构建目录
    build_dir = tempfile.mkdtemp(prefix="zesigen_build_folder_")
    dist_dir = os.path.join(build_dir, "dist")

    try:
        # 运行PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name", "zesigen-folder-test",
            "--distpath", dist_dir,
            "--workpath", os.path.join(build_dir, "build"),
            "--specpath", build_dir,
            "src/zesigen.py"
        ]

        print(f"运行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            # 检查生成的文件夹
            folder_path = os.path.join(dist_dir, "zesigen-folder-test")
            if os.path.exists(folder_path):
                print(f"✓ 文件夹构建成功: {folder_path}")

                # 检查文件夹内容
                exe_path = os.path.join(folder_path, "zesigen-folder-test.exe")
                if os.path.exists(exe_path):
                    print(f"✓ 可执行文件存在: {exe_path}")

                    # 列出文件夹内容
                    print("文件夹内容:")
                    for item in os.listdir(folder_path):
                        print(f"  - {item}")

                    return True
                else:
                    print("✗ 可执行文件不存在")
                    return False
            else:
                print("✗ 文件夹未生成")
                return False
        else:
            print("✗ PyInstaller构建失败")
            print(f"错误输出: {result.stderr}")
            return False

    finally:
        # 清理临时目录
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir, ignore_errors=True)

def main():
    """运行所有构建测试"""
    print("=" * 60)
    print("Zesigen 构建测试")
    print("=" * 60)

    tests = [
        test_pyinstaller_available,
        test_build_onefile,
        test_build_folder,
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ 测试异常: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"构建测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有构建测试通过！")
        return 0
    else:
        print("⚠️  部分构建测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())