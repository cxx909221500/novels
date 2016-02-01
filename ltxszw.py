from bs4 import BeautifulSoup
import re
import requests
import os
import threading
import base64

fenlei={'1':'暴力虐待',
        '2':'都市言情',
        '3':'校园美色',
        '4':'古典武侠',
        '5':'家庭乱伦',
        '6':'制服诱惑',
        '7':'科幻灵异'}
fenlei_fenyelist=set()
articlelist={}
zhangjie={}
fenlei_id=1

#下载该章节
def ltxszw_down_novel(novel_title,zhangjie):
    novel_title=novel_title
    zhangjie_title=zhangjie[0]
    zhangjie_url=zhangjie[1]
    # print('正在下载{}的{}章节。'.format(novel_title,zhangjie_title))
    # print(zhangjie_url)
    zhangjie_requests=requests.get(zhangjie_url)
    zhangjie_requests.encoding='gbk'
    zhangjie_data=zhangjie_requests.text
    zhangjie_soup=BeautifulSoup(zhangjie_data,'html.parser')
    zhangjie_text=zhangjie_soup.find('div',id="htmlContent",class_="contentbox")
    zhangjie_text=zhangjie_text.text
    # zhangjie_text=zhangjie_text.replace('看原创成人小说，就上龙腾小说网！网址：http://www.7ey.net','')
    fenleiname=fenlei[str(fenlei_id)]
    if os.path.exists(fenleiname):
        pass
    else:
        os.mkdir(fenleiname)
    if os.path.exists('{}/{}'.format(fenleiname,novel_title)):
        pass
    else:
        os.mkdir('{}/{}'.format(fenleiname,novel_title))
    if os.path.exists('{}/{}/{}.txt'.format(fenleiname,novel_title,zhangjie_title)):
        pass
    else:
        # print('开始写')
        file=open('{}/{}/{}.txt'.format(fenleiname,novel_title,zhangjie_title),'wb+',encoding='utf-8')
        zhangjie_text=zhangjie_text.encode('utf-8')
        file.write(zhangjie_text)
        file.close()

#获取该小说的所有章节——将章节链接传给ltxszw_down_novel
def ltxszw_down_articleindex(url):
    novel_title=url[0]
    novel_url=url[1]
    print('正在下载小说：{},url:{}'.format(novel_title,novel_url))
    ltxszw_article_requests=requests.get(novel_url)
    ltxszw_article_requests.encoding='gbk'
    ltxszw_article_data=ltxszw_article_requests.text
    ltxszw_article_soup=BeautifulSoup(ltxszw_article_data,"html.parser")
    ltxszw_articleinfo_readbtn=ltxszw_article_soup.find('a',id="htmldianjiyuedu")
    ltxszw_articleinfo_readbtn=ltxszw_articleinfo_readbtn['href']
    # print(ltxszw_articleinfo_readbtn)
    ltxszw_articleinfo_compile=re.compile(r'html/\d*/')
    ltxszw_articleinfo_compile2=re.compile(r'\d{2,}')
    ltxszw_articleinfo_readbtn_id_id=ltxszw_articleinfo_compile2.findall(ltxszw_articleinfo_readbtn)
    ltxszw_articleinfo_readbtn_id_id=ltxszw_articleinfo_readbtn_id_id[0]
    # print(ltxszw_articleinfo_readbtn_id_id)
    ltxszw_articleinfo_readbtn_id=ltxszw_articleinfo_compile.findall(ltxszw_articleinfo_readbtn)
    ltxszw_articleinfo_readbtn_id=ltxszw_articleinfo_readbtn_id[0][5:-1]
    # print(ltxszw_articleinfo_readbtn_id)
    ltxszw_article_requests=requests.get(ltxszw_articleinfo_readbtn)
    ltxszw_article_requests.encoding='gbk'
    ltxszw_article_data=ltxszw_article_requests.text
    ltxszw_article_soup=BeautifulSoup(ltxszw_article_data,'html.parser')
    for i in ltxszw_article_soup.find_all('a',href=re.compile(r'\d*.html')):
        zhangjie_title=i.text
        zhangjie_href='http://www.ltxszw.com/files/article/html/{}/{}/{}'.format(ltxszw_articleinfo_readbtn_id,ltxszw_articleinfo_readbtn_id_id,i['href'])
        zhangjie[zhangjie_title]=zhangjie_href
    for i in zhangjie.items():
        threading.Thread(target=ltxszw_down_novel(novel_title,i))
        #ltxszw_down_novel(novel_title,i)
    # ltxszw_down_novel(novel_title,zhangjie.popitem())
    # # print('{}下载完成'.format(novel_title))

#获取当前分页的所有小说——将分页上的一个小说传给ltxszw_down_articleindex方法
def ltxszw_down_articlelist(url):
    ltxszw_article_requests=requests.get(url)
    ltxszw_article_requests.encoding='gbk'
    ltxszw_article_data=ltxszw_article_requests.text
    ltxszw_article_soup=BeautifulSoup(ltxszw_article_data,'html.parser')
    for i in ltxszw_article_soup.find_all('a',href=re.compile(r"http://www.ltxszw.com/modules/article/articleinfo.php\?id=\d*")):
        articlelist[i.text]=i['href']
    for i in articlelist.items():
        ltxszw_down_articleindex(i)
    # ltxszw_down_articleindex(articlelist.popitem())


#获取当前分类的分页，将分页链接加入fenlei_fenyelist集合——将分页链接传入ltxszw_down_articlelist方法
def ltxszw(cc):
    ltxszw_fenlei_requests=requests.get('http://www.ltxszw.com/modules/article/articlelist.php?class={}'.format(cc))
    ltxszw_fenlei_requests.encoding='gbk'
    ltxszw_fenlei_data=ltxszw_fenlei_requests.text
    ltxszw_fenlei_soup=BeautifulSoup(ltxszw_fenlei_data,'html.parser')
    ltxszw_fenlei_fenye=ltxszw_fenlei_soup.find('em',id='pagestats')
    ltxszw_fenlei_compile=re.compile(r'/\d*')
    ltxszw_fenlei_fenye=ltxszw_fenlei_compile.findall(ltxszw_fenlei_fenye.text)
    ltxszw_fenlei_fenye=ltxszw_fenlei_fenye[0][1:]
    for i in range(int(ltxszw_fenlei_fenye)):
        fenlei_fenyelist.add('http://www.ltxszw.com/modules/article/articlelist.php?class={}&page={}'.format(cc,i))
    #ltxszw_down_articlelist(fenlei_fenyelist.pop())
    for i in fenlei_fenyelist:
        ltxszw_down_articlelist(i)
    # ltxszw_down_articlelist(fenlei_fenyelist.pop())
    # print('分类{}下载完成。'.format(cc))

#入口，遍历7个分类
#for i in range(1,7):
#    fenlei_id=i
for a,b in fenlei.items():
 print('{}--{}'.format(a,b))
fenlei_id=input('输入要下载的分类：')
ltxszw(fenlei_id)
print('小说全部下载完成。')