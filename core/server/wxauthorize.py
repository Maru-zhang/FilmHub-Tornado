# -*- coding: utf-8 -*-
from core.logger_helper import logger
import hashlib
import tornado.web
import tornado.httpclient
from core.server.wxconfig import WxConfig
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import time
import re
from core.cache.tokencache import TokenCache
from core.cache.wxmediacache import WxMediaCache
import json
from tornado.httputil import url_concat
import requests
import os
from PIL import Image,ImageDraw,ImageFont

class WxAuthorServer(object):
    """
    微信网页授权server

    get_code_url                            获取code的url
    get_auth_access_token                   通过code换取网页授权access_token
    refresh_token                           刷新access_token
    check_auth                              检验授权凭证（access_token）是否有效
    get_userinfo                            拉取用户信息
    """

    """授权后重定向的回调链接地址，请使用urlencode对链接进行处理"""
    REDIRECT_URI = '%s/wx/wxauthor' % WxConfig.AppHost

    """
    应用授权作用域
    snsapi_base （不弹出授权页面，直接跳转，只能获取用户openid）
    snsapi_userinfo （弹出授权页面，可通过openid拿到昵称、性别、所在地。并且，即使在未关注的情况下，只要用户授权，也能获取其信息）
    """
    SCOPE = 'snsapi_base'
    # SCOPE = 'snsapi_userinfo'

    """通过code换取网页授权access_token"""
    get_access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?'

    """拉取用户信息"""
    get_userinfo_url = 'https://api.weixin.qq.com/sns/userinfo?'

    def get_code_url(self, state):
        """获取code的url"""
        dict = {'redirect_uri': self.REDIRECT_URI}
        redirect_uri = urllib.parse.urlencode(dict)
        author_get_code_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&%s&response_type=code&scope=%s&state=%s#wechat_redirect' % (WxConfig.AppID, redirect_uri, self.SCOPE, state)
        logger.debug('【微信网页授权】获取网页授权的code的url>>>>' + author_get_code_url)
        return author_get_code_url

    def get_auth_access_token(self, code):
        """通过code换取网页授权access_token"""
        url = self.get_access_token_url + 'appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (WxConfig.AppID, WxConfig.AppSecret, code)
        r = requests.get(url)
        logger.debug('【微信网页授权】通过code换取网页授权access_token的Response[' + str(r.status_code) + ']')
        if r.status_code == 200:
            res = r.text
            logger.debug('【微信网页授权】通过code换取网页授权access_token>>>>' + res)
            json_res = json.loads(res)
            if 'access_token' in json_res.keys():
                return json_res
            elif 'errcode' in json_res.keys():
                errcode = json_res['errcode']

class WxSignatureHandler(tornado.web.RequestHandler):
    """
    微信服务器签名验证, 消息回复

    check_signature: 校验signature是否正确
    """
    sys_order_reply = "欢迎你关注娱乐圈"
    pattern = re.compile(r'^\d{15}$')
    _token_cache = TokenCache()
    _media_cache = WxMediaCache()

    def data_received(self, chunk):
        pass

    def get(self):
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')
            result = self.check_signature(signature, timestamp, nonce)
            logger.debug('微信sign校验,signature='+signature+',&timestamp='+timestamp+'&nonce='+nonce+'&echostr='+echostr)
            if result:
                logger.debug('微信sign校验,返回echostr='+echostr)
                self.write(echostr)
            else:
                logger.error('微信sign校验,---校验失败')
        except Exception as e:
            logger.error('微信sign校验,---Exception' + str(e))
   
    @tornado.web.asynchronous
    def post(self):
        body = self.request.body
        logger.debug('微信消息回复中心】收到用户消息' + str(body.decode('utf-8')))
        data = ET.fromstring(body)
        ToUserName = data.find('ToUserName').text
        FromUserName = data.find('FromUserName').text
        self._from_name = FromUserName
        self._to_name = ToUserName
        MsgType = data.find('MsgType').text
        if MsgType == 'text' or MsgType == 'voice':
            '''文本消息 or 语音消息'''
            try:
                MsgId = data.find("MsgId").text
                if MsgType == 'text':
                    Content = data.find('Content').text  # 文本消息内容
                    results = self.pattern.findall(Content)
                    if len(results) > 0:
                        # 找到了符合订单ID的内容
                        order_id = results[0]
                        self._order_id = order_id
                        http_client = tornado.httpclient.AsyncHTTPClient()
                        token = self._token_cache.get_cache(self._token_cache.KEY_WD_ACCESS_TOKEN)
                        params = {"order_id": order_id}
                        public = {"access_token": token,"version": "1.0","format": "json","method": "vdian.order.get"}
                        url = r'https://api.vdian.com/api?param={"order_id":"%s"}&public={"method":"vdian.order.get","access_token":"%s","version":"1.0","format":"json"}' % (order_id,token)
                        http_client.fetch(url, callback=self.on_response)
                    else:
                        reply_content = "对不起，你可以再说一遍么?"
                        CreateTime = int(time.time())
                        out = self.reply_text(FromUserName, ToUserName, CreateTime, reply_content)
                        self.write(out)
                        self.finish()
            except Exception as e:
                self.finish()
                logger.error(str(e))

        elif MsgType == 'event':
            '''接收事件推送'''
            try:
                Event = data.find('Event').text
                if Event == 'subscribe':
                    # 关注事件
                    CreateTime = int(time.time())
                    reply_content = self.sys_order_reply
                    out = self.reply_text(FromUserName, ToUserName, CreateTime, reply_content)
                    self.write(out)
                    self.finish()
            except:
                self.finish()
                logger.error('错误')

    def reply_text(self, FromUserName, ToUserName, CreateTime, Content):
        textTpl = """<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[%s]]></MsgType> <Content><![CDATA[%s]]></Content></xml>"""
        out = textTpl % (FromUserName, ToUserName, CreateTime, "text", Content)
        return out

    def reply_image(self, FromUserName, ToUserName, CreateTime, Media_ID):
        textTpl = """<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[image]]></MsgType><Image><MediaId><![CDATA[%s]]></MediaId></Image></xml>"""
        out = textTpl % (FromUserName, ToUserName, CreateTime, Media_ID)
        return out

    def check_signature(self, signature, timestamp, nonce):
        """校验token是否正µ确"""
        token = 'zhangbinhui'
        L = [timestamp, nonce, token]
        L.sort()
        s = L[0] + L[1] + L[2]
        sha1 = hashlib.sha1(s.encode('utf-8')).hexdigest()
        logger.debug('sha1=' + sha1 + '&signature=' + signature)
        return sha1 == signature
    
    def on_response(self, response):
        CreateTime = int(time.time())
        if response.error:
            content = "对不起，输入的订单编号有误"
            out = self.reply_image(self._fddrom_name,self._to_name,CreateTime, content)
            self.write(out)
            self.finish()
        else:
            content = "OK"
            CreateTime = int(time.time())
            res_json = json.loads(response.body)
            name = res_json["result"]["buyer_info"]["name"]
            logger.info("name is" + name)
            exit_media_id = self._media_cache.get_cache(self._order_id)
            if exit_media_id:
                out = self.reply_image(self._from_name, self._to_name, CreateTime, exit_media_id)
                self.write(out)
                self.finish()
            else:
                path = os.getcwd()
                token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
                playload_image = {'access_token': token,'type': 'image'}
                logger.info("access_token is", token)
                ttfont = ImageFont.truetype(path + '/core/product/AppleGothic.ttf', 36)
                im = Image.open(path + "/core/static/demo.jpeg")  
                draw = ImageDraw.Draw(im)  
                draw.text((100,10),name, fill=(0,0,0),font=ttfont)
                newPath = path + "/core/product/" + self._order_id + '.jpeg'
                im.save(newPath)
                data = {'media': open(newPath, 'rb')}
                r = requests.post(url='http://file.api.weixin.qq.com/cgi-bin/media/upload',params=playload_image,files=data)
                image_json = json.loads(r.text)
                media_id = image_json["media_id"]
                # save media_id for this order id
                self._media_cache.set_cache(media_id, self._order_id)
                print(media_id)
                out = self.reply_image(self._from_name, self._to_name, CreateTime, media_id)
                self.write(out)
                logger.info(r.text)
        self.finish()
