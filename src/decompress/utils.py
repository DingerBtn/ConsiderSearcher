import subprocess

def extract_with_7z(src_path, dest_path=None, code_page=932):
    """
    使用7z.exe解压缩文件，并指定文件名编码

    参数：
        src_path: 压缩包路径（绝对路径或相对路径）
        dest_path: 解压目标路径（None则默认当前目录）
        code_page: 编码对应的代码页（None则默认为932）
    """
    # 7z.exe路径（若已添加到环境变量，直接用"7z"即可）
    seven_zip_path = "C:/Program Files/7-Zip/7z.exe"

    # 构建命令：7z x 源文件 -o目标路径 -mcp=代码页
    cmd = [seven_zip_path, "x", src_path, "-y"] # -y 表示覆盖所有文件
    if dest_path:
        cmd.extend(["-o" + dest_path])  # 添加输出路径
    cmd.extend(["-mcp=" + str(code_page)])  # 指定编码代码页

    # 执行命令
    try:
        result = subprocess.run(
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