from http import cookiejar
import requests
# import cv2
import re

def downLoadCaptcha(url):
    captcha=requests.get(url)
    image=open('captcha.jpg','wb')
    image.write(captcha.content)
    image.close()

def printCaptcha():
    img=cv2.imread('captcha.jpg')
    cv2.imshow('yzm',img)
    cv2.waitKey()
    str=input('输入验证码:')
    print('输入的验证码为:%s'%str)
    return str
def getCaptchaUrlAndId(url):
    login=requests.get(url)
    tmp=str(login.content.decode('utf_8'))
    ruler=re.compile(r'name="captcha-id"(.*)value="(.*)"')
    match=ruler.search(tmp)
    if match:
        #豆瓣captcha格式
        temp='https://www.douban.com/misc/captcha?id='+match.group(2)+'&size=s'
        mlist=[match.group(2),temp]
        return mlist

def readCookie(cookieName):
    f=open(cookieName,'r')
    temp=f.read()
    f.close()
    cookie={}
    for i in temp.split('\n'):
        key,value=i.split(':',1)
        cookie[key]=value
    print(cookie)
    return cookie
#豆瓣爬取
def douban():
    username='******@qq.com'
    password='*****'
    data={
        'form_email':username,
        'form_password':password,
        'redir':'http://www.douban.com',
        'captcha-solution':'',
        'captcha-id':'',
        'source':'index_nav',
    }
    url='https://accounts.douban.com/login'
    #afturl为测试数据，登陆后可见
    afturl='https://www.douban.com/people/172618226'
    #首先获取登陆界面的验证码
    captcha=getCaptchaUrlAndId(url)
    captcha_id=captcha[0]
    print('captcha url :%s'%captcha[1])
    #验证码显示及输入
    downLoadCaptcha(captcha[1])
    yzm=printCaptcha()
    data['captcha-solution']=str(yzm)
    data['captcha-id']=str(captcha_id)
    print(data)
    print('验证码:%s'%yzm)
    #post请求
    login=requests.post(url,data=data)
    loginafter=requests.get(afturl,cookies=login.cookies)
    #记录内容
    f=open('text.txt','wb')
    f.write(loginafter.content)
    f.close()

#main为加载cookie访问
def main():
    url='https://accounts.douban.com/login'
    cookie=readCookie('cookies.txt')
    loginafter=requests.get('https://www.douban.com/people/172618226',cookies=cookie)
    f=open('text1.txt','wb')
    f.write(loginafter.content)
    f.close()
main()