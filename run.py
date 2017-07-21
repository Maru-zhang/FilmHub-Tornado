import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from core.url import urlpatterns
from core.server.wxschedule import WxSchedule
from core.server.wxmenu import WxMenuServer

define('port', default=80, help='run on the given port', type=int)

class Application(tornado.web.Application):
    
    def __init__(self):
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "core/template"),
            static_path=os.path.join(os.path.dirname(__file__), "core/static"),
            debug=True
        )
        super(Application, self).__init__(urlpatterns, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    # 执行定时任务
    wx_schedule = WxSchedule()
    wx_schedule.excute()
    tornado.ioloop.IOLoop.current().start()
    # 创建菜单
    menu = WxMenuServer()

if __name__ == '__main__':
    main()
