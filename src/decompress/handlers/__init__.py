# 导入所有处理器
from .zip_handler import is_zip_file, extract_zip, list_zip_contents
from .lzh_handler import is_lzh_file, extract_lzh, list_lzh_contents
from .rar_handler import is_rar_file, extract_rar, list_rar_contents

__all__ = [
    # ZIP相关
    "is_zip_file", "extract_zip", "list_zip_contents",
    # LZH相关
    "is_lzh_file", "extract_lzh", "list_lzh_contents",
    # RAR相关
    "is_rar_file", "extract_rar", "list_rar_contents"
]
