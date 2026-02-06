import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

prefix_list = ['81','10','70','70_10']
url_list = []

print('SCAN BEGIN')

nom = 12000
while(nom < (110000)):
    for prefix in prefix_list:
        url = f'https://drivers.icl-techno.ru/download/{nom}-{prefix}.zip     '
        print(f'Try: {url}', end='\r')
        request = urllib.request.Request(url, None, headers)
        try:
            response = urllib.request.urlopen(request)
            url_list.append(url)
            print(f'Find: {url}')
        except:
            pass
    nom += 1

print('SCAN COMPLETE')
#
with open('drivers_icl_techno_ru.txt', 'w') as f:
    for line in url_list:
        f.write(f'{line}\n')

print('DONE')