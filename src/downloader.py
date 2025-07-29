import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from urllib.parse import urljoin, urlparse
import time

# 全局配置
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

def get_http_session(max_workers):
    """创建高性能HTTP会话"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Encoding": "gzip, deflate",  # 启用压缩
    })
    # 扩大连接池
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=max_workers,
        pool_maxsize=max_workers * 2
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def format_speed(speed):
    """格式化速度显示"""
    if speed >= 1024 * 1024:
        return f"{speed/(1024 * 1024):.2f} MB/s"
    return f"{speed/1024:.2f} KB/s"

def download_file(session, url, local_path, timeout ,chunk_size, retries):
    """增强版下载函数（带速度显示）"""
    if os.path.exists(local_path):
        print(f"[跳过] 文件已存在: {os.path.basename(local_path)}")
        return True

    for attempt in range(retries):
        try:
            start_time = time.time()
            downloaded = 0
            last_update = start_time

            with session.get(url, stream=True, timeout=timeout) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))

                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # 每秒更新显示
                            now = time.time()
                            if now - last_update >= 0.5:
                                elapsed = now - start_time
                                speed = downloaded / elapsed if elapsed > 0 else 0
                                progress = f"{downloaded/1024/1024:.2f}MB" if total_size ==0 else \
                                         f"{downloaded/1024/1024:.2f}/{total_size/1024/1024:.2f}MB"
                                print(
                                    f"\r[下载] {os.path.basename(local_path)} "
                                    f"{progress} | {format_speed(speed)}".ljust(80),
                                    end=""
                                )
                                last_update = now

            # 最终速度计算
            elapsed = time.time() - start_time
            if elapsed == 0:
                elapsed = 0.001
            speed = downloaded / elapsed
            print(f"\r[完成] {os.path.basename(local_path)} "
                f"({downloaded/1024/1024:.2f}MB @ {format_speed(speed)})".ljust(80))
            return True

        except Exception as e:
            print(f"\r[重试 {attempt+1}/{retries}] {url} 错误: {str(e)}")
            time.sleep(1)
    
    return False

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

if __name__ == "__main__":
    print("🚀 FreeM 高性能下载器 v2")
    BASE_URL = "http://ftp.airnet.ne.jp/pub/pc/freem/"
    SAVE_DIR = input("保存路径（例如 D:/freem）: ").strip()
    START_NUM = int(input("起始编号（例如 731）: ") or 1)
    # 新增结束序号输入
    end_input = input("结束编号（留空则不限制）: ").strip()
    END_NUM = int(end_input) if end_input else None

    TIMEOUT = 30
    MAX_WORKERS = 12
    CHUNK_SIZE = 1024 * 128
    RETRIES = 3

    start_time = time.time()

    crawl_from_number(
        base_url=BASE_URL,
        start_num=START_NUM,
        save_dir=SAVE_DIR,
        timeout=TIMEOUT,
        max_workers=MAX_WORKERS,
        chunk_size=CHUNK_SIZE,
        retries=RETRIES,
        end_num = END_NUM  # 新增参数
    )
    print(f"⏱️ 总耗时: {time.time()-start_time:.2f}秒")