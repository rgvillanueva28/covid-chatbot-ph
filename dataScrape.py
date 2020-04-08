# import bs4
import requests
import json

def getData():
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }

    website = r"https://services5.arcgis.com/mnYJ21GiFTR97WFg/ArcGIS/rest/services/PH_masterlist/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=FID%20ASC"
    website2 = r"https://services5.arcgis.com/mnYJ21GiFTR97WFg/arcgis/rest/services/slide_fig/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*"
    website3 = r"https://services5.arcgis.com/mnYJ21GiFTR97WFg/ArcGIS/rest/services/PH_masterlist/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=residence&orderByFields=value%20desc&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22FID%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D"
    website4 = r"https://services5.arcgis.com/mnYJ21GiFTR97WFg/arcgis/rest/services/conf_fac_tracking/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=count_%20desc&resultOffset=0&resultRecordCount=50&cacheHint=true"

    res = requests.get(website, headers, verify=False)
    res2 = requests.get(website2, headers, verify=False)
    res3 = requests.get(website3, headers, verify=False)
    res4 = requests.get(website4, headers, verify=False)

    #jsonContent = json.loads(res.content.decode())
    jsonContent = res.json()
    jsonContent2 = res2.json()
    jsonContent3 = res3.json()
    jsonContent4 = res4.json()
    # res.raise_for_status()

    # soup = bs4.BeautifulSoup(res.content, 'html.parser').text
    #sleep(5)
    #ember1385 > svg > g.responsive-text-label > svg > text
    #content = soup.select('body > pre')
    #print(content)

    for features in jsonContent['features']:
        for key, value in features.items():
            #print(value['residence'])
            #print(value['residence'])
            value['residence'] = value['residence'].replace(r'�', r'n')
            value['residence'] = value['residence'].replace(r'ñ', r'n')

    for features in jsonContent3['features']:
        for key, value in features.items():
            #print(value['residence'])
            #print(value['residence'])
            value['residence'] = value['residence'].replace(r'�', r'n')
            value['residence'] = value['residence'].replace(r'ñ', r'n')

    for features in jsonContent4['features']:
        for key, value in features.items():
            #print(value['residence'])
            #print(value['residence'])
            value['facility'] = value['facility'].replace(r'�', r'n')
            value['facility'] = value['facility'].replace(r'ñ', r'n')

    with open('masterList.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent, jsonOutFile, ensure_ascii=False)

    with open('statistics.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent2, jsonOutFile, ensure_ascii=False)

    with open('locationStats.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent3, jsonOutFile, ensure_ascii=False)

    with open('facilityStats.json', 'w', encoding='utf-8') as jsonOutFile:
        json.dump(jsonContent4, jsonOutFile, ensure_ascii=False)

#getData()