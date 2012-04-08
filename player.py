import tornado.web

class HandshakeHandler(tornado.web.RequestHandler):
    def post(self):
        self.write('{}')
