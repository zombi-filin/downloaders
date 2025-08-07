import re
import urllib.request
import urllib.parse
import json

def get_html(url):
    ''' Функция возвращает HTML код страницы по url или None если 404'''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    request = urllib.request.Request(url, None, headers)
    try:
        print(url)
        response = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        if hasattr(e,'code') and (e.code == 404):
            return None
        elif hasattr(e,'code') and (e.code == 500):
            return '[]'
        else:
            return get_html(url) 
    if response.code == 404:
        return None
    else:
        return response.read().decode('utf-8')

download_list = []

product_class_list_str = get_html('https://en.colorful.cn/en/Home/GetProductClassList')
product_class_list_json = json.loads(product_class_list_str)

for product_class_item in product_class_list_json:
    product_class_str = get_html('https://en.colorful.cn/en/Home/GetProduct?modelid=' + product_class_item['parent_id'] +'&attrId=' + product_class_item['id'])
    product_class_json = json.loads(product_class_str)
    for product_item in product_class_json:
        download_str = get_html('https://en.colorful.cn/en/Home/GetProductDownload?mid=' + product_class_item['parent_id'] + '&id=' + product_item['id'])
        download_json = json.loads(download_str)
        for link_item in download_json:
            if link_item['fileurl'] is None:
                continue
            fileurl = urllib.parse.quote(link_item['fileurl']).replace('https%3A','https:')
            if fileurl not in download_list:
                download_list.append(fileurl)

with open('en.colorful.cn.txt', 'w') as f:
    for line in download_list:
        f.write(f'{line}\n')

print('Done')