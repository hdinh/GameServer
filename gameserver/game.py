import tornado.web
import random

import json
import sys
sys.path.append('../tienlenlib')
import tienlen

class GameHandler(tornado.web.RequestHandler):
    tables = []
    current_table_id = 0

    def get(self, game_name):
        self.write('cool %s' % game_name)

    def post(self):
        state = json.loads(self.request.arguments['state'][0])

        p = int(state['player']['number'])
        player = tienlen.player.Player('Player' + str(p))
        player.number = p

        method = self.request.arguments['method'][0]
        if method == 'host':
            table = self._create_table(name=self.request.arguments['table_name'])
        elif method == 'join':
            table = self._join_table(name=self.request.arguments['table_name'])
            if table == None:
                self.write(tornado.escape.json_encode({ "error": "table does not exist" }))
                return
        elif method == 'play_now':
            table = self._get_best_table()
        else:
            self.write(tornado.escape.json_encode({ "error": "invalid method" }))
            return

        for seat in range(len(table.seats)):
            if table.seats[seat] == None:
                table.sit_player(seat, player)
                break

        seats = []
        for seat in table.seats:
            if seat:
                s = { "name" : seat.name, "number" : seat.number }
            else:
                s = {}
            seats.append(s)
        table_copy = { \
            "name" : table.name, \
            "seats" : seats \
        }
        self.write(tornado.escape.json_encode({ "table": table_copy }))

    def _get_best_table(self):
        tables_with_empty_seats = self._get_empty_seat_tables()
        if len(tables_with_empty_seats) == 0:
            return self._create_table()
        else:
            r = random.randint(0, len(tables_with_empty_seats) - 1)
            return tables_with_empty_seats[r]

    def _get_empty_seat_tables(self):
        tables_with_empty_seats = []
        for table in GameHandler.tables:
            if table.seats == None:
                tables_with_empty_seats.append(table)
        return tables_with_empty_seats

    def _create_table(self, name=None):
        if name == None:
            GameHandler.current_table_id += 1
            name = 'Table-' + GameHandler.current_table_id

        table = tienlen.table.Table(name)
        GameHandler.tables.append(table)
        return table

    def _join_table(self, name):
        for table in GameHandler.tables:
            if table.name == name:
                return table
        return None
