import requests
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
import os
import threading
import webbrowser
import datetime

def get_filename_from_url(url):
    # 从下载链接中提取文件名.
    return os.path.basename(url)

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    with open(save_path, 'wb') as file:
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
        progress_bar.close()

def download_ftp_file(url, save_path):
    with open(save_path, 'wb') as file:
        response = requests.get(url)
        file.write(response.content)

def choose_save_location(file_name):
    root = tk.Tk()
    root.withdraw()
    save_path = filedialog.asksaveasfilename(defaultextension='.*', initialfile=file_name)
    return save_path

def is_html_file(file_path):
    # 检测文件扩展名是否是.html或.htm的文件名
    _, file_ext = os.path.splitext(file_path)
    return file_ext.lower() in ['.html', '.htm']

def open_url_in_browser(url):
    webbrowser.open(url)

def download_single_file(url, save_path):
    if url.startswith('ftp'):
        download_ftp_file(url, save_path)
    else:
        download_file(url, save_path)

    print(f"下载完成: {url}")

def download():
    urls = []

    # 输入多个链接，以空行结束输入
    print("请输入下载链接（每行一个链接）：")
    while True:
        url = input()
        if url:
            urls.append(url)
        else:
            break

    # 判断是否是4月1日
    current_date = datetime.date.today()
    is_april_fools_day = current_date.month == 4 and current_date.day == 1

    # 是否使用多线程下载
    use_multithread = input("是否使用多线程下载？(是/否): ").lower() in ['是', 'yes', '是的', 'y']

    if is_april_fools_day:
        print("今天是愚人节，程序即将闪退...")
    else:
        if use_multithread:
            # 输入多线程下载的线程数
            thread_count = int(input("请输入多线程下载的线程数："))

            print("开始下载...")
            threads = []

            for url in urls:
                if url == "Zesigen-Download-Manager-github":
                    open_url_in_browser("https://github.com/zhangchengmc/Zesigen-Download-Manager")
                elif url == "Zesigen-Download-Manager-debug":
                    print("触发调试模式，程序即将闪退...")
                else:
                    save_path = choose_save_location(get_filename_from_url(url))
                    thread = threading.Thread(target=download_single_file, args=(url, save_path))
                    threads.append(thread)
                    thread.start()

            for thread in threads:
                thread.join()

        else:
            print("开始单线程下载...")
            for url in urls:
                if url == "Zesigen-Download-Manager-github":
                    open_url_in_browser("https://github.com/zhangchengmc/Zesigen-Download-Manager")
                elif url == "Zesigen-Download-Manager-debug":
                    print("触发调试模式，程序即将闪退...")
                else:
                    save_path = choose_save_location(get_filename_from_url(url))
                    download_single_file(url, save_path)

        print("所有文件下载完成！")

if __name__ == '__main__':
    download()
