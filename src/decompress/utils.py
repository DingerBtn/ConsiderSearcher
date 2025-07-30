import os
import shutil

def ensure_temp_dir(archive_path):
    """确保temp目录存在并返回解压目标路径"""
    # 获取压缩文件所在目录
    archive_dir = os.path.dirname(archive_path)
    # 获取压缩文件名（不含扩展名）
    archive_name = os.path.splitext(os.path.basename(archive_path))[0]
    # 创建temp目录路径
    temp_dir = os.path.join(archive_dir, "temp")
    # 创建同名解压目录路径
    extract_dir = os.path.join(temp_dir, archive_name)

    # 确保temp目录存在
    os.makedirs(temp_dir, exist_ok=True)

    # 如果目标目录已存在，先清空
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)

    # 创建目标解压目录
    os.makedirs(extract_dir, exist_ok=True)

    return extract_dir
