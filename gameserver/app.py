import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import game
import table

define('port', default=8888, help='do stuff', type=int)

registry = None

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', RootHandler),
            (r'/games/([^/]+)/', game.GameHandler),
            (r'/games', game.CreateGameHandler),
            (r'/tables/([^/]+)/', table.TableHandler),
            (r'/tables/', table.CreateTableHandler),
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), 'static')
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write('Hello, world')
        self.redirect('/static/index.html')

def main():
    import pdb; pdb.set_trace()
    import registry
    r = registry.AppRegistry()

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

