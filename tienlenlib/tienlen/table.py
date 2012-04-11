"""Tienlen table."""

import datetime
import tienlen.game

class DefaultTableIdProvider():
    def __init__(self):
        self.current_id = 0

    def next_game_id(self):
        self.current_id += 1
        return self.current_id

class Table():
    """Represents tienlen table."""
    def __init__(self, name, manager=None):
        """Constructor for table."""
        self.name = name
        self.seats = [None, None, None, None]
        self.events = []
        self.game = None
        self.date_created = datetime.datetime.now()
        self.started = False

        if manager == None:
            self.manager = DefaultTableIdProvider()
        else:
            self.manager = manager

    def start_game(self):
        """Starts tienlen game for table."""
        if self.game:
            if self.started:
                return (False, 'game is already started')

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

