class WxConfig(object):
    """
    微信开发--基础配置
    """
    AppID = 'wxa78dfd0e461d4211'  # AppID(应用ID)
    AppSecret = '594e2e6f4de7fd19bd9ca1030aee5f10'  # AppSecret(应用密钥)
    AppCustomToken = 'circlemagazine'
    WdAppID = '683523' # 微店应用ID
    WdAppSecret = '083a282e921b0f9775d5e0222d3fc3e7' # 微店应用秘钥
    """微信网页开发域名"""
    AppHost = 'http://maru-zhang.cn'

    COMMON_COPYWRITE = '''Hey,
1.看往期精彩内容请点击菜单栏
2.请输入正确的订单号，获取分享图
3.订单号无法有效使用，请联系淘宝/微店客服'''
    ATTENTION_INIT_COPYWRITE_1 = u'''《影视圈》杂志创刊于1994年，
欢迎2017年关注！
~♥~'''
    ATTENTION_INIT_COPYWRITE_2 = u'''如果你是🐝
请输入暗号（订单号），
自动生成惊喜。

获取暗号→请请点击↓菜单栏“李易峰专刊”
下单后输入暗号（订单号），
生成不同款惊喜。'''
    REPRINT_COPYWRITE = u'''欢迎转载
转载请添加微信415716805
并请将你想要转载的文章以及你的公众号id发送给我们，我们会第一时间为你开通白名单。'''
    HTTP_RESPONSE_ERROR_COPYWRITE = u"服务器响应失败，请稍后再试~"
    PART_IN_SUCCESS_COPYWRITE = u'''订单号验证成功，
恭喜你获得专属分享图，
快晒一下吧~'''
    PART_IN_FAILURE_COPYWRITE = COMMON_COPYWRITE
    PART_IN_GUESSGANME_WAITTING = u"快如闪电，机智如你，图片收到，正在验证准确率！"
    
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
    '''客服发送消息接口'''
    server_message_send_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='

    '''微信公众号菜单映射数据'''
    """重定向后会带上state参数，开发者可以填写a-zA-Z0-9的参数值，最多128字节"""
    wx_menu_state_map = {
        'menuIndex0': '%s/page/index' % AppHost,  # 测试菜单1
    }
