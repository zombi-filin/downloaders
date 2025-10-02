import gzip
import re
import urllib.request
import time

def get_data(url):
    ''' Функция возвращает HTML код страницы по url или None если 404'''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept-Encoding': 'gzip'}
    request = urllib.request.Request(url, None, headers)
    try:
        print(url)
        response = urllib.request.urlopen(request)
        print('length:' + str(response.length))
    except urllib.error.URLError as e:
        if hasattr(e,'code') and (e.code == 404):
            return None
        elif hasattr(e,'code') and (e.code == 500):
            return None
        else:
            return get_data(url) 
    if response.code == 404:
        return None
    elif response.code == 301:
        return None
    elif hasattr(request,'redirect_dict'):
        return None
    else:
        return gzip.decompress(response.read()).decode('utf-8').split('><')
        # return response.read().decode('utf-8')

category_list = [
    'acer',
'advan',
'alps',
'archos',
'blackview',
'ccit',
'celkon',
'cross',
'cubot',
'gfive',
'gionee',
'haier',
'hotwav',
'lanix',
'lmkj',
'maximus',
'meizu',
'mobicel',
'myphone',
'orro',
'oukitel',
'panasonic',
'plum',
'qnet',
'samsungclone',
'sharp',
'spice',
'teclast',
'texet',
'ulefone',
'vertex',
'verykool',
'wiko',
'winmax',
'xgody',
'yezz',
'zen',
'zopo',
]
# 
page = 1
url = 'https://gsmusbdriver.com'
category_regex = r'href="https:\/\/gsmusbdriver\.com\/category\/(.*?)(")'
while True:
    page_data = get_data(url)
    
    if page_data is None:
        break

    for page_line in page_data:
        category_find = re.findall(category_regex, page_line)
        
        if len(category_find) == 0:
            continue

        category = category_find[0][0]
            
        if category not in category_list:
            print(category)
            category_list.append(category)

    page += 1
    if page == 2:
        page += 1
        
    url = f'https://gsmusbdriver.com/page-{page}'
#
device_list = []
device_regex = r'href="https:\/\/gsmusbdriver\.com\/(.*?)(")'
for category in category_list:
    page = 1
    url = f'https://gsmusbdriver.com/category/{category}'
    
    while True:
        page_data = get_data(url)
        
        if page_data is None:
            break

        for page_line in page_data:
            device_find = re.findall(device_regex, page_line)
            
            if len(device_find) == 0:
                continue

            device_name = device_find[0][0]
            if len(device_find) == 1 and '-' in device_name:
                if device_name not in device_list:
                    print(device_name)
                    device_list.append(device_name)
        
        page += 1
        url = f'https://gsmusbdriver.com/category/{category}/page/{page}'
# 
dowload_urls = []
link_regex = r'href="https:\/\/gsmusbdriver\.com\/wp-content\/uploads\/(.*?)(")'
for device_name in device_list:
    page_data = get_data(f'https://gsmusbdriver.com/{device_name}')
    
    for page_line in page_data:
        link_find = re.findall(link_regex, page_line)
        
        if len(link_find) == 0:
            continue

        link = f'https://gsmusbdriver.com/wp-content/uploads/{link_find[0][0]}'
        
        if link not in dowload_urls:
            print(link)
            dowload_urls.append(link)
# 
with open('gsmusbdriver.com.txt', 'w') as f:
    for line in dowload_urls:
        f.write(f'{line}\n')

print('DONE')