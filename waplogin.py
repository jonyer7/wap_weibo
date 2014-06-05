#coding:utf-8
import urllib,urllib2,cookielib,re
#获得一个cookieJar实例
cookie=cookielib.CookieJar()
#cookieJar作为参数，获得一个opener
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)

#登录新浪通行证
page=opener.open("http://3g.sina.com.cn/prog/wapsite/sso/login.php")
data=page.read()
mobile="903218171@qq.com"    #微博登陆邮箱
pwd="mabin150750"          #密码
# 找到页面的password 和 vk 的值，后边POST时候要用
password=re.findall('<postfield name="([\S]*)" value="\$\(password\)" />',data)[0]
vk=re.findall('<postfield name="vk" value="([\S]*)" />',data)[0]
#POST登陆
params=urllib.urlencode({"mobile":mobile,password:pwd,"vk":vk,"remember":"on","backURL":"http://weibo.cn","submit":"1"})
#这里的headers用的是PC端浏览器的User-Agent，访问速度快
headers={
        "Content-Type":"application/x-www-form-urlencoded",
        "Referer":"http://3g.sina.com.cn/prog/wapsite/sso/login.php",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0"
         }
req=urllib2.Request("http://3g.sina.com.cn/prog/wapsite/sso/login.php",params,headers)
page=urllib2.urlopen(req)
#print page.read()
#抓取cookie中的gsid,实际上有了gsid在手机端直接访问 weibo.cn/？gsid="你的gsdi" 就可以登陆微博了
cookieStr=""
for item in cookie:
    cookieStr+=(item.name+'='+item.value+';')
    if "gsid" in item.name:
        gsid=item.value
#print gsid
#print cookieStr
#这里的headers模拟手机端登录了，PC端无法登录weibo.cn
headers={"User-Agent":"JUC (Linux; U; 2.3.7; zh-cn; MB200; 320*480) UCWEB7.9.3.103/139/999",
         "Cookie":cookieStr,
         #"Referer": "http://weibo.cn/search/?pos=search"
         }
req=urllib2.Request("http://weibo.cn/?gsid="+gsid,None,headers)
page=urllib2.urlopen(req)
data=page.read()
#获取uid和st字段，后边发微博和点赞的时候需要用
src=re.search('<a href="http://weibo.cn/[\S]*uid=([\d]*)[\S]*st=([\S]{4})">',data)
uid=src.group(1)
st=src.group(2)

#发微博
content="要发的微博"
newparam=urllib.urlencode({"rl":'0',"content":content})
req=urllib2.Request("http://weibo.cn/mblog/sendmblog?vt=4&gsid="+gsid+"&st=" + st,newparam,headers)
page=urllib2.urlopen(req)
#print "成功"

#给好友点赞，goduid是女神的微博uid

goduid=1146576392
dic=[]
while True:
    req=urllib2.Request("http://weibo.cn/u/"+str(goduid),None,headers)
    page=urllib2.urlopen(req).read()
    firstblog=re.search('<div class="c" id="M_([\S]*)">',page)
    if (firstblog==None):
        continue
    M_id=firstblog.group(1)
    if M_id not in dic:
        dic.append(M_id)
        req=urllib2.Request("http://weibo.cn/attitude/"+M_id+"/add?uid="+uid+"&rl=0&st="+st,None,headers)
        urllib2.urlopen(req)
        

    










