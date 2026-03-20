#!/usr/bin/env python3
"""
Zesigen - 跨平台下载管理器
支持命令行和图形界面两种模式
"""

import sys
import os
import argparse
import platform
import requests
from tqdm import tqdm
import threading
import datetime
import webbrowser
from typing import List, Optional
import queue

# GUI相关导入（可选）
GUI_AVAILABLE = True
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ImportError:
    GUI_AVAILABLE = False
    # 创建虚拟类以便类型提示
    class tk:
        Tk = None
        StringVar = None
        IntVar = None
        DISABLED = "disabled"
        END = "end"
        W = "w"
        E = "e"
        N = "n"
        S = "s"

    class ttk:
        Frame = None
        LabelFrame = None
        Button = None
        Label = None
        Entry = None
        Spinbox = None
        Treeview = None
        Scrollbar = None

    filedialog = None
    messagebox = None

__version__ = "1.0.0"
__author__ = "Zesigen Team"
__license__ = "MIT"

class ZesigenDownloader:
    """下载器核心类"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; Zesigen/1.0)'
        })

    def get_filename_from_url(self, url: str) -> str:
        """从URL中提取文件名"""
        filename = os.path.basename(url)
        if '?' in filename:
            filename = filename.split('?')[0]
        return filename

    def download_file(self, url: str, save_path: str, progress_callback=None) -> bool:
        """下载单个文件"""
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192

            with open(save_path, 'wb') as file:
                if progress_callback:
                    # 使用进度回调
                    downloaded = 0
                    for data in response.iter_content(block_size):
                        file.write(data)
                        downloaded += len(data)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(url, progress, downloaded, total_size)
                else:
                    # 使用tqdm进度条
                    with tqdm(total=total_size, unit='B', unit_scale=True,
                             desc=os.path.basename(save_path)) as pbar:
                        for data in response.iter_content(block_size):
                            file.write(data)
                            pbar.update(len(data))

            return True
        except Exception as e:
            print(f"下载失败 {url}: {e}")
            return False

    def download_multiple_files(self, urls: List[str], save_dir: str,
                               max_threads: int = 4, progress_callback=None) -> dict:
        """多线程下载多个文件"""
        results = {}
        url_queue = queue.Queue()

        # 将URL放入队列
        for url in urls:
            url_queue.put(url)

        def worker():
            while not url_queue.empty():
                try:
                    url = url_queue.get_nowait()
                    filename = self.get_filename_from_url(url)
                    save_path = os.path.join(save_dir, filename)

                    print(f"开始下载: {filename}")
                    success = self.download_file(url, save_path, progress_callback)
                    results[url] = success

                    if success:
                        print(f"下载完成: {filename}")
                    else:
                        print(f"下载失败: {filename}")

                    url_queue.task_done()
                except queue.Empty:
                    break

        # 创建并启动线程
        threads = []
        for i in range(min(max_threads, len(urls))):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        return results

class CommandLineInterface:
    """命令行界面"""

    def __init__(self):
        self.downloader = ZesigenDownloader()

    def show_version(self):
        """显示版本信息"""
        print(f"Zesigen Download Manager v{__version__}")
        print(f"Python {sys.version}")
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Author: {__author__}")
        print(f"License: {__license__}")

    def show_help(self):
        """显示帮助信息"""
        print("Zesigen - 跨平台下载管理器")
        print("\n使用方法:")
        print("  zesigen [选项]")
        print("\n选项:")
        print("  -h, --help           显示此帮助信息")
        print("  -v, --version        显示版本信息")
        print("  -g, --gui            启动图形界面")
        print("  -c, --cli            使用命令行界面")
        print("  -u URL, --url URL    指定下载URL")
        print("  -f FILE, --file FILE 从文件读取URL列表")
        print("  -o DIR, --output DIR 指定输出目录")
        print("  -t N, --threads N    指定线程数 (默认: 4)")
        print("\n示例:")
        print("  zesigen --version")
        print("  zesigen --gui")
        print("  zesigen --cli -u https://example.com/file.zip -o ./downloads")
        print("  zesigen --cli -f urls.txt -o ./downloads -t 8")

    def run_cli(self, args):
        """运行命令行模式"""
        if args.version:
            self.show_version()
            return

        if args.help or (not args.url and not args.file):
            self.show_help()
            return

        # 收集URL
        urls = []
        if args.url:
            urls.append(args.url)
        if args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            urls.append(line)
            except Exception as e:
                print(f"读取文件失败: {e}")
                return

        if not urls:
            print("错误: 没有指定下载URL")
            return

        # 设置输出目录
        output_dir = args.output or os.getcwd()
        os.makedirs(output_dir, exist_ok=True)

        print(f"开始下载 {len(urls)} 个文件到目录: {output_dir}")
        print(f"使用线程数: {args.threads}")

        # 执行下载
        results = self.downloader.download_multiple_files(
            urls, output_dir, args.threads
        )

        # 显示结果
        success_count = sum(1 for success in results.values() if success)
        print(f"\n下载完成: {success_count}/{len(urls)} 个文件成功下载")

        if success_count < len(urls):
            print("失败的URL:")
            for url, success in results.items():
                if not success:
                    print(f"  - {url}")

class GraphicalInterface:
    """图形界面"""

    def __init__(self):
        if not GUI_AVAILABLE:
            print("错误: GUI不可用。请安装tkinter或使用命令行模式。")
            print("在Ubuntu/Debian上: sudo apt-get install python3-tk")
            print("在macOS上: brew install python-tk")
            print("在Windows上: tkinter通常已包含在Python安装中")
            sys.exit(1)

        self.root = tk.Tk()
        self.root.title(f"Zesigen Download Manager v{__version__}")
        self.root.geometry("800x600")

        self.downloader = ZesigenDownloader()
        self.download_queue = []
        self.downloading = False

        self.setup_ui()

    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # URL输入区域
        url_frame = ttk.LabelFrame(main_frame, text="下载URL", padding="10")
        url_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.url_text = tk.Text(url_frame, height=5, width=70)
        self.url_text.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        ttk.Button(url_frame, text="从文件导入", command=self.import_urls).grid(row=1, column=0, padx=(0, 5))
        ttk.Button(url_frame, text="清空", command=self.clear_urls).grid(row=1, column=1)

        # 设置区域
        settings_frame = ttk.LabelFrame(main_frame, text="设置", padding="10")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10), padx=(0, 10))

        ttk.Label(settings_frame, text="输出目录:").grid(row=0, column=0, sticky=tk.W)
        self.output_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        ttk.Entry(settings_frame, textvariable=self.output_var, width=40).grid(row=0, column=1, padx=(5, 0))
        ttk.Button(settings_frame, text="浏览", command=self.browse_output).grid(row=0, column=2, padx=(5, 0))

        ttk.Label(settings_frame, text="线程数:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.threads_var = tk.IntVar(value=4)
        ttk.Spinbox(settings_frame, from_=1, to=16, textvariable=self.threads_var, width=10).grid(row=1, column=1, pady=(10, 0), padx=(5, 0))

        # 控制按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        ttk.Button(button_frame, text="开始下载", command=self.start_download).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="暂停", command=self.pause_download, state=tk.DISABLED).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="关于", command=self.show_about).grid(row=0, column=2)

        # 进度显示区域
        progress_frame = ttk.LabelFrame(main_frame, text="下载进度", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建树形视图显示下载进度
        columns = ("filename", "progress", "status")
        self.tree = ttk.Treeview(progress_frame, columns=columns, show="headings", height=10)

        self.tree.heading("filename", text="文件名")
        self.tree.heading("progress", text="进度")
        self.tree.heading("status", text="状态")

        self.tree.column("filename", width=300)
        self.tree.column("progress", width=100)
        self.tree.column("status", width=100)

        scrollbar = ttk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="日志", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        self.log_text = tk.Text(log_frame, height=8, width=70)
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 配置网格权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

    def log(self, message: str):
        """添加日志"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()

    def import_urls(self):
        """从文件导入URL"""
        filepath = filedialog.askopenfilename(
            title="选择URL文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    self.url_text.insert(tk.END, '\n'.join(urls) + '\n')
                self.log(f"从 {filepath} 导入了 {len(urls)} 个URL")
            except Exception as e:
                messagebox.showerror("错误", f"读取文件失败: {e}")

    def clear_urls(self):
        """清空URL列表"""
        self.url_text.delete(1.0, tk.END)

    def browse_output(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_var.set(directory)

    def start_download(self):
        """开始下载"""
        if self.downloading:
            return

        # 获取URL列表
        urls_text = self.url_text.get(1.0, tk.END).strip()
        if not urls_text:
            messagebox.showwarning("警告", "请输入下载URL")
            return

        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]

        # 检查输出目录
        output_dir = self.output_var.get()
        if not output_dir:
            messagebox.showwarning("警告", "请选择输出目录")
            return

        os.makedirs(output_dir, exist_ok=True)

        # 清空进度显示
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 添加下载任务到树形视图
        self.download_items = {}
        for url in urls:
            filename = self.downloader.get_filename_from_url(url)
            item_id = self.tree.insert("", tk.END, values=(filename, "0%", "等待"))
            self.download_items[url] = item_id

        self.log(f"开始下载 {len(urls)} 个文件到: {output_dir}")
        self.downloading = True

        # 在新线程中执行下载
        download_thread = threading.Thread(
            target=self.execute_download,
            args=(urls, output_dir, self.threads_var.get())
        )
        download_thread.daemon = True
        download_thread.start()

    def execute_download(self, urls: List[str], output_dir: str, max_threads: int):
        """执行下载任务"""
        def progress_callback(url: str, progress: float, downloaded: int, total: int):
            # 更新进度显示
            item_id = self.download_items.get(url)
            if item_id:
                progress_str = f"{progress:.1f}%"
                status = "下载中"
                if progress >= 100:
                    status = "完成"

                self.tree.item(item_id, values=(
                    self.downloader.get_filename_from_url(url),
                    progress_str,
                    status
                ))

            # 更新日志
            filename = self.downloader.get_filename_from_url(url)
            self.log(f"{filename}: {progress:.1f}% ({downloaded}/{total} bytes)")

        # 执行下载
        results = self.downloader.download_multiple_files(
            urls, output_dir, max_threads, progress_callback
        )

        # 下载完成
        success_count = sum(1 for success in results.values() if success)
        self.log(f"下载完成: {success_count}/{len(urls)} 个文件成功下载")

        if success_count == len(urls):
            messagebox.showinfo("完成", f"所有文件下载完成！\n保存到: {output_dir}")
        else:
            messagebox.showwarning("完成",
                f"下载完成: {success_count}/{len(urls)} 个文件成功下载\n请查看日志了解详情")

        self.downloading = False

    def pause_download(self):
        """暂停下载"""
        # TODO: 实现暂停功能
        pass

    def show_about(self):
        """显示关于对话框"""
        about_text = f"""Zesigen Download Manager
版本: {__version__}
作者: {__author__}
许可证: {__license__}

一个跨平台的下载管理器，支持命令行和图形界面。
"""
        messagebox.showinfo("关于 Zesigen", about_text)

    def run(self):
        """运行GUI"""
        self.root.mainloop()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Zesigen - 跨平台下载管理器",
        add_help=False
    )

    parser.add_argument("-h", "--help", action="store_true", help="显示帮助信息")
    parser.add_argument("-v", "--version", action="store_true", help="显示版本信息")
    parser.add_argument("-g", "--gui", action="store_true", help="启动图形界面")
    parser.add_argument("-c", "--cli", action="store_true", help="使用命令行界面")
    parser.add_argument("-u", "--url", help="指定下载URL")
    parser.add_argument("-f", "--file", help="从文件读取URL列表")
    parser.add_argument("-o", "--output", help="指定输出目录")
    parser.add_argument("-t", "--threads", type=int, default=4, help="指定线程数 (默认: 4)")

    args = parser.parse_args()

    # 如果没有指定任何参数，显示版本信息
    if len(sys.argv) == 1:
        cli = CommandLineInterface()
        cli.show_version()
        return

    # 处理参数
    if args.gui:
        # 启动GUI模式
        if not GUI_AVAILABLE:
            print("错误: GUI不可用。请安装tkinter或使用命令行模式。")
            print("在Ubuntu/Debian上: sudo apt-get install python3-tk")
            print("在macOS上: brew install python-tk")
            print("在Windows上: tkinter通常已包含在Python安装中")
            print("\n使用命令行模式: zesigen --cli --help")
            sys.exit(1)
        gui = GraphicalInterface()
        gui.run()
    elif args.cli or args.url or args.file:
        # 启动CLI模式
        cli = CommandLineInterface()
        cli.run_cli(args)
    elif args.version:
        # 显示版本
        cli = CommandLineInterface()
        cli.show_version()
    elif args.help:
        # 显示帮助
        cli = CommandLineInterface()
        cli.show_help()
    else:
        # 默认显示帮助
        cli = CommandLineInterface()
        cli.show_help()

if __name__ == "__main__":
    main()