#coding=utf-8
from polls.models import Poll, Choice, User, Dish
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from django.utils import timezone
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import dianping
import json

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    ids = json.loads(request.body)["id"]
    for myid in ids:
        selected_choice = p.choice_set.get(business_id=myid)
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponse(request.body)


@csrf_exempt
def result(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    cs = list(poll.choice_set.all().order_by('votes')[::-1])
    ls = []
    for c in cs:
        d = {}
        d['business_id'] = c.business_id
        d['name'] = c.name
        d['votes'] = c.votes
        ls.append(d)
    return HttpResponse(json.dumps(ls, ensure_ascii=False, indent=2))


def createPoll(create_user):
    p = Poll(pub_date=timezone.now(), create_user=create_user)
    p.save()
    return p.id


def joinPoll(poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
        if len(poll.choice_set.all()) == 0:
            return '<a href="http://dianpingwechat.sinaapp.com/static/weixinpage/id.html#idresult?' + str(
                poll_id) + '">点击进入房间。</a>'
        return '<a href="http://dianpingwechat.sinaapp.com/static/weixinpage/id.html#votepage?' + str(
            poll_id) + '">点击进入房间。</a>'
    except Poll.DoesNotExist:
        return "无效文本"


def updateLocation(user_name, longitude, latitude):
    try:
        user = User.objects.get(user_name=user_name)
    except User.DoesNotExist:
        user = User(user_name=user_name)
    user.longitude = longitude
    user.latitude = latitude
    user.save()
    return


def roomDetail(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        return HttpResponse('{}')
    if len(poll.json_string) == 0:
        user = User.objects.get(user_name=poll.create_user)
        poll.json_string = dianping.dianping(user.longitude, user.latitude)
        jsonObject = json.loads(poll.json_string)
        cs = poll.choice_set
        for business in jsonObject['businesses']:
            business_id = business['business_id']
            name = business['name']
            s_photo_url = business['s_photo_url']
            rating_img_url = business['rating_img_url']
            c = Choice(business_id=business_id, name=name, s_photo_url=s_photo_url, rating_img_url=rating_img_url)
            cs.add(c)
        c = Choice(business_id=2552704, name='一茶一坐(龙之梦店)', s_photo_url='http://i1.dpfile.com/2008-08-25/852885_m.jpg',
                   rating_img_url='http://i2.dpfile.com/s/i/app/api/32_0star.png')
        cs.add(c)
        poll.save()
    return HttpResponse(poll.json_string, mimetype='application/json')


def menu(request, shop_id, poll_id):
    dish = Dish.objects.filter(poll_id=poll_id)
    if len(dish) == 0:
        return HttpResponse(dianping.menu(shop_id, poll_id), mimetype='application/json')
    else:
        result = []
        for i in dish:
            entry = {}
            entry['id'] = i.id
            entry['dish_name'] = i.dish_name
            entry['price'] = i.price
            entry['category'] = i.category
            entry['amount'] = i.amount
            result.append(entry)
    return HttpResponse(json.dumps(result, ensure_ascii=False, indent=2), mimetype='application/json')

def menu2(request, shop_id, poll_id):
    dish = Dish.objects.filter(poll_id=poll_id)
    if len(dish) == 0:
    #if True:
        return HttpResponse(dianping.menu2(shop_id, poll_id), mimetype='application/json')
    else:
        res1 = []
        category='';
        res2={}
        res3=[]
        for i in dish[::-1]:
            if category==i.category:
                entry={}
                entry['id'] = i.id
                entry['dish_name'] = i.dish_name
                entry['price'] = i.price
                entry['amount'] = i.amount
                res3.append(entry)
            else:
                if (len(res3)>0):
                    res2['dishes']=res3
                    res1.append(res2)
                category=i.category
                res2={}
                res2['category']=category
                res3=[]
                entry = {}
                entry['id'] = i.id
                entry['dish_name'] = i.dish_name
                entry['price'] = i.price
                entry['amount'] = i.amount
                res3.append(entry)
        res2['dishes']=res3
        res1.append(res2)
    print res1
    return HttpResponse(json.dumps(res1, ensure_ascii=False, indent=2), mimetype='application/json')


def adddish(request, dish_name, poll_id):
    try:
        dish = Dish.objects.get(dish_name=dish_name, poll_id=poll_id)
    except Poll.DoesNotExist:
        return HttpResponse('{}')
    dish.amount = dish.amount + 1
    dish.save()
    return HttpResponse(str(dish.amount))


def deldish(request, dish_name, poll_id):
    try:
        dish = Dish.objects.get(dish_name=dish_name, poll_id=poll_id)
    except Poll.DoesNotExist:
        return HttpResponse('{}')
    if dish.amount > 0:
        dish.amount = dish.amount - 1
    dish.save()
    return HttpResponse(str(dish.amount))


def checkorder(request, poll_id):
    try:
        dish = Dish.objects.filter(poll_id=poll_id, amount__gt=0)
        result = []
        for i in dish:
            entry = {}
            entry['id'] = i.id
            entry['dish_name'] = i.dish_name
            entry['price'] = i.price
            entry['category'] = i.category
            entry['amount'] = i.amount
            result.append(entry)
    except Poll.DoesNotExist:
        return HttpResponse('[]')
    return HttpResponse(json.dumps(result, ensure_ascii=False, indent=2), mimetype='application/json')