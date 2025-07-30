import os
from .utils import ensure_temp_dir
from .handlers import (
    is_zip_file, extract_zip,
    is_lzh_file, extract_lzh,
    is_rar_file, extract_rar
)

def decompress_file(archive_path: str) -> str:
    """
    解压压缩文件到指定目录

    Args:
        archive_path: 压缩文件路径

    Returns:
        解压目录路径，如果失败则返回空字符串
    """
    if not os.path.exists(archive_path):
        print(f"错误: 文件不存在 - {archive_path}")
        return ""

    # 确保temp目录存在并获取解压路径
    extract_dir = ensure_temp_dir(archive_path)

    # 根据文件类型选择对应的解压方法
    if is_zip_file(archive_path):
        success = extract_zip(archive_path, extract_dir)
    elif is_lzh_file(archive_path):
        success = extract_lzh(archive_path, extract_dir)
    elif is_rar_file(archive_path):
        success = extract_rar(archive_path, extract_dir)
    else:
        print(f"错误: 不支持的文件格式 - {archive_path}")
        return ""

    return extract_dir if success else ""
