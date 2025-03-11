import re
import urllib.request
import json

alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
file_id_regex = r'\/downloadsr\.aspx\?File_Id=(.*)\"\starget'

def get_html(url, aspx = False):
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
    elif aspx:
        return response.url
    else:
        
        return response.read().decode('utf-8')

opened_id = []
download_list = []

f = open('usb-drivers.org.txt', 'w')
for suf in alphabet_list:
    print(f'suf > {suf}')
    id_list_src = get_html(f'https://apis-corp.advantech.com/api/v1/search/documents/support?q={suf}&lang=en&use_fuzzy=false&data_types=Driver&page_index=1&page_size=1000')
    id_list_json = json.loads(id_list_src)
    
    if int(id_list_json['count']) > 1000:
        breakpoint()
    for line_json in id_list_json['documents']:
        page_id = line_json['id']
        
        print(f'page_id > {page_id}')
        
        if page_id in opened_id:
            continue
        opened_id.append(page_id)

        page_src = get_html(f'https://www.advantech.com/en/support/details/driver?id={page_id}')
        page_scr_list = page_src.split('\n')
        for page_src_line in page_scr_list:
            file_id_finds = re.findall(file_id_regex, page_src_line)
            if len(file_id_finds) > 1:
                breakpoint()
            elif len(file_id_finds) > 0:    
                
                download_url = get_html(f'https://downloadt.advantech.com/download/downloadsr.aspx?File_Id={file_id_finds[0]}', aspx = True)
                if download_url not in download_list:
                    print(f'download_url > {download_url}')
                    download_list.append(download_url)
                    f.write(f'{download_url}\n')
f.close()