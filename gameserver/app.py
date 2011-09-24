import sqlite3

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define('port', default=8888, help='do stuff', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', RootHandler),
            (r'/games/([^/]+)/', GameHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world')

class GameHandler(tornado.web.RequestHandler):
    def get(self, game_name):
        self.write('cool %s' % game_name)

def setup_db():
    con = sqlite3.connect(':memory:')
    cur = con.cursor()
    cur.executescript("""
        create table users(
            firstname,
            lastname);
    """)

def main():
    setup_db()

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
