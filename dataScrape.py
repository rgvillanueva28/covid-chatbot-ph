# import bs4
import requests
import json
from collections import Counter

def getData():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }

    website = r"https://coronavirus-ph-api.herokuapp.com/cases/"
    website2 = r"https://coronavirus-ph-api.herokuapp.com/facilities/"
    website3 = r"https://coronavirus-ph-api.herokuapp.com/total/"
    #website4 = r"https://services5.arcgis.com/mnYJ21GiFTR97WFg/arcgis/rest/services/conf_fac_tracking/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=count_%20desc&resultOffset=0&resultRecordCount=50&cacheHint=true"

    res = requests.get(website)
    res2 = requests.get(website2)
    res3 = requests.get(website3)
    #res4 = requests.get(website4, headers, verify=False)

    jsonContent = json.loads(res.content.decode())
    jsonContent2 = json.loads(res2.content.decode())
    jsonContent3 = json.loads(res3.content.decode())

    for case in jsonContent['data']:
        #break
        
        case['residence_in_the_ph'] = case['residence_in_the_ph'].replace(r'�', r'n')
        case['residence_in_the_ph'] = case['residence_in_the_ph'].replace(r'ñ', r'n')
        case['residence_in_the_ph'] = case['residence_in_the_ph'].replace(r'ё', r'n')
        case['hospital_admitted_to'] = case['hospital_admitted_to'].replace(r'�', r'n')
        case['hospital_admitted_to'] = case['hospital_admitted_to'].replace(r'ñ', r'n')
        case['hospital_admitted_to'] = case['hospital_admitted_to'].replace(r'ё', r'n')

    for facility in jsonContent2['data']:
        #print(facility)
        #break
        facility['facility'] = facility['facility'].replace(r'�', r'n')
        facility['facility'] = facility['facility'].replace(r'ñ', r'n')
        facility['facility'] = facility['facility'].replace(r'ё', r'n')

    
    jsonContent4 = jsonContent
    jsonContent4 = dict(Counter(case['residence_in_the_ph'] for case in jsonContent4['data']))
    #print(counts)


    with open('masterList.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent, jsonOutFile, ensure_ascii=False)

    with open('facilityStats.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent2, jsonOutFile, ensure_ascii=False)

    with open('statistics.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent3, jsonOutFile, ensure_ascii=False)

    with open('locationStats.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent4, jsonOutFile, ensure_ascii=False)

if __name__ == '__main__':
    getData()