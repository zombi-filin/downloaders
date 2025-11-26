import urllib.request
import json
import os
import re

def get_data(url, data = None):
    ''' Функция возвращает HTML код страницы по url или None если 404'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': 'https://neobihier.com',
        'Referer': 'https://neobihier.com/driver'
    }
    if data is not None:
        data = json.dumps(data).encode('utf-8')

    request = urllib.request.Request(url=url, data=data, headers=headers)
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        if hasattr(e,'code') and (e.code == 400):
            print('ERROR 400 Bad Request')
        if hasattr(e,'code') and (e.code == 403):
            print('ERROR 403 Forbidden')
        elif hasattr(e,'code') and (e.code == 404):
            print('ERROR 404 Not Found')
            return None
        elif hasattr(e,'code') and (e.code == 500):
            return '[]'
        else:
            return get_data(url, data) 
    if response.code == 404:
        return None
    else:
        return response.read().decode('utf-8')

def download_file(url):
    download_folder = 'neobihier_com'
    if not os.path.exists(download_folder):
        os.mkdir(download_folder)
    filename_regex = r'com\/(.*?)(\?)'
    find = re.findall(filename_regex, url)
    filename = os.path.join(download_folder, find[0][0])
    if os.path.exists(filename):
        return

    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        # 'Accept': 'application/json',
        # 'Content-Type': 'application/json',
        'Origin': 'https://neobihier.com',
        'Referer': 'https://neobihier.com/driver'
        }
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        total_size = response.length
        chunk_size = 256 * 1024
        downloaded = 0
        with open(filename + '.tmp', 'wb') as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                downloaded += len(chunk)
                per = int((downloaded / total_size) * 100)
                print(f'Download {filename} {per}%',end='\r')
                f.write(chunk)
        os.rename(filename + '.tmp', filename)
        print(f'Download {filename} successfully.')
    except urllib.error.URLError as e:
        print(f"Error downloading file: {e}")

download_list = []


product_src = get_data('https://neobihier.com/api/product/list')
product_json = json.loads(product_src)
for product in product_json:
    product_id = product['id']
    print(f'product:{product_id}')
    motherboard_src =  get_data(f'https://neobihier.com/api/product/motherboard/{product_id}')
    motherboard_json = json.loads(motherboard_src)
    for motherboard in motherboard_json:
        motherboard_id = motherboard['id']
        print(f'motherboard:{motherboard_id}')
        url = 'https://neobihier.com/api/driver/search'
        data = {'motherboardId':motherboard_id , 'productId':product_id}
        search_src = get_data(url, data)
        search_json = json.loads(search_src)
        for line in search_json:
            download_src = get_data('https://neobihier.com/api/driver/download/'+str(line['id']),'')
            download_json = json.loads(download_src)
            if download_json['url'] not in download_list:
                download_list.append(download_json['url'])
                download_file(download_json['url'])
print('DONE')