import urllib.request
import urllib.parse
import json

def get_data(url, data = None):
    ''' Функция возвращает HTML код страницы по url или None если 404'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    if data is not None:
        data_encode = urllib.parse.urlencode(data).encode()
    else:
        data_encode = None
    request = urllib.request.Request(url, data_encode, headers)
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        if hasattr(e,'code') and (e.code == 404):
            return None
        elif hasattr(e,'code') and (e.code == 500):
            return '[]'
        else:
            return get_data(url, data) 
    if response.code == 404:
        return None
    else:
        return response.read().decode('utf-8')

exclude_dirs = [
    'manual'
]

dir_list = []

download_list = []

alias_list = [
    "mobile",
    "handsfree",
    "note_docks",
    "portable_speakers",
    "card_reader",
    "mini_systems",
    "phone",
    "tablet_pc",
    "fitness_bracelets",
    "cellphones_chargers",
    "cables",
    "backup_battery",
    "computers",
    "microphones",
    "gameaudio",
    "monoblocks",
    "extension-cords",
    "kits",
    "keyboards",
    "mouses",
    "monitors",
    "games_consoles",
    "ssd",
    "notebooks_and_computers",
    "note_bags",
    "audio_and_video",
    "receivers",
    "tv",
    "wall_brackets",
    "powersafe",
    "stabilizer",
    "battery",
    "ups",
    "home_appliances",
    "convectors",
    "air_humidifiers",
    "cleaners",
    "kitchen_appliances",
    "table_cookers",
    "bread-makers",
    "drying_vegetables",
    "kitchen_scales",
    "sandwich_makers",
    "thermopots",
    "multicooker",
    "mini_ovens",
    "kettles",
    "microwaves",
    "mixers",
    "meat_grinders",
    "large_appliances",
    "refrigerators",
    "washing_machines",
    "freezer",
    "sushilnye_mashiny",
    "climate_control",
    "air_conditioners",
    "pogodnye-stancii",
    "mobile_conditioners",
    "beauty",
    "hairdryers",
    "floor_scales",
    "car_accessories",
    "car_cams",
    "car_fridge"
]


for alias_str in alias_list:
    print(alias_str)
    url = 'https://sunwind.ru.com/catalog/get-info-group'
    data = {
        'alias': alias_str,
        'isFull': 0
    }
    group_src = get_data(url, data)
    group_json = json.loads(group_src)
    for products_id in group_json['products']:
        item_no = group_json['products'][products_id]['item_no']
        url = 'https://sunwind.ru.com/support/get-downloads'
        data = {
            'alias' : item_no
        }
        print(item_no)
        downloads_src = get_data(url, data)
        downloads_json = json.loads(downloads_src)
        for downlods_name in downloads_json:
            for downloads_item in downloads_json[downlods_name]:
                downloads_dir = downloads_item['dir']
                if downloads_dir in exclude_dirs:
                    continue
                
                if downloads_dir not in dir_list:
                    dir_list.append(downloads_dir)

                link = downloads_item['link']
                if link not in download_list:
                    download_list.append(link)

with open('sunwind_ru_com.txt', 'w') as f:
    for line in download_list:
        f.write(f'{line}\n')

print("DONE")

'''
Array.from(document.getElementsByClassName("option")).forEach(element => {
  console.log(element.getAttribute("data-alias"));
})

'''