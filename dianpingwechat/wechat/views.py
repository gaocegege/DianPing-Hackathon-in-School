#coding=utf-8
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
import time
import hashlib

from settings import WECHAT_TOKEN as TOKEN
import json
import polls.views as VU


@csrf_exempt
def index(request):
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request), content_type="text/plain")
        return response
    elif request.method == 'POST':
        response = HttpResponse(responseMsg(request), content_type="text/xml")
        return response
    else:
        return "UNSUPPORT METHOD"


def checkSignature(request):
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr", None)

    token = TOKEN
    tmpList = [token, timestamp, nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echoStr
    else:
        return "WEIXIN INDEX"


def responseMsg(request):
    try:
        xml_str = smart_str(request.body)
        request_xml = ET.fromstring(xml_str)
        msg = paraseMsgXml(request_xml)
        if msg['MsgType'] == 'location':
            VU.updateLocation(msg['FromUserName'], float(msg['Location_Y']), float(msg['Location_X']))
            return getReplyXml(msg, '')
        elif msg['MsgType'] == 'event':
            if msg['Event'] == 'LOCATION':
                VU.updateLocation(msg['FromUserName'], float(msg['Longitude']), float(msg['Latitude']))
                return getReplyXml(msg, '')
            elif msg['Event'] == 'CLICK':
                rid = VU.createPoll(msg['FromUserName'])
                return getReplyXml(msg, '您的房间已经创建好，房间号为' + str(rid) + '，您可以让您的小伙伴在聊天栏里输入此房间号进入房间。')
        elif msg['MsgType'] == 'text':
            return getReplyXml(msg, VU.joinPoll(int(msg['Content'])))
    except:
        return "<xml></xml>"


def paraseMsgXml(rootElem):
    msg = {}
    for child in rootElem:
        msg[child.tag] = child.text
    return msg


def getReplyXml(msg, replyContent):
    extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA["\
             "%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA["\
             "%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    extTpl = extTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', replyContent)
    return extTpl


