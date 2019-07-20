# 引入模块
from bs4 import BeautifulSoup
from urllib import request
import chardet
import itchat
import re
import os

# # 登陆微信
# itchat.auto_login(hotReload=True)

official = "http://www.suse.edu.cn"
url = "http://www.suse.edu.cn/p/10/?StId=st_app_news_search_x636053927420541815_x__x__x_0_x_0"

def DowloadPage(url):
    # 下载网页
    response1 = request.urlopen(url)
    # 获取网页内容
    html = response1.read()
    # 设置编码格式
    Coding = chardet.detect(html)['encoding']
    # 关闭response1
    response1.close()

    Page_Soup = BeautifulSoup(html.decode(Coding), 'html.parser')
    return (Page_Soup,Coding)

# 创建目录
Path = "E:\Python\SUSE_website\站内通知\\"
isExists = os.path.exists(Path)
# 判断是否否存在路径
if not isExists:
    os.makedirs(Path)

# 获取链接及内容
Page_Soup = DowloadPage(url)[0]
Links = Page_Soup.find_all('div', class_="div_item")
Notice = dict()
Serial = 0
for Link in Links:
    link = Link.find('a', href=re.compile(r'/p/10'))
    Serial += 1
    # print(Serial, link.get_text())
    site = official + link.get('href')
    # print(site)
    Notice[link.get_text()] = site

    # 保存信息
    name = link.get_text()
    FilePath = Path + name + '.txt'
    if not FilePath:
        file = open(FilePath, "w+",encoding=DowloadPage(url)[1])

        # 获取通知内容
        PageSoup = DowloadPage(site)[0]
        for p in PageSoup.find_all(name='p'):
            for span in p.find_all(name='span'):
                if span.string != None:
                    file.write(span.string + '\n')
        file.close()

        # itchat.send_file(FilePath, toUserName='filehelper')


# msg = ""
# for i in Notice.keys():
#     msg = msg + str(i) + "\n"
#
# # 将消息发送到微信
#
# itchat.send(msg, toUserName='filehelper')

