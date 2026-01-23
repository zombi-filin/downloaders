import re
import urllib.request
import urllib.parse
import json

def get_data(url, data = None):
    ''' Функция возвращает HTML код страницы по url или None если 404'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'referer' : 'https://support.getac.com/Service/F0021/Index?lang=100020&region=100025'
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


base = {
'100095':[
  {
    "Key": "100098",
    "Value": "A790(791901190XXX)"
  },
  {
    "Key": "100179",
    "Value": "B300G4(52628540XXXX)"
  },
  {
    "Key": "100184",
    "Value": "B300G5(52628591XXXX)"
  },
  {
    "Key": "100203",
    "Value": "B300G6(52628800XXXX)"
  },
  {
    "Key": "100218",
    "Value": "B300G7(52628955XXXX)"
  },
  {
    "Key": "100167",
    "Value": "B300H(52628417XXXX)"
  },
  {
    "Key": "100156",
    "Value": "B300X(52628317XXXX)"
  },
  {
    "Key": "100235",
    "Value": "B360G1(52629010XXXX)"
  },
  {
    "Key": "100252",
    "Value": "B360G2(5262GA02XXXX)"
  },
  {
    "Key": "100289",
    "Value": "B360G3(5262GB46XXXX)"
  },
  {
    "Key": "100293",
    "Value": "B360G3PLUS(5262GB465XXX)"
  },
  {
    "Key": "100140",
    "Value": "M230N(52621161XXXX)"
  },
  {
    "Key": "100145",
    "Value": "M230N2(52621163XXXX)"
  },
  {
    "Key": "100119",
    "Value": "P470(791901270XXX)"
  },
  {
    "Key": "100155",
    "Value": "S400(52628307XXXX)"
  },
  {
    "Key": "100175",
    "Value": "S400G2(52628521XXXX)"
  },
  {
    "Key": "100188",
    "Value": "S400G3(52628657XXXX)"
  },
  {
    "Key": "100198",
    "Value": "S410G1(52628768XXXX)"
  },
  {
    "Key": "100210",
    "Value": "S410G2(52628862XXXX)"
  },
  {
    "Key": "100232",
    "Value": "S410G3(52629028XXXX)"
  },
  {
    "Key": "100240",
    "Value": "S410G4(52629177XXXX)"
  },
  {
    "Key": "100255",
    "Value": "S410G5(5262GA34XXXX)"
  },
  {
    "Key": "100287",
    "Value": "S510(5262GA89XXXX)"
  },
  {
    "Key": "100298",
    "Value": "S510AD(5262GC01XXXX)"
  },
  {
    "Key": "100174",
    "Value": "V100G4(52621259XXXX)"
  },
  {
    "Key": "100143",
    "Value": "V100M(52621253XXXX)"
  },
  {
    "Key": "100161",
    "Value": "V100X(52621255XXXX)"
  },
  {
    "Key": "100183",
    "Value": "V110G1(52621290XXXX)"
  },
  {
    "Key": "100191",
    "Value": "V110G2(52621292XXXX)"
  },
  {
    "Key": "100202",
    "Value": "V110G3(52621294XXXX)"
  },
  {
    "Key": "100214",
    "Value": "V110G4(52621296XXXX)"
  },
  {
    "Key": "100229",
    "Value": "V110G5(526215010XXX)"
  },
  {
    "Key": "100238",
    "Value": "V110G6(526215011XXX)"
  },
  {
    "Key": "100250",
    "Value": "V110G7(5262GA21XXXX)"
  },
  {
    "Key": "100297",
    "Value": "V120(5262GB82XXXX)"
  },
  {
    "Key": "100173",
    "Value": "V200G2(52621264XXXX)"
  },
  {
    "Key": "100162",
    "Value": "V200X(52621256XXXX)"
  },
  {
    "Key": "100165",
    "Value": "X500G1(52621280XXXX)"
  },
  {
    "Key": "100186",
    "Value": "X500G2(52621284XXXX)"
  },
  {
    "Key": "100212",
    "Value": "X500G3(52621285XXXX)"
  },
  {
    "Key": "100247",
    "Value": "X600G1(52621287XXXX)"
  }
],
'100096':[
  {
    "Key": "100206",
    "Value": "A140G1(52621401XXXX)"
  },
  {
    "Key": "100233",
    "Value": "A140G2(52621403XXXX)"
  },
  {
    "Key": "100299",
    "Value": "A140G2E(5262GB96XXXX)"
  },
  {
    "Key": "100176",
    "Value": "E110(52628495XXXX)"
  },
  {
    "Key": "100211",
    "Value": "EX80(52628742XXXX)"
  },
  {
    "Key": "100182",
    "Value": "F110G1(52628571XXXX)"
  },
  {
    "Key": "100190",
    "Value": "F110G2(52628707XXXX)"
  },
  {
    "Key": "100201",
    "Value": "F110G3(52628783XXXX)"
  },
  {
    "Key": "100208",
    "Value": "F110G4(52628887XXXX)"
  },
  {
    "Key": "100231",
    "Value": "F110G5(52629018XXXX)"
  },
  {
    "Key": "100237",
    "Value": "F110G6(52629180XXXX)"
  },
  {
    "Key": "100276",
    "Value": "F110G7(5262GA45XXXX)"
  },
  {
    "Key": "100288",
    "Value": "F120(5262GB76XXXX)"
  },
  {
    "Key": "100223",
    "Value": "K120G1(52621420XXXX)"
  },
  {
    "Key": "100241",
    "Value": "K120G2(52621446XXXX)"
  },
  {
    "Key": "100282",
    "Value": "K120G3(5262GB19XXXX)"
  },
  {
    "Key": "100204",
    "Value": "MX50(52628730XXXX)"
  },
  {
    "Key": "100197",
    "Value": "RX10G1(52628719XXXX)"
  },
  {
    "Key": "100220",
    "Value": "RX10G2(52628970XXXX)"
  },
  {
    "Key": "100187",
    "Value": "T800G1(52621221XXXX)"
  },
  {
    "Key": "100199",
    "Value": "T800G2(52621228XXXX)"
  },
  {
    "Key": "100228",
    "Value": "UX10G1(526214110XXX)"
  },
  {
    "Key": "100236",
    "Value": "UX10G2(526214111XXX)"
  },
  {
    "Key": "100251",
    "Value": "UX10G3(5262GA01XXXX)"
  },
  {
    "Key": "100296",
    "Value": "UX10G5(5262GB99XXXX)"
  },
  {
    "Key": "100177",
    "Value": "Z710(52628476XXXX)"
  },
  {
    "Key": "100246",
    "Value": "ZX10G1(52629190XXXX)"
  },
  {
    "Key": "100290",
    "Value": "ZX10G2(5262GB11XXXX)"
  },
  {
    "Key": "100205",
    "Value": "ZX70G1(52628791XXXX)"
  },
  {
    "Key": "100230",
    "Value": "ZX70G2(52621443XXXX)"
  },
  {
    "Key": "100278",
    "Value": "ZX80(5262GA75XXXX)"
  }
],
'100132':[
    {
        "Key": "100144",
        "Value": "PS236(52628209XXXX)"
    },
    {
        "Key": "100168",
        "Value": "PS236EXT(52628387XXXX)"
    },
    {
        "Key": "100178",
        "Value": "PS336(52628498XXXX)"
    },
    {
        "Key": "100142",
        "Value": "PS535F(52628215XXXX)"
    },
    {
        "Key": "100151",
        "Value": "PS535F(52628306XXXX)"
    }
    ],
'100147':[
  {
    "Key": "100234",
    "Value": "Getac Device Monitoring System"
  },
  {
    "Key": "100226",
    "Value": "Getac Driving Safety Utility"
  },
  {
    "Key": "100227",
    "Value": "Getac KeyWedge Utility"
  },
  {
    "Key": "100283",
    "Value": "Getac Management"
  },
  {
    "Key": "100284",
    "Value": "Getac Monitoring"
  },
  {
    "Key": "100245",
    "Value": "Getac OEMConfig"
  },
  {
    "Key": "100295",
    "Value": "Getac SmartUpdate"
  },
  {
    "Key": "100239",
    "Value": "Getac VGPS Utility"
  },
  {
    "Key": "100277",
    "Value": "Getac Voice"
  },
  {
    "Key": "100242",
    "Value": "Getac deployXpress"
  },
  {
    "Key": "100248",
    "Value": "Getac enrollXpress"
  },
  {
    "Key": "100244",
    "Value": "Open source"
  }
],
'100192':[
  {
    "Key": "100258",
    "Value": "BC-01(41287670XXXX)"
  },
  {
    "Key": "100259",
    "Value": "BC-03(53168947XXXX)"
  },
  {
    "Key": "100271",
    "Value": "BC-4K(53169185XXXX)"
  },
  {
    "Key": "100219",
    "Value": "CA-NF21(53168928XXXX)"
  },
  {
    "Key": "100272",
    "Value": "CA-NF21A(53169099XXXX)"
  },
  {
    "Key": "100273",
    "Value": "CA-NF22(53169069XXXX)"
  },
  {
    "Key": "100292",
    "Value": "CA-NF22G2(5316GB85XXXX)"
  },
  {
    "Key": "100274",
    "Value": "CA-NF42(5316GA15XXXX)"
  },
  {
    "Key": "100217",
    "Value": "CU-D50(52118692XXXX)"
  },
  {
    "Key": "100207",
    "Value": "MD-02D(52628906XXXX)"
  },
  {
    "Key": "100200",
    "Value": "VD-01(54138767XXXX)"
  },
  {
    "Key": "100196",
    "Value": "VH-C10(52558692XXXX)"
  },
  {
    "Key": "100193",
    "Value": "VR-X10(52658688XXXX)"
  },
  {
    "Key": "100286",
    "Value": "VR-X20 DH(526589441XXX)"
  },
  {
    "Key": "100243",
    "Value": "VR-X20 F1(526589441XXX)"
  },
  {
    "Key": "100216",
    "Value": "VR-X20(526589440XXX)"
  },
  {
    "Key": "100249",
    "Value": "VR-X20G2(5265GA140XXX)"
  },
  {
    "Key": "100281",
    "Value": "VR-X20G3(5265GB010XXX)"
  }
],
'100221':[
  {
    "Key": "100222",
    "Value": "VR-X20PC(52628974XXXX)"
  }
],
'100224':[
  {
    "Key": "100256",
    "Value": "Adapter"
  },
  {
    "Key": "100294",
    "Value": "Battery Charger"
  },
  {
    "Key": "100279",
    "Value": "DS100"
  },
  {
    "Key": "100257",
    "Value": "Docking"
  },
  {
    "Key": "100225",
    "Value": "VKB10"
  }
],
}

download_urls = []

for product_id in base:
    for model in base[product_id]:
        model_name = model['Value']
        print(f'get product_id:{product_id} model:{model_name}')
        url = 'https://support.getac.com/Service/F0021/Index'
        data = {
            'txtkeyword' : '',
            'ddlProductList' : product_id,
            'ddlModelList' : model['Key'],
            'ddlOSList' : '',
            'region' : '100025',
            'lang' : '100130',
            'hidProductTypeId' : product_id,
            'hidProductTypeName' : '',
            'hidModelId' : model['Key'],
            'hidModelName' : '',
            'hidFileGroupId' : '',
            'hidFileGroupName' : '',
            'hidFileOSId' : '',
            'hidFileOSName':'',
            'hidSearchText' : ''
        }
        model_data = get_data(url , data)
        model_list = model_data.split('\n')
        for line in model_list:
            regx = r'\"https:\/\/support\.getac\.com\/Service\/FileReader\/Index\?([^\"]+)'
            find = findlinks = re.findall(regx, line)
            if len(find)>0:
                link = 'https://support.getac.com/Service/FileReader/Index?' + find[0]
                if link not in download_urls:
                    print(link)
                    download_urls.append(link)
# 
with open('support_getac_com.txt', 'w') as f:
    for line in download_urls:
        f.write(f'{line}\n')

print('DONE')