class WxConfig(object):
    """
    微信开发--基础配置
    """
    AppID = 'wxa78dfd0e461d4211'  # AppID(应用ID)
    AppSecret = '594e2e6f4de7fd19bd9ca1030aee5f10'  # AppSecret(应用密钥)
    AppCustomToken = 'zhangbinhui'
    WdAppID = '683523' # 微店应用ID
    WdAppSecret = '083a282e921b0f9775d5e0222d3fc3e7' # 微店应用秘钥
    """微信网页开发域名"""
    AppHost = 'http://maru-zhang.cn'

    PART_IN_SUCCESS_COPYWRITE = "你已成功参与活动，下面是你专属的应援图。快去分享吧~，集齐4张不同的李易峰专属应援图可兑换李易峰签名海报1张。"
    PART_IN_FAILURE_COPYWRITE = "请输入正确的订单号，李易峰专刊正热卖种，想了解活动详情/点击这里/。如有疑问请咨询小圈，电话/微信：xxxxxxx"
    
    '''获取微信access_token'''
    config_get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID, AppSecret)
    '''获取微店access_token'''
    config_wd_get_access_token_url = 'https://oauth.open.weidian.com/token?grant_type=client_credential&appkey=%s&secret=%s' % (WdAppID, WdAppSecret)
    '''自定义菜单创建接口'''
    menu_create_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='

    '''自定义菜单查询接口'''
    menu_get_url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token='

    '''自定义菜单删除接口'''
    menu_delete_url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token='

    '''微信公众号菜单映射数据'''
    """重定向后会带上state参数，开发者可以填写a-zA-Z0-9的参数值，最多128字节"""
    wx_menu_state_map = {
        'menuIndex0': '%s/page/index' % AppHost,  # 测试菜单1
    }
