# coding:utf-8
import requests
from lxml import etree
import re
import asyncio
import copy
import pickle
import time
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
    'cookie': 'cna=VxSdGq5W9WECAXPNciF8oBw6; t=efe1f56160832f9b26b1131f4f6e5279; tracknick=bzzzz_kaba; lid=bzzzz_kaba; lgc=bzzzz_kaba; enc=pI80SsyGaXghBvrT9b%2FiXoJMBsdVdQYHPxwce1lUj9%2F5fwIGH7%2F3hZOvz5eIFDSDCbdZCtknqc5OQnwbPG3dpQ%3D%3D; _m_h5_tk=e3e4178b89faa1c9f3ac3b85c028c25c_1648138709275; _m_h5_tk_enc=99536afa510637c97331a4f9455dc43b; xlly_s=1; pnm_cku822=; dnk=bzzzz_kaba; uc1=existShop=false&cookie14=UoewCLA2Dcw7%2FA%3D%3D&pas=0&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&cookie21=UtASsssmeW6lpyd%2BB%2B3t; uc3=id2=UojcjU6y2%2BVQSw%3D%3D&lg2=WqG3DMC9VAQiUQ%3D%3D&nk2=AR7rEKars5hk%2Fw%3D%3D&vt3=F8dCvConqKrxwZvQzf4%3D; _l_g_=Ug%3D%3D; uc4=id4=0%40UOBYxUZKAx73vNpi6CS1hl6uJSD4&nk4=0%40A7NLpSHVvfKW3Z7DjMYJ63kLDrpD; unb=1986247790; cookie1=VTtAfYdW5KnmWSmOcdsMueOvfuz3m3nv0Hpz3Xis2xY%3D; login=true; cookie17=UojcjU6y2%2BVQSw%3D%3D; cookie2=2011bb98e5a9c711d9cde4b0da2e25e2; _nk_=bzzzz_kaba; sgcookie=E100RTx%2B39fPnBdzkimf3cFg7O3eIcCh%2BwJjRxP1j0W4I3XrH%2FMRU29CuJJpHzdmosKRhbUlbM4u2jUWzWETd8A9C%2FtcrDWJdz4YSJvSuVgusebL390zhmyQ%2FdnzCjPKpyzW; cancelledSubSites=empty; sg=a06; csg=6c54f4fe; _tb_token_=5eba3473e3056; cq=ccp%3D0; tfstk=cy6lB7OuK_RWW4Oc18950orpVBFAZUkeS9Wf3OUgWUffuZ6ViqGq_Tz_mU4_zX1..; l=eB_09h8nLIIQI0UXBOfwourza77OSIRAguPzaNbMiOCP_y5p5QXAW60dr889C3GVhs_vR3-3_v0_BeYBqIVL9nzkEoiPN_Mmn; isg=BGNjVB3_BXaqx8lC8119OE7d8qcNWPeao0nH2JXAv0I51IP2HSiH6kECzqRa9E-S',
    'referer' : 'https://xiaomi.tmall.com/category.htm?spm=a1z10.5-b-s.w4011-14756119836.54.bb814e025qwZVN&orderType=hotsell_desc&viewType=grid&scene=taobao_shop&pageNo=2'
}
def parse(page_text,x):
    dic = {}
    list = []
    num = int(1)
    #裁剪响应中前半段无效代码每个商品前会出现的标签,可分段进行正则解析，正则在大规模代码中效率低
    page_text = page_text.split('<!--  item')
    page_text.pop(0)
    #弹出最后6个推荐商品剩余一页共60个,换item不用弹
    # for i in range(6):
    #     page_text.pop()
    #     i += 1
    #<img alt=\"【包邮 多仓速发】小米米家体重秤体脂秤智能家用婴儿女生宿舍称重健康减肥称精准迷你小型人体电子秤女\" data-ks-lazyload=\"//img.alicdn
    # re解析：<img alt=\"【天玑1100 处理器】小米/Redmi Note 10 Pro 5G智能红米手机学生拍照游戏官方旗舰店红米官方旗舰店官网\"
    #class=\"c-price\">1469.00</span></div>
    # class=\"sale-num\">40万+</span>
    #href=\"//detail.tmall.com/item.htm?id=44932380380&rn=ea8fc89d045f285d78fe41708a17beb9&abbucket=5\" ta
    for i in page_text:
        dic['num'] = num+(60*int(x))-60
        dic['title'] = re.findall('\s>\D+.*?<\/a>',i)[0].split('>')[1].split('<')[0]
        dic['price'] = re.findall('\d*?.\d\d\s+?--',i)[0].split('     --')[0]
        dic['sales_num'] = re.findall('>\d+\+?<\/span>|>\d+\D{1}\+<\/span>',i)[0].split('>')[1].split('<')[0]
        dic['product_url'] = re.findall('detail\.tmall\.com\/item\.htm\?id=.*?abbucket=5',i)[0]
        num += 1
        f.write(str(dic['num']) + ' ' + dic['title'] + ' ' + dic['price'] + ' ' + dic['sales_num'] + ' ' + dic['product_url'] + '\n')
        list.append(copy.deepcopy(dic))
    return list
z = int(input('单页1或连续2：'))
if z == 1:
    z = input('请输入页数：')
    start_time = time.time()
    f = open('data.csv', 'a', encoding='utf-8')
    params = set_params(z)
    page_text = requests.get(url=url, headers=headers, params=params).text
    # 开发中获取一次响应后存下来进行本地的数据解析，以防过度访问被封ip
    # with open('test.html','w',encoding= 'utf-8') as f:
    #     f.write(page_text)
    list = parse(page_text, z)
    print(list)
    f.close()
else:
    x = int(input('请输入开始页数:'))
    y = int(input('请输入结束页数:'))
    start_time = time.time()
    f = open('data.csv', 'a', encoding='utf-8')
    for i in range(x,y+1):
        params = set_params(i)
        page_text = requests.get(url=url, headers=headers, params=params).text
        # 开发中获取一次响应后存下来进行本地的数据解析，以防过度访问被封ip
        # with open('test.html','w',encoding= 'utf-8') as f:
        #     f.write(page_text)
        # with open('test.html','r',encoding= 'utf-8') as f:
        #     page_text = f.read()
        list = parse(page_text,i)
        i += 1
        print(list)
    f.close()
total_time = time.time()-start_time
print('总用时：',total_time)

