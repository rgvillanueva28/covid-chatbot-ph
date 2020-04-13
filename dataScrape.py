# import bs4
import requests
import json
from collections import Counter

def getData():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }

    website = r"https://coronavirus-ph-api.herokuapp.com/cases"
    website2 = r"https://coronavirus-ph-api.herokuapp.com/facilities"
    website3 = r"https://covid19.mathdro.id/api/countries/philippines"
    #website4 = r"https://services5.arcgis.com/mnYJ21GiFTR97WFg/arcgis/rest/services/conf_fac_tracking/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=count_%20desc&resultOffset=0&resultRecordCount=50&cacheHint=true"

    res = requests.get(website, headers, verify=False)
    res2 = requests.get(website2, headers, verify=False)
    res3 = requests.get(website3, headers, verify=False)
    #res4 = requests.get(website4, headers, verify=False)

    jsonContent = json.loads(res.content.decode())
    jsonContent2 = json.loads(res2.content.decode())
    jsonContent3 = json.loads(res3.content.decode())
    #cases = res.json()
    #print(res.raise_for_status())
    #jsonContent2 = res2.json()
    #jsonContent3 = res3.json()
    #jsonContent4 = res4.json()
    # res.raise_for_status()

    # soup = bs4.BeautifulSoup(res.content, 'html.parser').text
    #sleep(5)
    #ember1385 > svg > g.responsive-text-label > svg > text
    #content = soup.select('body > pre')
    #print(content)

    for case in jsonContent:
        #break
        #for key, value in case.items():
            #print(value['residence'])
            #print(value['residence'])
        case['resident_of'] = case['resident_of'].replace(r'�', r'N')
        case['resident_of'] = case['resident_of'].replace(r'ñ', r'N')
        case['resident_of'] = case['resident_of'].replace(r'ё', r'N')
        case['hospital_admitted_to'] = case['hospital_admitted_to'].replace(r'�', r'N')
        case['hospital_admitted_to'] = case['hospital_admitted_to'].replace(r'ñ', r'N')
        case['hospital_admitted_to'] = case['hospital_admitted_to'].replace(r'ё', r'N')

    for facility in jsonContent2:
        #print(facility)
        #break
        facility['facility'] = facility['facility'].replace(r'�', r'N')
        facility['facility'] = facility['facility'].replace(r'ñ', r'N')
        facility['facility'] = facility['facility'].replace(r'ё', r'N')
        #print(facility)
        #break

    
    jsonContent4 = jsonContent
    jsonContent4 = dict(Counter(case['resident_of'] for case in jsonContent4))
    #print(counts)

    #jsonContent4 = jsonContent
    #counts =  dict(Counter(case for case in jsonContent4))
    #print(counts)

    #for stat in jsonContent3:
    #print(jsonContent3)
    #print(counts)


    # for case in jsonContent3:
    #     try:
    #         confirmed = Counter(case["status"])
    #         print(confirmed)
    #     except Exception as ex:
    #         print(ex)


    # for features in jsonContent3['features']:
    #     for key, value in features.items():
    #         #print(value['residence'])
    #         #print(value['residence'])
    #         value['residence'] = value['residence'].replace(r'�', r'n')
    #         value['residence'] = value['residence'].replace(r'ñ', r'n')

    # for features in jsonContent4['features']:
    #     for key, value in features.items():
    #         #print(value['residence'])
    #         #print(value['residence'])
    #         value['facility'] = value['facility'].replace(r'�', r'n')
    #         value['facility'] = value['facility'].replace(r'ñ', r'n')

    with open('masterList.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent, jsonOutFile, ensure_ascii=False)

    with open('facilityStats.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent2, jsonOutFile, ensure_ascii=False)

    with open('statistics.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent3, jsonOutFile, ensure_ascii=False)

    with open('locationStats.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent4, jsonOutFile, ensure_ascii=False)

#getData()