import os
import time
from .utils import format_speed

def download_file(session, url, local_path, timeout, chunk_size, retries):
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
