#coding=utf-8
__author__ = 'jingyuan'

import hashlib
import urllib
import json
from bs4 import BeautifulSoup
from polls.models import Dish
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def dianping(longitude, latitude):
    appkey = "99946310"
    secret = "69c47baf99354bd8a9e1669183413153"
    apiUrl = "http://api.dianping.com/v1/business/find_businesses"

    paramSet = []
    paramSet.append(("format", "json"))
    paramSet.append(("latitude", str(latitude)))
    paramSet.append(("longitude", str(longitude)))
    paramSet.append(("category", "美食"))
    paramSet.append(("limit", "20"))
    paramSet.append(("radius", "2000"))
    paramSet.append(("offset_type", "0"))
    paramSet.append(("sort", "7"))

    paramMap = {}
    for pair in paramSet:
        paramMap[pair[0]] = pair[1]

    codec = appkey
    for key in sorted(paramMap.iterkeys()):
        codec += key + paramMap[key]

    codec += secret

    sign = (hashlib.sha1(codec).hexdigest()).upper()

    url_trail = "appkey=" + appkey + "&sign=" + sign
    for pair in paramSet:
        url_trail += "&" + pair[0] + "=" + pair[1]

    requestUrl = apiUrl + "?" + url_trail

    response = urllib.urlopen(requestUrl)
    return response.read()


def menu(shopid, poll_id):
    html= urllib.urlopen('http://www.dianping.com/shop/'+str(shopid)+'/menu').read()
    result = []
    soup = BeautifulSoup(html)
    list = soup.findAll('div', 'menus-mode')
    for i in list:
        category = i['id']
        detail = BeautifulSoup(str(i))
        item = detail.findAll('li', 'dish-item')
        for j in item:
            sol = BeautifulSoup(str(j))
            dish = sol.findAll('span', 'name')
            dish_name = dish[0]['dish-name']
            p = sol.findAll('em')
            price = float(str(p[0].string))
            _dish=Dish()
            _dish.amount=0
            _dish.dish_name=dish_name
            _dish.price=price
            _dish.category=category
            _dish.poll_id=poll_id
            _dish.save()
            entry = {}
            entry['dish_name'] = dish_name
            entry['category'] = category
            entry['price'] = price
            entry['amount']=0
            entry['id']=_dish.id;
            result.append(entry)
    content= json.dumps(result, ensure_ascii=False, indent=2)
    return content

def menu2(shopid, poll_id):
    html= urllib.urlopen('http://www.dianping.com/shop/'+str(shopid)+'/menu').read()
    res1 = []
    soup = BeautifulSoup(html)
    list = soup.findAll('div', 'menus-mode')
    for i in list:
        category = i['id']
        res2={}
        res2['category']=category
        res3=[]
        detail = BeautifulSoup(str(i))
        item = detail.findAll('li', 'dish-item')
        for j in item:
            sol = BeautifulSoup(str(j))
            dish = sol.findAll('span', 'name')
            dish_name = dish[0]['dish-name']
            p = sol.findAll('em')
            price = float(str(p[0].string))
            _dish=Dish()
            _dish.amount=0
            _dish.dish_name=dish_name
            _dish.price=price
            _dish.category=category
            _dish.poll_id=poll_id
            _dish.save()
            entry = {}
            entry['dish_name'] = dish_name
            entry['price'] = price
            entry['amount']=0
            entry['id']=_dish.id;
            res3.append(entry)
        res2['dishes']=res3
        res1.append(res2)
    content= json.dumps(res1, ensure_ascii=False, indent=2)
    return content


if __name__=='__main__':
    print dianping()