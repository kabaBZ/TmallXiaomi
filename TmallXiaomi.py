# coding:utf-8
import requests
from lxml import etree
import re
import copy
url = 'https://xiaomi.tmall.com/i/asynSearch.htm'
def set_params(a):
    params = {
        '_ksTS': '1648134407880_133',
        'mid': 'w-14756119836-0',
        'wid': '14756119836',
        'path': '/category.htm',
        'spm': 'a1z10.5-b-s.w4011-14756119836.54.bb814e025qwZVN',
        'orderType': 'hotsell_desc',
        'viewType': 'grid',
        'scene': 'taobao_shop',
        'pageNo': a
    }
    return params
headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46',
}
def parse(page_text):
    dic = {}
    list = []
    i = 0
    num = 1
    #裁剪响应中前半段无效代码每个商品前会出现的标签,可分段进行正则解析，正则在大规模代码中效率低
    page_text = page_text.split('<!--  item')
    page_text.pop(0)
    #弹出最后6个推荐商品剩余一页共60个,换item不用弹
    # for i in range(6):
    #     page_text.pop()
    #     i += 1
    # re解析：<img alt=\"【天玑1100 处理器】小米/Redmi Note 10 Pro 5G智能红米手机学生拍照游戏官方旗舰店红米官方旗舰店官网\"
    #class=\"c-price\">1469.00</span></div>
    # class=\"sale-num\">40万+</span>
    #href=\"//detail.tmall.com/item.htm?id=44932380380&rn=ea8fc89d045f285d78fe41708a17beb9&abbucket=5\" ta
    for i in page_text:
        dic['num'] = num
        dic['title'] = re.findall('.*?<img alt=(.*?)" data-ks-lazyl.*?',i)[0].split('\" ')[1].split('\\')[0]
        dic['price'] = re.findall('.*?.discntPrice:  (.*?)     -->.*?',i)[0]
        dic['sales_num'] = re.findall('.*?"sale-num(.*?)</span>.*?',i)[0].split('>')[1]
        dic['product_url'] = re.findall('.*?href=(.*?)" target=.*?',i)[0].split('//')[1].split('\\')[0]
        num += 1
        list.append(copy.deepcopy(dic))
    return list

# page_text = requests.get(url = url,headers = headers ,params = params).text
# print(page_text)
# with open('test.html','w',encoding= 'utf-8') as f:
#     f.write(page_text)
#开发中获取一次响应后存下来进行本地的数据解析，以防过度访问被封ip
i = 1
for i in range(int(input('请输入爬取页数:'))):
    params = set_params(i)
    page_text = requests.get(url=url, headers=headers, params=params).text
# with open('test.html','r',encoding= 'utf-8') as f:
#     page_text = f.read()
# print(page_text)
    print(parse(page_text))
