#!/usr/bin/env python3
"""
Zesigen - 跨平台下载管理器
安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取版本号
with open('src/zesigen.py', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'\"")
            break
    else:
        version = '1.0.0'

# 读取长描述
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# 读取依赖
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='zesigen',
    version=version,
    author='Zesigen Team',
    author_email='',
    description='跨平台下载管理器，支持命令行和图形界面',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zhangchengmc/Zesigen',
    packages=find_packages(),
    package_dir={'': 'src'},
    py_modules=['zesigen'],
    entry_points={
        'console_scripts': [
            'zesigen=zesigen:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
    ],
    keywords='download manager, http download, multi-threaded, gui, cli',
    python_requires='>=3.8',
    install_requires=requirements,
    extras_require={
        'dev': [
            'black',
            'flake8',
            'mypy',
            'pytest',
            'pytest-mock',
            'pre-commit',
        ],
        'build': [
            'pyinstaller>=5.0.0',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/zhangchengmc/Zesigen/issues',
        'Source': 'https://github.com/zhangchengmc/Zesigen',
        'Documentation': 'https://github.com/zhangchengmc/Zesigen/tree/main/docs',
    },
)