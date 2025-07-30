import os
from typing import List
try:
    import rarfile  # 需要安装 rarfile 库
except ImportError:
    print("警告: 未找到rarfile库，RAR解压功能不可用")
    rarfile = None

def is_rar_file(archive_path: str) -> bool:
    """检查是否为RAR文件"""
    return archive_path.lower().endswith('.rar')

def list_rar_contents(archive_path: str) -> List[str]:
    """列出RAR文件内容"""
    if not rarfile:
        raise ImportError("rarfile库未安装")

    with rarfile.RarFile(archive_path, 'r') as rar_ref:
        return rar_ref.namelist()

def extract_rar(archive_path: str, extract_dir: str) -> bool:
    """解压RAR文件（支持日语Shift-JIS编码）"""
    if not rarfile:
        print("[RAR] 请先安装rarfile库: pip install rarfile")
        return False

    try:
        # 指定编码为Shift-JIS以支持日语文件名
        with rarfile.RarFile(archive_path, 'r', encoding='shift_jis') as rar_ref:
            rar_ref.extractall(extract_dir)
        print(f"[RAR] 成功解压到: {extract_dir}")
        return True
    except Exception as e:
        print(f"[RAR] 解压失败: {str(e)}")
        return False
