from bs4 import BeautifulSoup
from urllib import request
import chardet
import re
import os

official = "http://www.suse.edu.cn"
url = "http://www.suse.edu.cn/p/10/?StId=st_app_news_i_x636875672237590022"

# 下载网页
response1 = request.urlopen(url)
# 获取网页内容
html = response1.read()
# 设置编码格式
Coding = chardet.detect(html)['encoding']
# 关闭response1
response1.close()

Page_Soup = BeautifulSoup(html.decode(Coding), 'html.parser')

print(Page_Soup)