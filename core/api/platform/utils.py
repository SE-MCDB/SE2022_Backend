

def format_time(time):
    # 格式化时间，2019-09-09 12:23:33
    # 去掉毫秒
    if time != None:
        time = str(time)[0:19]
    else:
        print(2)
    return time