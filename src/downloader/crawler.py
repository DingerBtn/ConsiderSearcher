import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from .session import get_http_session
from .core import download_file

def crawl_from_number(base_url, start_num, save_dir, timeout, max_workers, chunk_size, retries, end_num=None):
    """高性能爬取"""
    session = get_http_session(max_workers)
    current_num = start_num

    while True:
        # 新增结束序号检查
        if end_num is not None and current_num > end_num:
            print(f"✅ 已达到指定结束序号 {end_num}")
            return True

        dir_url = urljoin(base_url, f"{current_num}/")
        print(f"\n🔍 检查目录: {dir_url}")

        try:
            # 快速目录检测
            r = session.head(dir_url, timeout=5)
            if r.status_code != 200:
                print(f"❌ 目录不存在: {current_num}")
                current_num += 1
                continue

            # 获取文件列表
            r = session.get(dir_url, timeout=timeout)
            soup = BeautifulSoup(r.text, 'html.parser')
            files = []
            for a in soup.find_all('a'):
                href = a.get('href')
                if href and not href.startswith(('../', './')) and not href.endswith('/'):
                    files.append(urljoin(dir_url, href))

            if not files:
                print(f"⚠️ 空目录: {current_num}")
                current_num += 1
                continue

            # 并发下载
            os.makedirs(os.path.join(save_dir, str(current_num)), exist_ok=True)
            print(f"📁 开始下载目录 {current_num} ({len(files)} 个文件)")

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for file_url in files:
                    local_path = os.path.join(save_dir, str(current_num),
                                            os.path.basename(urlparse(file_url).path))
                    futures.append(executor.submit(download_file, session, file_url, local_path, timeout, chunk_size, retries))

                # 实时显示进度
                for future in as_completed(futures):
                    future.result()

            print(f"✅ 完成目录: {current_num}")
            current_num += 1

        except KeyboardInterrupt:
            print("\n🛑 用户中断")
            break
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            current_num += 1
