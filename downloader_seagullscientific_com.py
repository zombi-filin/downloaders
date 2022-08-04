import re
import urllib.request

url = 'https://www.seagullscientific.com/support/downloads/drivers/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
request = urllib.request.Request(url, None, headers)
response = urllib.request.urlopen(request)
html = response.read().decode('utf-8')

regx = r'href="https://www.seagullscientific.com/support/downloads/drivers/([^\"]+)'
pages = re.findall(regx, html)
f = open("seagullscientific.com.txt", "w")
for i in range(len(pages)):
    url = 'https://www.seagullscientific.com/support/downloads/drivers/' + \
        pages[i] + '/download/'
    request = urllib.request.Request(url, None, headers)
    try:
        response = urllib.request.urlopen(request)
    except:
        print(str(i+1) + '/' + str(len(pages)) + ' ' + pages[i] + ' Error: Get ' + url)
        continue

    html = response.read().decode('utf-8')
    regx = r'//([^\.]+).cloudfront.net/Drivers/([^\"]+)'
    findlinks = re.findall(regx, html)
    if (len(findlinks) == 0):
        print(str(i+1) + '/' + str(len(pages)) + ' ' + pages[i] + ' Error: No link ' + url)
        continue
    link = 'https://'+findlinks[0][0] + '.cloudfront.net/Drivers/'+findlinks[0][1]
    f.write(link +'\n')
    print(str(i+1) + '/' + str(len(pages)) + ' ' + pages[i] + ' ' + link)
f.close()