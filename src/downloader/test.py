import time
from .crawler import crawl_from_number

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
        end_num=END_NUM
    )
    print(f"⏱️ 总耗时: {time.time()-start_time:.2f}秒")
