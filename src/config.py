class Config:
    def __init__(self):
        self.seven_zip_path = "7z"
        self.code_page = 932
        self.temp_dir = "temp"
        self.keywords = ["rpg"]
        self.start_num = 1     # 起始序号
        self.end_num = 100    # 结束序号
        self.download_threads = 5  # 同时下载的线程数
        self.max_workers = 5  # 搜索最大线程数
        self.timeout = 30
        self.chunk_size = 1024 * 128
        self.retries = 3
        self.base_url = "http://ftp.airnet.ne.jp/pub/pc/freem/"    # 下载基地址
        self.temp_dir = "J:/1/temp" # 缓存目录
        self.download_dir = "J:/1/download" # 下载目录
        self.output_dir = "J:/1/output"  # 输出目录