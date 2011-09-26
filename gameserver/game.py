import tornado.web

class GameHandler(tornado.web.RequestHandler):
    def get(self, game_name):
        self.write('cool %s' % game_name)

class CreateGameHandler(tornado.web.RequestHandler):
    def post(self):
        import pdb; pdb.set_trace()
        self.write('you wrote')


