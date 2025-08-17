from decompress import decompress_file

# 解压文件
extract_path = decompress_file("ude_onara.zip","temp",932)
if extract_path:
    print(f"文件已解压到: {extract_path}")
