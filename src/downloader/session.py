import requests
from requests.adapters import HTTPAdapter

# 全局配置
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

def get_http_session(max_workers):
    """创建高性能HTTP会话"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Encoding": "gzip, deflate",  # 启用压缩
    })
    # 扩大连接池
    adapter = HTTPAdapter(
        pool_connections=max_workers,
        pool_maxsize=max_workers * 2
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
