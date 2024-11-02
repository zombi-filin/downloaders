import re
import urllib.request

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

f = open("usb-drivers.org.txt", "w")

page_index = 1
while page_index < 5:
    url = f'https://www.usb-drivers.org/page/{page_index}'
    print(f'grab page# {page_index}')
    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    
    if response.code == 404:
        page_index = 0
        continue

    html = response.read().decode('utf-8')
    bookmark_regx = r'([-\w]+.html)\" rel=\"bookmark\"><'
    bookmark_finds = re.findall(bookmark_regx, html)
    
    for bookmark_page in bookmark_finds:
        bookmark_url = f'https://www.usb-drivers.org/{bookmark_page}'
        print(f'grab bookmark {bookmark_url}')
        bookmark_request = urllib.request.Request(bookmark_url, None, headers)
        bookmark_response = urllib.request.urlopen(bookmark_request)
        bookmark_html = bookmark_response.read().decode('utf-8')
        
        links_regx = r'<h4>[<\w\s=\"->]+href=\"([-:\/.\w]+)\"'
        h4_regx = r'<h4>([<\w\s=\"->]+)</h4>'
        h4_finds = re.findall(h4_regx, bookmark_html)
        for h4_block in h4_finds:
            links_regx = r'href=\"([\/:.\-\w]+)'
            links_finds = re.findall(links_regx, h4_block)
            for links_url in links_finds:
                print(f'find link {links_url}')
                f.write(f'{links_url}\n')
    page_index += 1
f.close()
print('DONE')