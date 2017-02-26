import requests
import db
import model
from lxml import etree
from Config import config
from pyquery import PyQuery


class KaoYanBang(object):

    def __init__(self, main_url):
        self.main_url = main_url+'{num}'
        self.headers = config.headers
        self.url_list = list()
        self.title_list = list()
        self.class_list = list()
        self.content_list = list()
        self.endpoint = config.get_endpoint()
        self.first_url = True
        self.db_session = db.make_db_session()

    def test(self):
        url1 = 'http://bbs.kaoyan.com/t1821347p1'
        resp = requests.get(url1)
        html = etree.HTML(resp.content.decode())
        self.get_cur_page_title(html)
        self.get_cur_page_class(html)
        print(self.title_list)
        print(self.class_list)

    # 得到当前页面的url list，筛选之后直接加入到总的里面
    def get_cur_page_url_list(self, cur_url):
        resp = requests.get(cur_url)
        html = etree.HTML(resp.content.decode())
        # 只记录符合阅读大于read，回复大于reply的
        raw_path = "//td[@class='num']/em[text()>{read_num}]/../a[text()>{reply_num}]/@href"
        made_path = raw_path.format(read_num=config.filters['read'], reply_num=config.filters['reply'])
        filtered_url_list = html.xpath(made_path)
        # 如果当前页面的文章发帖列表为空则终止此次任务并返回None
        if len(filtered_url_list) < 1:
            print('No data')
            return None
        # 将当前页中的所有文章链接加入到 self.url_list 中
        for url in filtered_url_list:
            # 如果当前URL为上次运行后的最后一个则终止此次任务并返回None
            if url == self.endpoint:
                return None
            self.url_list.append(url)
        return 'OK'

    def get_url_list(self):
        # 由配置文件确定默认爬取的页数和板块
        for i in range(config.filters['pages']):
            cur_url = self.main_url.format(num=i+1)
            # 添加脚手架代码
            if self.get_cur_page_url_list(cur_url) is None:
                print(cur_url+' | States: Access the end url.')
                return

    def get_num_of_cur_page(self, html, cur_url):
        # 水贴返回None
        # 如果楼主被禁言则视为水贴
        islocked = len(html.xpath("//div[@id='postlist']/div[1]//div[@class='locked']")) == 1
        if islocked:
            return None
        # 通过楼主占据的回复数判断水贴与否
        raw_auth_href_list = html.xpath("//div[@class='pi']/div[@class='authi']/a/@href")
        try:
            basic_href = raw_auth_href_list[0]
        except Exception as e:
            print('Error In: '+cur_url)
            return -1
        count = 0
        count_max = config.filters['re-max']
        for href in raw_auth_href_list:
            if basic_href == href:
                count += 1
                if count > count_max:
                    return None
        if basic_href == raw_auth_href_list[1]:
            return 2
        else:
            return 1

    def get_cur_page_title(self, html):
        title = html.xpath("//div[@id='postlist']//span[@id='thread_subject']/text()")
        if len(title) < 1:
            self.title_list.append('Empty')
            print('Empty')
        else:
            self.title_list.append(title[0])
            print(title[0])

    def get_cur_page_class(self, html):
        raw_cls = html.xpath("//div[@id='postlist']//span[@id='thread_subject']/../a//text()")
        made_cls = ''.join(raw_cls)
        # if made_cls == '':
        #     made_cls = 'Empty'
        # else:
        made_cls = made_cls[1:-1]
        print(made_cls)
        self.class_list.append(made_cls)

    def get_cur_page_html_of_content(self, td_list):
        html_in_str = ''
        for td in td_list.items():
            # 完善img的src属性
            img_list = td('img')
            for img in img_list.items():
                file = img.attr("file")
                img.attr("src", file)
            # 将 pyquery 对象转换为 str 再保存
            html_in_str += td.html()
        self.content_list.append(html_in_str)

    def get_cur_page_main_content(self, cur_url):
        resp = requests.get(cur_url, headers=self.headers)
        html = etree.HTML(resp.content.decode())
        doc = PyQuery(html)
        tag_td_list = doc('td').filter('.t_f')
        # 添加控制，保留第一个还是前两个，水贴终止并返回
        num = self.get_num_of_cur_page(html, cur_url)
        if num is None:
            return None
        del tag_td_list[num:]
        # 得到当前页面的标题
        self.get_cur_page_title(html)
        # 得到当前页面的分类
        self.get_cur_page_class(html)
        # 得到包含楼主内容的html代码
        self.get_cur_page_html_of_content(tag_td_list)
        # 将第一个有效文章链接设置为endpoint
        if self.first_url:
            self.endpoint = cur_url
            self.first_url = False
        return 'OK'

    def get_content_list(self):
        self.get_url_list()
        for url in self.url_list:
            # 添加脚手架代码
            if self.get_cur_page_main_content(url) is not None:
                print(url+' | States: OK')

    def save(self):
        for i in range(len(self.content_list)):
            new_src = model.KybSrc(title=self.title_list[i],
                                   content=self.content_list[i],
                                   cls=self.class_list[i])
            self.db_session.add(new_src)
            self.db_session.commit()
            self.db_session.close()

    def close(self):
        # 更新endpoint
        config.set_endpoint(self.endpoint)

    def work(self):
        self.get_content_list()
        self.save()
        # self.close()

if __name__ == '__main__':
    print('OK')
    # 暂时由配置模块读入板块首页面
    #KaoYanBang('http://bbs.kaoyan.com/f1822p').get_content_list()
    # k1.test()
    # k1.get_content_list()
    # print(len(k1.content_list))
    # print(len(k1.title_list))
    # print(len(k1.class_list))
    # for i in range(len(k1.title_list)):
    #     print('=============================')
    #     print(k1.title_list[i])
    #     print(k1.class_list[i])
    #     print('***************************')
    #     print(k1.content_list[i])
    # k1.close()
