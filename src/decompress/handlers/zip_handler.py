import os
import zipfile
from typing import List

def is_zip_file(archive_path: str) -> bool:
    """检查是否为ZIP文件"""
    return archive_path.lower().endswith('.zip')

def list_zip_contents(archive_path: str) -> List[str]:
    """列出ZIP文件内容"""
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        return zip_ref.namelist()

def extract_zip(archive_path: str, extract_dir: str) -> bool:
    """解压ZIP文件"""
    try:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            # 解压所有文件
            zip_ref.extractall(extract_dir)
        print(f"[ZIP] 成功解压到: {extract_dir}")
        return True
    except Exception as e:
        print(f"[ZIP] 解压失败: {str(e)}")
        return False
