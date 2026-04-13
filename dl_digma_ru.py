import urllib.request

download_list = []

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }
scip_code = [404, 503]
id = 1
while id <= 99999:
    url = f'https://dl.digma.ru/{id:05d}'
    print(f'{url}')
    request = urllib.request.Request(url, None, headers)
    try:
        response = urllib.request.urlopen(request)
        download_list.append(url)
    except urllib.error.URLError as e:
        if e.code in scip_code:
            pass
        else:
            pass
    id += 1

with open('dl_digma_ru.txt', 'w') as f:
    for line in download_list:
        f.write(f'{line}\n')

print('DONE')

'''
https://dl.digma.ru/03415
https://dl.digma.ru/03417
'''