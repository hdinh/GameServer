#~/usr/bin/env python

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import game
import player
import table

define('port', default=8888, type=int)

registry = None

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', RootHandler),
            (r'/api/games/([^/]+)/', game.GameHandler),
            (r'/api/games', game.GameHandler),
            (r'/api/tables/([^/]+)/', table.TableHandler),
            (r'/api/tables/', table.CreateTableHandler),
            (r'/api/player/handshake', player.HandshakeHandler),
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), 'static')
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/static/index.html')

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print('listening on port %i' % options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
