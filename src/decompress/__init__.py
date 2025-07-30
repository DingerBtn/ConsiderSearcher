# 暴露公共API
from .core import decompress_file
from .utils import ensure_temp_dir
from .handlers import (
    is_zip_file, extract_zip, list_zip_contents,
    is_lzh_file, extract_lzh, list_lzh_contents,
    is_rar_file, extract_rar, list_rar_contents
)

__all__ = [
    "decompress_file", "ensure_temp_dir",
    "is_zip_file", "extract_zip", "list_zip_contents",
    "is_lzh_file", "extract_lzh", "list_lzh_contents",
    "is_rar_file", "extract_rar", "list_rar_contents"
]
