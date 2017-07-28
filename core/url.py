from core.server.wxauthorize import WxSignatureHandler
from core.server.wd_handler import WdHandler
import tornado.web


'''web解析规则'''

urlpatterns = [
    (r'/wxsignature', WxSignatureHandler),
    (r'/wxsignature', WdHandler)
   ]
