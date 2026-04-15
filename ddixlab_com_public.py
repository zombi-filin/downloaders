import re
import urllib.request

download_list = []

def get_html(url):
    ''' Функция возвращает HTML код страницы по url или None если 404'''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    request = urllib.request.Request(url, None, headers)
    try:
        response = urllib.request.urlopen(request)
        return response.read().decode('utf-8').replace(' ','').split('\n')
    except UnicodeDecodeError:
        return ''
    except urllib.error.URLError as e:
        return ''

def processed_url(url):
    print(url)
    html_src = get_html(url)
    for line in html_src:
        regex = r'^<ahref=[\"\']([^\"\']*)[\"\']'
        find_res = re.findall(regex, line)
        if len(find_res) > 1:
            pass
        elif len(find_res) == 1:
            if find_res[0][-1] == '/':
                processed_url(url + find_res[0])
            else:
                download_list.append(url + find_res[0])

url_list = [
    'https://www.ddixlab.com/public/digma/',
    'https://www.ddixlab.com/public/sunwind/'
]

for url in url_list:
    processed_url(url)


with open('ddixlab_com_public.txt', 'w') as f:
    for line in download_list:
        f.write(f'{line}\n')

print('DONE')