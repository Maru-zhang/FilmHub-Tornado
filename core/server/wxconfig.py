class WxConfig(object):
    """
    微信开发--基础配置

    """
    AppID = 'wxa78dfd0e461d4211'  # AppID(应用ID)
    AppSecret = '594e2e6f4de7fd19bd9ca1030aee5f10'  # AppSecret(应用密钥)

    '''获取access_token'''
    config_get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (AppID, AppSecret)
