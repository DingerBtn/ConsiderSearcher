from decompress import decompress_file

# 解压ZIP文件
extract_path = decompress_file("D:\\freem\\100\\hunterlife2_t.zip")
if extract_path:
    print(f"文件已解压到: {extract_path}")

# 解压LZH文件
# extract_path = decompress_file("D:/downloads/archive.lzh")

# 解压RAR文件
# extract_path = decompress_file("D:/downloads/data.rar")
