import re
import urllib.request
import json
import os

tmp_dir = 'advantech_com'
page_ids_dir = os.path.join(tmp_dir, 'page_ids')
file_ids_dir = os.path.join(tmp_dir, 'file_ids')

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
# 
if not os.path.isdir(tmp_dir):
    os.mkdir(tmp_dir)
# 
if not os.path.isdir(page_ids_dir):
    os.mkdir(page_ids_dir)
# 
if not os.path.isdir(file_ids_dir):
    os.mkdir(file_ids_dir)
#
# Создание файлов ID страниц
search_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
for suf in search_list:
    # Делаем запрос на список ID страниц
    id_list_src = get_html(f'https://apis-corp.advantech.com/api/v1/search/documents/support?q={suf}&lang=en&use_fuzzy=true&data_types=Driver&page_index=1&page_size=10000')
    # Парсим в JSON результат ответа
    id_list_json = json.loads(id_list_src)
    # Берем количество ID из результата запроса
    pages_all_count = int(id_list_json['count'])
    # Если количество более 10000 отладка
    if pages_all_count > 10000:
        breakpoint()
    # Счетчик обработанных страниц
    pages_count = 0

    print(f'{suf} > {pages_all_count}')
          
    # Проходим по списку ID страниц
    for line_json in id_list_json['documents']:
        # Увеличиваем счетчик обработанных страниц
        pages_count += 1
        # Берем ID страницы
        page_id_path = os.path.join(page_ids_dir,line_json['id'])

        if not os.path.exists(page_id_path):
            open(page_id_path, 'w')
        continue
#
# Обработка файлов ID страниц
file_id_regex = r'\/downloadsr\.aspx\?File_Id=(.*)\"\starget'
page_ids_list = os.listdir(page_ids_dir)
page_ids_all_count = len(page_ids_list)
page_ids_count = 0
for page_id in page_ids_list:
    page_ids_count += 1
    print(f'page_ids > {page_ids_count}/{page_ids_all_count}', end='\r')
    page_id_file = os.path.join(page_ids_dir, page_id)
    
    if os.path.getsize(page_id_file) > 0:
        continue
    
    # Запрашиваем HTLM страницы по ID
    page_src = get_html(f'https://www.advantech.com/en/support/details/driver?id={page_id}')
    
    if page_src is None:
        continue

    # Парсим с разбивкой по строкам
    page_scr_list = page_src.split('\r\n')
    # Флаг блока закачки
    is_downloadContent = False
    # Проходим построчно
    for page_src_line in page_scr_list:
        # Определяем начало блока закачки
        if page_src_line == '            <!---Start of downloadContent-->':
            is_downloadContent = True
            continue
        # Определяем конец блока закачки
        if page_src_line == '            <!--End of downloadContent -->':
            break
        # Если не в блоке не обрабатываем
        if not is_downloadContent:
            continue
        # Ищем ID закачки
        file_id_finds = re.findall(file_id_regex, page_src_line)
        # Если нашли в строе более 1 отладка
        if len(file_id_finds) > 1:
            breakpoint()
        # Если корректно нашли ID закачки
        elif len(file_id_finds) == 1:
            file_id_path = os.path.join(file_ids_dir, file_id_finds[0])
            if not os.path.exists(file_id_path):
                open(file_id_path, 'w')
    with open(page_id_file, 'w') as f:
        f.write('DONE')
#
# Обработка файлов ID закачек
file_ids_list = os.listdir(file_ids_dir)
file_ids_all_count = len(file_ids_list)
file_ids_count = 0
for file_id in file_ids_list:
    file_ids_count += 1
    print(f'file_ids > {file_ids_count}/{file_ids_all_count}', end='\r')
    file_id_file = os.path.join(file_ids_dir, file_id)
    
    if os.path.getsize(file_id_file) > 0:
        continue

    download_url = get_html(f'https://downloadt.advantech.com/download/downloadsr.aspx?File_Id={file_id}', aspx = True)
    if download_url is None:
        continue
    with open(file_id_file, 'w') as f:
        f.write(download_url)
# 
# Конец скрипта
print('\n> DONE')