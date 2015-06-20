# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json,urllib
from lxml import etree


class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        code=data.code
        #应用 的参数
        appid = "wx250d00817156085c"
        appsecret="50c6b69c831f811d4d723990abec6173"
        #oauth2的方式获得openid
        access_token_url='https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(appid,appsecret,code)
        res = urllib.urlopen(access_token_url)
        r = json.loads(res.read())
        openId=r['openid']
        accessToken=r['access_token']
        #req = urllib2.Request(access_token_url)
        '''data = urllib.urlopen(access_token_url)
        jsonData = data.read()
        dictData=json.loads(jsonData)
        openId=dictData[openid]
        access_Token=dictData[access_token]'''
        
        #获取用户信息
        url='https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN'%(accessToken,openId)
        #req1 = urllib2.Request(url)
        data = urllib.urlopen(url)
        jsonData = data.read()    
        dictData=json.loads(jsonData)
        name=dictData['nickname']
        sex=dictData['sex']
        city=dictData['city']
        province=dictData['province']
        country=dictData['country']
        return self.render.userInfo(name,sex,city,province,country)        
        #return self.render.userInfo(1,2,3,4,5)
        '''signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="weixin" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr'''
        
    def POST(self):
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        return self.render.reply_text(fromUser,toUser,int(time.time()),content)