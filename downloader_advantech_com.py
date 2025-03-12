import re
import urllib.request
import json

search_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
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

opened_ids = []
download_links = []
download_links_count = 0

# Проходимся по списку поиска
for suf in search_list:
    # Делаем запрос на список ID страниц
    id_list_src = get_html(f'https://apis-corp.advantech.com/api/v1/search/documents/support?q={suf}&lang=en&use_fuzzy=false&data_types=Driver&page_index=1&page_size=1000')
    # Парсим в JSON результат ответа
    id_list_json = json.loads(id_list_src)
    # Берем количество ID из результата запроса
    pages_all_count = int(id_list_json['count'])
    # Если количество более 1000 отладка
    if pages_all_count > 1000:
        breakpoint()
    # Счетчик обработанных страниц
    pages_count = 0    
    # Проходим по списку ID страниц
    for line_json in id_list_json['documents']:
        # Увеличиваем счетчик обработанных страниц
        pages_count += 1
        # Берем ID страницы
        page_id = line_json['id']
        # Лог
        print(f'{suf} > {pages_count}/{pages_all_count} > {page_id}')
        # Проверяем обрабатывали уже страницу
        if page_id in opened_ids:
            continue
        opened_ids.append(page_id)
        # Запрашиваем HTLM страницы по ID
        page_src = get_html(f'https://www.advantech.com/en/support/details/driver?id={page_id}')
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
                # Запрашиваем URL загрузки через ID загрузки
                download_url = get_html(f'https://downloadt.advantech.com/download/downloadsr.aspx?File_Id={file_id_finds[0]}', aspx = True)
                # Если нет в списке найденых
                if download_url not in download_links:
                    # Увеличиваем счетчик найденых URL
                    download_links_count += 1
                    # Лог
                    print(f'download_url #{download_links_count} > {download_url}')
                    # Добавляем в список найденых
                    download_links.append(download_url)                    
# Сохраняем результат
print('> SAVE TO FILE')
f = open('advantech.com.txt', 'w')
for line in download_links:
    f.write(f'{line}\n')
f.close()
# Конец скрипта
print('> DONE')