import tornado.web
import tornado.escape

class HandshakeHandler(tornado.web.RequestHandler):
    players = []
    next_player_id = 0

    def post(self):
        HandshakeHandler.next_player_id += 1
        self.write(tornado.escape.json_encode({'number': HandshakeHandler.next_player_id}))
