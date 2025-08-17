from decompress import decompress_file

# 解压文件
# 7z.exe路径（若已添加到环境变量，直接用"7z"即可）
seven_zip_path = "C:/Program Files/7-Zip/7z.exe"
extract_path = decompress_file("ude_onara.zip","temp",932,"C:/Program Files/7-Zip/7z.exe")
if extract_path:
    print(f"文件已解压到: {extract_path}")