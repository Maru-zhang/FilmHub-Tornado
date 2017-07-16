from core.server.wxauthorize import WxSignatureHandler
from core.server.test import HomePageHandler
import tornado.web


'''web解析规则'''

urlpatterns = [
    (r'/wxsignature', WxSignatureHandler),
    (r'/home', HomePageHandler)
   ]
