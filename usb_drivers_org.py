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

#--------------------------------------------------------------
# main
#--------------------------------------------------------------

f = open('usb_drivers_org.txt', 'w')
# Список линков
links_list = []
# Список расширений
ext_list = []
# Счетчик страниц
page_index = 1
# 
exclude_ext_list = ['html', 'pdf']
# Цикл пока 
while page_index > 0:
    print(f'{page_index} > grab page')
    # Получаем страницу со списком драйверов
    page_html = get_html(f'https://www.usb-drivers.org/page/{page_index}')
    # Если страница не найдена прекращаем обработку
    if page_html is None:
        page_index = 0
        continue
    # Получаем список подстраниц с драйверами
    bookmark_regx = r'([-\w]+.html)\" rel=\"bookmark\"><'
    bookmark_finds = re.findall(bookmark_regx, page_html)
    bookmark_page_count = len(bookmark_finds)
    # Счетчик подстраниц
    bookmark_page_index = 1
    # Обработка списка подстраниц
    for bookmark_page in bookmark_finds:
        bookmark_page_prefix = f'{page_index} > {bookmark_page_index}/{bookmark_page_count} >'
        bookmark_url = f'https://www.usb-drivers.org/{bookmark_page}'
        print(f'{bookmark_page_prefix} grab bookmark > {bookmark_url}')
        bookmark_html = get_html(bookmark_url)
        # Ругулярка для поиска линков
        links_regx = r'<h4>[<\w\s=\"->]+href=\"([-:\/.\w]+)\"'
        # Цикл по строкам в коде подстраницы
        for bookmark_line in bookmark_html.split('\n'):
            # Поиск линков
            links_finds = re.findall(links_regx, bookmark_line)
            # Если в строке 1 линк
            if len(links_finds) == 1 :
                # Если линк не в списке добавленных
                if links_finds[0] not in links_list:
                    # Получение расширения файла
                    ext_regx = r'[\w]+\.([\w]+)$'
                    ext_finds = re.findall(ext_regx, links_finds[0])
                    if len(ext_finds) == 1:
                        if ext_finds[0] not in exclude_ext_list:
                            if ext_finds[0] not in ext_list:
                                ext_list.append(ext_finds[0])
                            # Добавляем в список линков
                            links_list.append(links_finds[0])
                            # Лог
                            print(f'{bookmark_page_prefix} add link > {links_finds[0]}')
                            # Записываем в файл
                            f.write(f'{links_finds[0]}\n')
                        else:
                            print(f'{bookmark_page_prefix} exclude link > {links_finds[0]}')
                else:
                    # Если в списке добавленных
                    print(f'{bookmark_page_prefix} exist link > {links_finds[0]}')
            # Если более 1 линка в строке , не нормально
            elif len(links_finds) > 1:
                pass
        # Увеличиваем счетчик подстраниц
        bookmark_page_index += 1
    # Увеличиваем счетчик страниц
    page_index += 1
# Конец скрипта
f.close()
print('DONE')