import urllib.request

download_list = []

error_count = 0

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }
scip_code = [404, 503]
id = 1
while id <= 99999 and error_count < 100:
    url = f'https://dl.sunwind.ru.com/{id:05d}'
    print(f'{url}')
    request = urllib.request.Request(url, None, headers)
    try:
        response = urllib.request.urlopen(request)
        download_list.append(url)
        error_count = 0
    except urllib.error.URLError as e:
        if e.code in scip_code:
            pass
            error_count += 1
        else:
            pass
    id += 1

with open('dl_sunwind_ru_com.txt', 'w') as f:
    for line in download_list:
        f.write(f'{line}\n')

print('DONE')