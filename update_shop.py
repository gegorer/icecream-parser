from lxml import etree
import urllib2
import urllib
import cookielib
import json
import mypprint

FAMILY_URL = 'http://www.family.com.tw/marketing/inquiry.aspx'
API_MAP = 'http://api.map.com.tw/net/familyShop.aspx'

def getAreaList(opener):
    fp = opener.open(FAMILY_URL)
    root = etree.parse(fp, etree.HTMLParser(encoding="UTF-8"))
    areas = root.xpath('//div[@id="taiwanMap"]/div/a/text()')
    return areas

def getTownList(opener, area):
    data = urllib.urlencode({
        'searchType': 'ShowTownList',
        'type': 'icecream',
        'city': area.encode('UTF-8'),
        'fun': 'storeTownList',
    })
    req = urllib2.Request(API_MAP + '?' + data)
    fp = opener.open(req)
    ret_str = fp.read().decode('UTF-8').lstrip("storeTownList(").rstrip(")")
    return json.loads(ret_str)

def getShopList(opener, town):
    data = urllib.urlencode({
        'searchType': 'ShopList',
        'type': 'icecream',
        'city': town['city'].encode('UTF-8'),
        'area': town['town'].encode('UTF-8'),
        'road': '',
        'fun': 'storeStoreList',
    })
    req = urllib2.Request(API_MAP + '?' + data)
    fp = opener.open(req)
    ret_str = fp.read().decode('UTF-8').lstrip("showStoreList(").rstrip(")")
    return json.loads(ret_str)

def main():
    #ret = {}
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    areaList = getAreaList(opener)
    allShop = []
    for area in areaList:
        townList = getTownList(opener, area)
        if townList:
            #ret[area] = {}
            for town in townList:
                shopList = getShopList(opener, town)
                allShop.extend(shopList)
                #ret[area][town['town']] = shopList
    #pp = mypprint.MyPrettyPrinter(indent=4)
    #pp.pprint(ret)
    json.dump(allShop, open('all-shop.json', 'w'))

if __name__ == '__main__':
    main()
