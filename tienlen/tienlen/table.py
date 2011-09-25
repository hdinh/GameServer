"""Tienlen table."""

import datetime
import tienlen.game

class Table():
    """Represents tienlen table."""
    def __init__(self, name, manager):
        """Constructor for table."""
        self.name = name
        self.manager = manager
        self.seats = [None, None, None, None]
        self.events = []
        self.game = None
        self.date_created = datetime.datetime.now()
        self.started = False

    def start_game(self):
        """Starts tienlen game for table."""
        if self.game:
            #if self.game.completed:
            #   return (False, 'game is completed')
            if self.started:
                return (False, 'game is already started')

        #game = self.manager.table_create(callback)
        #return game
        game_id = -1
        if self.manager:
            game_id = self.manager.next_game_id()
        self.game = tienlen.game.Game(self.seats, game_id=game_id)

    def sit_player(self, seat, player):
        """Sits specified table in seat."""
        if self.seats[seat]:
            return (False, 'seat %s is already taken' % seat)
        elif not player.name:
            return (False, 'username must be provided')
        else:
            self.seats[seat] = player
            #self.events.app
        #self.seats

