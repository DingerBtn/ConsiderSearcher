import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from config import Config
import downloader
from decompress import decompress_file
from searcher import search_in_directory

def process_number(num, config):
    """处理单个序号的任务"""
    try:
        # 下载文件
        download_path = os.path.join(config.download_dir, str(num))
        success = downloader.download_specific_number(
            base_url=config.base_url,
            specific_num=num,
            save_dir=config.download_dir,
            timeout=config.timeout,
            max_workers=config.download_threads,
            chunk_size=config.chunk_size,
            retries=config.retries
        )
        
        if not success:
            return num, False, "下载失败"

        # 修改解压部分：遍历下载目录中的压缩文件
        zip_files = [f for f in os.listdir(download_path) 
                    if f.lower().endswith(('.zip', '.lzh', '.rar', '.7z'))]
        
        if not zip_files:
            return num, False, "无压缩文件"

        # 解压第一个找到的压缩文件（或遍历所有）
        extract_paths = []
        for zip_file in zip_files:
            extract_path = decompress_file(
                os.path.join(download_path, zip_file),  # 修改这里
                config.temp_dir,
                config.code_page,
                config.seven_zip_path
            )
            if extract_path:
                extract_paths.append(extract_path)

        if not extract_paths:
            return num, False, "解压失败"

        # 修改搜索部分：遍历所有解压路径
        found_keywords = []
        for path in extract_paths:
            search_in_directory(path, config.keywords, lambda f,k: found_keywords.extend(k))

        # 保留或删除
        if found_keywords:
            output_path = os.path.join(config.output_dir, str(num))
            shutil.move(download_path, output_path)
            return num, True, f"找到关键词: {', '.join(set(found_keywords))}"
        else:
            shutil.rmtree(download_path)
            return num, False, "未找到关键词"

    except Exception as e:
        return num, False, f"处理异常: {str(e)}"

def main():
    # 初始化配置
    config = Config()

    # 创建目录
    os.makedirs(config.download_dir, exist_ok=True)
    os.makedirs(config.output_dir, exist_ok=True)

    # 使用线程池处理
    with ThreadPoolExecutor(max_workers=config.max_workers) as executor:
        futures = [executor.submit(process_number, num, config) 
                 for num in range(config.start_num, config.end_num + 1)]
        
        # 实时输出结果
        for future in futures:
            num, success, message = future.result()
            log = f"序号 {num}: {message}"
            print(log)
            with open("search_results.log", "a") as f:
                f.write(log + "\n")

if __name__ == "__main__":
    main()
