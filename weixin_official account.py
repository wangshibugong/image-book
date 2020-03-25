#-*- coding:UTF-8 -*-
import json
import time
import pdfkit

import requests
import pymongo
confg = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
#这里指定一下wkhtmltopdf的路径，这就是我为啥在前面让记住这个路径

base_url = 'https://mp.weixin.qq.com/mp/profile_ext'
#'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzU2ODYzNTkwMg==&f=json&offset=12&count=10&is_ok=1&scene=&uin=777&key=777&pass_ticket=xVgxqIPj5DvCamb6GJzjdCW43tdL9rpdBKiCXbuKEYPDATz7sbzpuCYWPFSlPQg0&wxtoken=&appmsg_token=1052_AR8Q5h%252BkMOlLIo7aHLB5bEAo7vVjbCZ2NoHfcg~~&x5=0&f=json'



headers = {
    'Connection': 'keep - alive',
    'Accept': '* / *',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; RMX1931 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MMWEBID/7505 MicroMessenger/7.0.6.1460(0x27000634) Process/toolsmp NetType/WIFI Language/zh_CN',
    'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU2ODYzNTkwMg==&subscene=0&devicetype=android-22&version=27000634&lang=zh_CN&nettype=WIFI&a8scene=7&session_us=gh_10d1e024f589&pass_ticket=fURUsxAFml94bagxjZY%2F6lKuUKgefIviYZreMP713WrjcHmPxMrnNWgwVy4ntk2k&wx_header=1',
    'Accept-Encoding': 'br, gzip, deflate'
}

cookies = {
    'devicetype': 'android-22',
    'lang': 'zh_CN',
    'pass_ticket': 'fURUsxAFml94bagxjZY/6lKuUKgefIviYZreMP713WrjcHmPxMrnNWgwVy4ntk2k',
    'version': '27000634',
    'wap_sid2': 'CPXYrbADElxPeGZJQ0VPUWw0ZHlKeDZ2bkZNQ3FzZVNaaTdvVE1nNVoyY3BObW1zNkVTNXhXbmR4WjlHOW9IWXZWQTcxNURIN0diWDVFWm8yWlhfUkhVb3ROd0laQndFQUFBfjDqi7fzBTgNQJVO',
    'wxuin': '906718325'
}



def get_params(offset):
    params = {
        'action': 'getmsg',
        '__biz': 'MzU2ODYzNTkwMg==',
        'f': 'json',
        'offset': '{}'.format(offset),
        'count': '10',
        'is_ok': '1',
        'scene': '126',
        'uin': '777',
        'key': '777',
        'pass_ticket': 'fURUsxAFml94bagxjZY/6lKuUKgefIviYZreMP713WrjcHmPxMrnNWgwVy4ntk2k',
        'appmsg_token': '1052_9vujILNi%2FP1KHXHiKwRMwpVWiHkZ3fy1HKk5bQ~~',
        'x5': '0',
        'f': 'json',
    }

    return params


def get_list_data(offset):
    res = requests.get(base_url, headers=headers, params=get_params(offset), cookies=cookies)
    data = json.loads(res.text)
    can_msg_continue = data['can_msg_continue']
    next_offset = data['next_offset']

    general_msg_list = data['general_msg_list']
    list_data = json.loads(general_msg_list)['list']
    client = pymongo.MongoClient('localhost', 27017)  # 创建连接，因为用的本机的mongodb数据库，所以直接写localhost即可，也可以写成127.0.0.1，27017为端口

    db = client['mydb']  # 连接的数据库

    collection = db['my_collection']  # 连接的表



    for data in list_data:
        try:
            if data['app_msg_ext_info']['copyright_stat'] == 11:
                msg_info = data['app_msg_ext_info']
                title = msg_info['title']
                content_url = msg_info['content_url']
                # 自己定义存储路径
                pdfkit.from_url(content_url, 'C:/Users/lee/Pictures/Camera Roll/'+ title +'.pdf',configuration=confg)
                data = {'title': title, 'url': content_url}  # 将数据存入到字典变量data中

                collection.insert(data)  # 将data中的输入插入到mongodb数据库

                print('获取到原创文章：%s ： %s' % (title, content_url))
                print(32323)
        except:
            print('不是图文')

    if can_msg_continue == 1:
        time.sleep(1)
        get_list_data(next_offset)


if __name__ == '__main__':
    get_list_data(0)