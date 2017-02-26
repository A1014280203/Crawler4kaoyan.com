headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

check_time = '05'

# 保存的是“元链接”
block_urls = {'2017年考研': 'http://bbs.kaoyan.com/f2051p',
              '2018年考研': 'http://bbs.kaoyan.com/f2052p',
              '考研调剂': 'http://bbs.kaoyan.com/f326p',
              '2017考研复试现场直击': 'http://bbs.kaoyan.com/f2076p',
              '跨专业考研': 'http://bbs.kaoyan.com/f467p',
              '资料/试题': 'http://bbs.kaoyan.com/f1822p',
              '“我的考研之路”征文 ': 'http://bbs.kaoyan.com/f1951p'}

filters = {
    'reply': 10,
    'read': 2000,
    'pages': 2,
    're-max': 3
}


def get_endpoint():
    with open('./Config/endpoint.txt', 'r') as fe:
        endpoint = fe.readline()
    return endpoint


def set_endpoint(endpoint):
    with open('./Config/endpoint.txt', 'w') as fe:
        fe.write(endpoint)
