#!/usr/bin/env python3
# 感谢百度翻译，禁止用于商业用途

import requests


# 中译英
def zh2en(content):
    data = {
        ' from':'zh','to':'en','query':content  ,
        'transtype':'translang',
        'simple_means_flag':'3',
    }
    return _translate(data)


# 英译中
def en2zh(content):
    data = {
        ' from':'en','to':'zh','query':content  ,
        'transtype':'translang',
        'simple_means_flag':'3',
    }
    return _translate(data)


def _translate(data):
    url = 'http://fanyi.baidu.com/v2transapi/'
    headers ={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'}
    response = requests.post(url,data,headers=headers)
    result = response.json()['trans_result']['data'][0]['dst']
    return result


if __name__=="__main__":
    print(zh2en('你好，世界'))
    print(en2zh('Hello, world'))
