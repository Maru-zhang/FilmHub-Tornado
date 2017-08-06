import requests
import json
from core.server.wxconfig import WxConfig
from core.cache.tokencache import TokenCache
from core.logger_helper import logger

class WxMenuServer(object):
    """
    微信自定义菜单

    create_menu                     自定义菜单创建接口
    get_menu                        自定义菜单查询接口
    delete_menu                     自定义菜单删除接口
    create_menu_data                创建菜单数据
    """

    _token_cache = TokenCache()  # 微信token缓存

    def create_menu(self):
        """自定义菜单创建接口"""
        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
        if access_token:
            url = WxConfig.menu_create_url + access_token
            data = self.create_menu_data()
            r = requests.post(url, data.encode('utf-8'))
            logger.debug('【微信自定义菜单】自定义菜单创建接口Response[' + str(r.status_code) + ']')
            if r.status_code == 200:
                res = r.text
                logger.debug('【微信自定义菜单】自定义菜单创建接口' + res)
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode
        else:
            logger.error('【微信自定义菜单】自定义菜单创建接口获取不到access_token')

    def get_menu(self):
        """自定义菜单查询接口"""
        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
        if access_token:
            url = WxConfig.menu_get_url + access_token
            r = requests.get(url)
            logger.debug('【微信自定义菜单】自定义菜单查询接口Response[' + str(r.status_code) + ']')
            if r.status_code == 200:
                res = r.text
                logger.debug('【微信自定义菜单】自定义菜单查询接口' + res)
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode
        else:
            logger.error('【微信自定义菜单】自定义菜单查询接口获取不到access_token')

    def delete_menu(self):
        """自定义菜单删除接口"""
        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
        if access_token:
            url = WxConfig.menu_delete_url + access_token
            r = requests.get(url)
            logger.debug('【微信自定义菜单】自定义菜单删除接口Response[' + str(r.status_code) + ']')
            if r.status_code == 200:
                res = r.text
                logger.debug('【微信自定义菜单】自定义菜单删除接口' + res)
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode
        else:
            logger.error('【微信自定义菜单】自定义菜单删除接口获取不到access_token')

    def create_menu_data(self):
        """创建菜单数据"""
        menu_data = {"button": [
            {
                "name": "精选内容",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "精选文章",
                        "url": "http://mp.weixin.qq.com/mp/homepage?__biz=MjM5Nzc5MDkwMQ==&hid=3&sn=70ce35abda6a8236f90a3a36e964dc2d"
                    },
                    {
                        "type": "view",
                        "name": "影评剧评",
                        "url": "http://mp.weixin.qq.com/mp/homepage?__biz=MjM5Nzc5MDkwMQ==&hid=4&sn=aeaee3a48324880d0c5e6ea335d5b9cc"
                    },
                    {
                        "type": "view",
                        "name": "明星专访",
                        "url": "http://mp.weixin.qq.com/mp/homepage?__biz=MjM5Nzc5MDkwMQ==&hid=5&sn=24c252b77d42b6d93bd021bbc4eaf67f"
                    }
                ]
            },
            {
                "type": "view",
                "name": "李易峰专刊",
                "url": "https://weidian.com/s/209793342?ifr=shopdetail&wfr=c"
            },
            {
                "name": "联系我们",
                "sub_button": [
                    {
                        "type": "media_id",
                        "name": "加入我们",
                        "media_id": "b-Ij3Ifb-J_iT6cv09d5mOV7UvvCeEZ9fQqxIEqAXW0"
                    },
                    {
                        "type": "click",
                        "name": "欢迎转载",
                        "key": "reprint"
                    },
                    {
                        "type": "media_id",
                        "name": "商务合作",
                        "media_id": "b-Ij3Ifb-J_iT6cv09d5mKHcKOLuXzDAqMAT9ns8XWU"
                    }
                ]
            }
            ]}
        MENU_DATA = json.dumps(menu_data, ensure_ascii=False)
        logger.debug('【微信自定义菜单】创建菜单数据MENU_DATA[' + str(MENU_DATA) + ']')
        return MENU_DATA

if __name__ == '__main__':
    wx_menu_server = WxMenuServer()
    '''创建菜单数据'''
    wx_menu_server.create_menu_data()
    '''自定义菜单创建接口'''
    wx_menu_server.create_menu()
    '''自定义菜单查询接口'''
    # wx_menu_server.get_menu()
    '''自定义菜单删除接口'''
    # wx_menu_server.delete_menu()
