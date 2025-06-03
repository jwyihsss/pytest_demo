import time
def get_time():
    """
    获取当前时间
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
def get_time_stamp_str():
    """
    获取当前时间戳
    :return:
    """
    return str(int(time.time()*1000))





