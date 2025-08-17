import os
import subprocess


def decompress_file(archive_path: str, output_dir: str = None, code_page: int = None, seven_zip_path: str = "7z") -> str:
    """
    解压压缩文件到指定目录 (使用 7-Zip)

    Args:
        :param archive_path: 压缩文件路径 (必须是绝对路径或相对于当前工作目录的有效路径)
        :param output_dir: 自定义解压根目录路径。
                    如果为 None，则解压到压缩文件所在的目录。
        :param code_page: 文件名编码代码页。
                   如果为 None，则 extract_with_7z 使用其默认值 (932)。
        :param seven_zip_path: 7z.exe路径（若已添加到环境变量，直接用"7z"即可）,默认"7z"
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

    def extract_with_7z(src_path, dest_path=None, code_page=932, seven_zip_path: str = "7z"):
        """
        使用7z.exe解压缩文件，并指定文件名编码

        :param src_path: 压缩包路径（绝对路径或相对路径）
        :param dest_path: 解压目标路径（None则默认当前目录）
        :param code_page: 编码对应的代码页（None则默认为932）
        :param seven_zip_path: 7z.exe路径（若已添加到环境变量，直接用"7z"即可）,默认"7z"
        """
        # 构建命令：7z x 源文件 -o目标路径 -mcp=代码页
        cmd = [seven_zip_path, "x", src_path, "-y"]  # -y 表示覆盖所有文件
        if dest_path:
            cmd.extend(["-o" + dest_path])  # 添加输出路径
        cmd.extend(["-mcp=" + str(code_page)])  # 指定编码代码页

        # 执行命令
        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # 输出以文本形式返回（需Python 3.7+）
            )
            print(f"[7Z] 解压成功：{src_path} -> {dest_path or '当前目录'}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[7Z] 解压失败：{e.stderr}")
            return False
        except FileNotFoundError:
            print(f"[7Z] 错误: 找不到 7-Zip 程序 '{seven_zip_path}'。请确保 7-Zip 已安装并添加到系统环境变量 PATH 中。")
            return False

    # 调用 7-Zip 解压函数
    success = extract_with_7z(archive_path, final_extract_dir, code_page, seven_zip_path)

    # 返回解压目录的绝对路径或空字符串
    return os.path.abspath(final_extract_dir) if success else ""