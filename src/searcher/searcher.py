import os
import tempfile
from typing import List, Set
from .midi2text import read_midi_text_messages
from ..decompress.core import decompress_file

# 支持的纯文本文件扩展名
TEXT_EXTENSIONS = {
    '.txt', '.htm', '.html', '.md', '.rst',
    '.int', '.sh', '.bat', '.csv', '.yml',
    '.yaml', '.toml', '.tex', '.bib'
}

# MIDI文件扩展名
MIDI_EXTENSIONS = {'.mid', '.midi'}

def create_temp_directory(base_path: str) -> str:
    """
    在指定路径下创建一个临时目录，如果temp已存在则创建temptemp等

    Args:
        base_path: 基础路径

    Returns:
        创建的临时目录路径
    """
    temp_name = "temp"
    temp_path = os.path.join(base_path, temp_name)

    # 如果temp目录已存在，创建temptemp, temptemptemp等
    counter = 1
    while os.path.exists(temp_path):
        temp_name = "temp" * (counter + 1)
        temp_path = os.path.join(base_path, temp_name)
        counter += 1

    os.makedirs(temp_path, exist_ok=True)
    return temp_path

def search_in_text_file(file_path: str, keywords: List[str]) -> List[str]:
    """
    在文本文件中搜索关键词

    Args:
        file_path: 文本文件路径
        keywords: 关键词列表

    Returns:
        匹配到的关键词列表
    """
    matched_keywords = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()

        for keyword in keywords:
            if keyword.lower() in content:
                matched_keywords.append(keyword)
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")

    return matched_keywords

def search_in_midi_file(file_path: str, keywords: List[str]) -> List[str]:
    """
    在MIDI文件中搜索文本消息中的关键词

    Args:
        file_path: MIDI文件路径
        keywords: 关键词列表

    Returns:
        匹配到的关键词列表
    """
    matched_keywords = []
    try:
        # 读取MIDI文件中的文本消息
        text_messages = read_midi_text_messages(file_path)

        # 将所有文本消息合并为一个字符串进行搜索
        all_text = ' '.join([msg['text'] for msg in text_messages]).lower()

        for keyword in keywords:
            if keyword.lower() in all_text:
                matched_keywords.append(keyword)
    except Exception as e:
        print(f"读取MIDI文件 {file_path} 时出错: {e}")

    return matched_keywords

def search_in_directory(directory_path: str, keywords: List[str], config_path: str = None):
    """
    在指定目录中搜索包含关键词的文件

    Args:
        directory_path: 要搜索的目录路径
        keywords: 关键词列表
        config_path: 配置文件路径（如果为None，则使用默认配置）
    """
    if not os.path.exists(directory_path):
        print(f"错误: 目录 {directory_path} 不存在")
        return

    # 如果配置文件路径未提供，使用默认路径
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'keywords.txt')

    # 如果提供了关键词列表，则使用它；否则从配置文件读取
    if not keywords:
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    keywords = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"读取配置文件 {config_path} 时出错: {e}")
                return
        else:
            print(f"错误: 配置文件 {config_path} 不存在")
            return

    print(f"开始在目录 {directory_path} 中搜索关键词...")

    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[-1].lower()

            # 处理压缩文件
            if file_ext in ['.zip', '.rar', '.7z', '.lzh']:
                print(f"发现压缩文件: {file_path}")
                # 创建临时目录解压文件
                temp_dir = create_temp_directory(root)
                print(f"创建临时目录: {temp_dir}")

                # 解压文件
                extract_path = decompress_file(file_path, temp_dir)
                if extract_path:
                    # 递归搜索解压后的目录
                    search_in_directory(extract_path, keywords, config_path)
                continue

            # 处理纯文本文件
            if file_ext in TEXT_EXTENSIONS:
                matched = search_in_text_file(file_path, keywords)
                if matched:
                    print(f"在文本文件 {file_path} 中找到关键词: {', '.join(matched)}")
                continue

            # 处理MIDI文件
            if file_ext in MIDI_EXTENSIONS:
                matched = search_in_midi_file(file_path, keywords)
                if matched:
                    print(f"在MIDI文件 {file_path} 中找到关键词: {', '.join(matched)}")
                continue

# 示例用法
if __name__ == "__main__":
    # 示例关键词
    example_keywords = ["title", "rpg", "music"]

    search_in_directory("J:/1/ude_onara", example_keywords)
