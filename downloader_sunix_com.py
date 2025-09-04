import re
import urllib.request
import urllib.parse
import json

def get_data(url, data = None):
    ''' Функция возвращает HTML код страницы по url или None если 404'''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    if data is not None:
        data_encode = urllib.parse.urlencode(data).encode()
    else:
        data_encode = None
    request = urllib.request.Request(url, data_encode, headers)
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        if hasattr(e,'code') and (e.code == 404):
            return None
        elif hasattr(e,'code') and (e.code == 500):
            return '[]'
        else:
            return get_data(url, data) 
    if response.code == 404:
        return None
    else:
        return response.read().decode('utf-8')
    

url = 'https://www.sunix.com/en/support_action.php?oper=get_product_name'

product_id = 0
dowload_list = []

while product_id < 3000:
    print(f'product_id:{product_id}')
    data = {'product_id':product_id}

    data_src = get_data(url, data)
    if len(data_src) > 1:
        data_json = json.loads(data_src)
        print('found:' + str(len(data_json)))
        for item in data_json:
            driver_link = 'https://www.sunix.com/' + item['driver_link']
            if driver_link not in dowload_list:
                print(driver_link)
                dowload_list.append(driver_link)
        pass
    product_id += 1

with open('sunix.com.txt', 'w') as f:
    for line in dowload_list:
        f.write(f'{line}\n')

print('DONE')