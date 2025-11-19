import urllib.request
import json

def get_data(url, data = None):
    ''' Функция возвращает HTML код страницы по url или None если 404'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'origin': 'https://neobihier.com',
        'referer': 'https://neobihier.com/driver'
    }
    if data is not None:
        data_encode = urllib.parse.urlencode(data).encode('utf-8')
        method = 'POST'
    else:
        data_encode = None
        method = 'GET'
    request = urllib.request.Request(url=url,data=data_encode, headers=headers , method=method)
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
        pass