import tornado.web

class WdHandler(tornado.web.RequestHandler):
    """
    微店handler处理类
    """

    return_data = {"status": "success"}

    def post(self):
        self.write(return_data)

    def post(self):
        self.write(return_data)