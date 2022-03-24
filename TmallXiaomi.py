# coding:utf-8
import requests
from lxml import etree
import re
import copy

url = 'https://xiaomi.tmall.com/category.htm'
params = {
    'spm' : 'a1z10.3-b-s.w15914064-15567552165.2.7a8248feAP04A4',
    'orderType' : 'hotsell_desc',
    'viewType' : 'grid',
    'keyword' : '',
    'lowPrice' : '',
    'highPrice' : '',
    'scene' : 'taobao_shop'
}
headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46',
    'cookie' : 'cna=VxSdGq5W9WECAXPNciF8oBw6; sgcookie=E100OAML9wNnJfZ7VZGyBNVRN4SInawW1nfpTCPFeHp1IrIihDlMOdENM9QKNHnzQNQMynPewwSZGbQGCuzaPvH3z+mIHUk2afkmrXnnvIaDbmsBIotfV4x1IZmlIUSBEVDE; t=efe1f56160832f9b26b1131f4f6e5279; uc3=vt3=F8dCvUCV1rgu7k/Er3Q=&nk2=AR7rEKars5hk/w==&id2=UojcjU6y2+VQSw==&lg2=VFC/uZ9ayeYq2g==; tracknick=bzzzz_kaba; lid=bzzzz_kaba; uc4=nk4=0@A7NLpSHVvfKW3Z7DjMYHhqqBz0LN&id4=0@UOBYxUZKAx73vNpi6CS7oc1zwuok; lgc=bzzzz_kaba; enc=pI80SsyGaXghBvrT9b/iXoJMBsdVdQYHPxwce1lUj9/5fwIGH7/3hZOvz5eIFDSDCbdZCtknqc5OQnwbPG3dpQ==; _tb_token_=ee88e07ed3de0; cookie2=123020b79d32ad0402040896211c14ba; _m_h5_tk=e3e4178b89faa1c9f3ac3b85c028c25c_1648138709275; _m_h5_tk_enc=99536afa510637c97331a4f9455dc43b; xlly_s=1; pnm_cku822=; cq=ccp=1; tfstk=clhRBPvqEnxl8vzx7YpmAFZfGtmda_xLcaZh9EbLIOBdAdfRNsAisfKEzLaQbuLA.; l=eB_09h8nLIIQIApCKO5aourza77TiIdb4sPzaNbMiInca1Pf_ZdP6NCnJ5vM8dtjgtCfmetyx5kn5dLHR3jMBDLixLqj4_aEFxvO.; isg=BOTkWNDEWmsNx66n2Fjy1UVAteLWfQjnWARgPf4E_63wqYRzJohHdxlDbQGxcUA_'
}
dic = {}
list = []
page_text = requests.get(url = url,headers = headers ,params = params).text
#开发中获取一次响应后存下来进行本地的数据解析，以防过度访问被封ip
# with open('test.html','r',encoding= 'utf-8') as f:
#     page_text = f.read()
#裁剪响应中前半段无效代码
page_text = page_text.split('<li class="item even first">')
page_text = page_text[1]
#裁剪响应数据中后半段无效代码（随便挑一个不重复的标签裁剪后取前半段）
page_text = page_text.split('<div class="panel collection disappear">')
page_text = page_text[0]
#<div class="ranking">每个商品前会出现的标签,可分段进行正则解析，正则在大规模代码中效率低，不过天猫只有十个可以分可以不分
page_text = page_text.split('<div class="ranking">')
page_text.pop(0)
print(len(page_text))
# re解析：title="【老年机备用机优选】小米红米9A 5000mAh大电量屏幕游戏备用老年人手机xiaomi小米官方旗舰店官网正品" href="//
for i in page_text:
    dic['title'] = re.findall('.*?title="(.*?)" href=".*?',i)[0]
    dic['price'] = re.findall('.*?ce">￥<span>(.*?)</span></p>.*?',i)[0]
    dic['sales_num'] = re.findall('.*?"sale-count">(.*?)</span>笔.*?',i)[0]
    dic['product_url'] = re.findall('.*?href="//(.*?)" target="_.*?',i)[0]
    print(dic)
    list.append(copy.deepcopy(dic))
print(list)
