import re
import urllib.request


def get_html(url):
    ''' Функция возвращает HTML код страницы по url или None если 404'''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    request = urllib.request.Request(url, None, headers)
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        if hasattr(e,'code') and (e.code == 404):
            return None
        else:
            return get_html(url) 
    if response.code == 404:
        return None
    else:
        return response.read().decode('utf-8')

dowload_list = []

def processed(url):
    print(f'processed {url}')
    page_html = get_html(url)
    page_list = page_html.split('\n')
    link_regex = r'class="link"><a href="(.*?)(")'
    for page_line in page_list:
        link_find = re.findall(link_regex, page_line)
        if len(link_find)>0:
            link = link_find[0][0]
            
            if link == '../':
                continue

            if '/' in link:
                processed(url + link)
            else:
                download_link = url + link
                if download_link not in dowload_list:
                    dowload_list.append(download_link)


processed('https://download.ninkear.com/')

with open('download_ninkear_com.txt', 'w') as f:
    for line in dowload_list:
        f.write(f'{line}\n')

print('DONE')