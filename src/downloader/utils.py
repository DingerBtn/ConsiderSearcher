def format_speed(speed):
    """格式化速度显示"""
    if speed >= 1024 * 1024:
        return f"{speed/(1024 * 1024):.2f} MB/s"
    return f"{speed/1024:.2f} KB/s"
