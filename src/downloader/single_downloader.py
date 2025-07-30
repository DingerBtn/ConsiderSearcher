import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from .session import get_http_session
from .core import download_file

def download_specific_number(base_url, specific_num, save_dir, timeout, max_workers, chunk_size, retries):
    """下载特定序号的文件夹"""
    session = get_http_session(max_workers)
    dir_url = urljoin(base_url, f"{specific_num}/")
    print(f"\n🔍 检查特定目录: {dir_url}")

    try:
        # 检查目录是否存在
        r = session.head(dir_url, timeout=5)
        if r.status_code != 200:
            print(f"❌ 目录不存在: {specific_num}")
            return False

        # 获取文件列表
        r = session.get(dir_url, timeout=timeout)
        soup = BeautifulSoup(r.text, 'html.parser')
        files = []
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and not href.startswith(('../', './')) and not href.endswith('/'):
                files.append(urljoin(dir_url, href))

        if not files:
            print(f"⚠️ 空目录: {specific_num}")
            return True

        # 创建保存目录并下载文件
        save_path = os.path.join(save_dir, str(specific_num))
        os.makedirs(save_path, exist_ok=True)
        print(f"📁 开始下载目录 {specific_num} ({len(files)} 个文件)")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for file_url in files:
                local_path = os.path.join(save_path, os.path.basename(urlparse(file_url).path))
                futures.append(executor.submit(
                    download_file, session, file_url, local_path, timeout, chunk_size, retries
                ))

            # 等待所有文件下载完成
            for future in as_completed(futures):
                future.result()

        print(f"✅ 完成特定目录下载: {specific_num}")
        return True

    except Exception as e:
        print(f"❌ 下载失败: {str(e)}")
        return False
