import os
# 从 utils 导入 extract_with_7z，但不再需要 ensure_temp_dir
from .utils import extract_with_7z

def decompress_file(archive_path: str, output_dir: str = None, code_page: int = None) -> str:
    """
    解压压缩文件到指定目录 (使用 7-Zip)

    Args:
        archive_path: 压缩文件路径 (必须是绝对路径或相对于当前工作目录的有效路径)
        output_dir: 自定义解压根目录路径。
                    如果为 None，则解压到压缩文件所在的目录。
        code_page: 文件名编码代码页。
                   如果为 None，则 extract_with_7z 使用其默认值 (932)。

    Returns:
        解压目录的绝对路径，如果失败则返回空字符串。
        - 如果 output_dir 被指定，解压到 {output_dir}/{archive_name_without_ext}/
        - 如果 output_dir 未指定，解压到 {archive_dir}/{archive_name_without_ext}/
    """
    if not os.path.exists(archive_path):
        print(f"错误: 文件不存在 - {archive_path}")
        return ""

    archive_path = os.path.abspath(archive_path)  # 确保是绝对路径
    archive_dir = os.path.dirname(archive_path)
    archive_name_no_ext = os.path.splitext(os.path.basename(archive_path))[0]

    # 确定最终的解压目录
    if output_dir:
        # 如果指定了 output_dir，则在其中创建与压缩文件同名的子目录
        final_extract_dir = os.path.join(os.path.abspath(output_dir), archive_name_no_ext)
    else:
        # 如果未指定 output_dir，则在压缩文件同目录下创建同名子目录
        final_extract_dir = os.path.join(archive_dir, archive_name_no_ext)

    # 确保解压目录存在
    # 注意：extract_with_7z 使用 -y 参数覆盖，我们不主动清空目录
    os.makedirs(final_extract_dir, exist_ok=True)

    # 调用 7-Zip 解压函数
    success = extract_with_7z(archive_path, final_extract_dir, code_page)

    # 返回解压目录的绝对路径或空字符串
    return os.path.abspath(final_extract_dir) if success else ""