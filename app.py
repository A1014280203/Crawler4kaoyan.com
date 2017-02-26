from time import strftime, gmtime
from Config import config
from Crawler.KaoYan import KaoYanBang
import threading
# 使用协程提升IO速度
# 如果需要代理IP，则封装一个get函数
# 使用列表记录每一个线程的endpoint

if strftime('%H', gmtime()) == config.check_time:
    pass
else:
    for url in config.block_urls.values():
        temp = threading.Thread(target=KaoYanBang(url).work())
        temp.start()
        print(temp.name)
