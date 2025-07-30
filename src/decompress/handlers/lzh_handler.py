import os
from typing import List
try:
    from pylzh import LzhFile  # 需要安装 pylzh 库
except ImportError:
    print("警告: 未找到pylzh库，LZH解压功能不可用")
    LzhFile = None

def is_lzh_file(archive_path: str) -> bool:
    """检查是否为LZH文件"""
    return archive_path.lower().endswith('.lzh')

def list_lzh_contents(archive_path: str) -> List[str]:
    """列出LZH文件内容"""
    if not LzhFile:
        raise ImportError("pylzh库未安装")

    contents = []
    with LzhFile(archive_path, 'r') as lzh_ref:
        for entry in lzh_ref.infolist():
            contents.append(entry.filename)
    return contents

def extract_lzh(archive_path: str, extract_dir: str) -> bool:
    """解压LZH文件"""
    if not LzhFile:
        print("[LZH] 请先安装pylzh库: pip install pylzh")
        return False

    try:
        with LzhFile(archive_path, 'r') as lzh_ref:
            lzh_ref.extractall(extract_dir)
        print(f"[LZH] 成功解压到: {extract_dir}")
        return True
    except Exception as e:
        print(f"[LZH] 解压失败: {str(e)}")
        return False
