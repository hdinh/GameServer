"""Tienlen game logic."""

import random
from tienlen.misc import TienlenException
import tienlen.handvalue

#pylint: disable=C0301,R0902,R0903

def deck():
    """Returns a representation of tienlen deck."""
    result = range(52)
    random.shuffle(result)
    return result

class GameActionResult():
    """Represents a tienlen action result."""
    #pylint: disable=R0913
    def __init__(self,
                 message='',
                 valid=False,
                 next_to_act_seat=-1,
                 in_control_seat=-1,
                 takes_control=False):
        """Constructor for game result."""
        self.message = message
        self.valid = valid
        self.next_to_act_seat = next_to_act_seat
        self.in_control_seat = in_control_seat
        self.takes_control = takes_control

class Game():
    """Represents Tienlen Game."""
    def __init__(self, players, game_id=-1):
        """Default constrcutor."""
        num = len([p for p in players if p != None])
        if num < 2:
            raise TienlenException('not enough players')
        if num > 4:
            raise TienlenException('too many players')

        self._observers = []

        self.player_cards = {}
        self.players = players
        self.game_id = game_id
        self.next_to_act_seat = -1
        self.in_control_seat = -1
        self.started = False
        self.completed = False
        self.common_cards = []
        self.seats_in_round = []

    def start(self):
        """Starts tienlen game."""
        game_deck = deck()
        for i in range(len(self.players)):
            if self.players[i]:
                self.player_cards[i] = [game_deck.pop() for _ in range(13)]
                self.player_cards[i].sort()
                self.players[i].on_cards(list(self.player_cards[i]))

        self._notify_event(method='game_started', args=None)
        self._notify_event(method='cards_dealt', args=None)

        self._process_new_round()
        self.next_to_act_seat = self._get_next_to_act_seat()
        self.in_control_seat = self.next_to_act_seat
        self.started = True

    def subscribe(self, subscriber):
        """Subscribes to event. Observer pattern."""
        self._observers.append(subscriber)

    def _notify_event(self, method, args):
        """Calls observers with event. Observer pattern."""
        for observer in self._observers:
            observer(method, args)

    def try_action(self, seat, cards):
        """Validates and process action.
        Assumes that specified action is well-formed.
        """
        test = self._test_action(seat, cards)
        if (test.valid == True):
            self._process_action(seat, cards, test.takes_control)

            # Attach useful properties to the action result
            # May be useful? But we could do the same thing just on the client-side
            test.next_to_act_seat = self.next_to_act_seat
            test.in_control_seat = self.in_control_seat

        return test

    def _test_action(self, seat, cards):
        """Tests if action is valid for the current game state."""
        # Verify it is the player's turn
        if seat != self.next_to_act_seat:
            return GameActionResult(valid=False, message='not player\'s turn')

        # Check if player passed
        if len(cards) == 0:
            return GameActionResult(valid=True,
                                    takes_control=False,
                                    message='passed')

        # Verify cards are all the user's
        for i in range(len(cards)):
            if cards[i] not in self.player_cards[self.next_to_act_seat]:
                return GameActionResult(valid=False,
                                        message='cards not in player\'s hand')

        # If hand is the same type and better than common, it is a valid action
        hand_value = tienlen.handvalue.handvalue(tienlen.core.handmask(cards))
        common_value = tienlen.handvalue.handvalue(tienlen.core.handmask(self.common_cards))

        if not tienlen.handvalue.valid(hand_value):
            return GameActionResult(valid=False, message='cards do not make a valid hand')
        if tienlen.handvalue.isbetter(hand_value, common_value):
            return GameActionResult(valid=True, takes_control=True, message='ok')
        return GameActionResult(valid=False,
                                message='your cards are not better than the current hand')

    def _get_next_to_act_seat(self):
        """Returns next seat to act."""
        candidate = self.next_to_act_seat
        player_count = len(self.players)
        for _ in range(4):
            candidate = (candidate + 1) % 4
            if candidate < player_count and self.players[candidate]:
                if candidate in self.seats_in_round:
                    return candidate
        return 'next player not found'

    def _process_new_round(self):
        """Processes new round. Enables all players who have finished
        hand to be eligible to act again.
        """
        self.seats_in_round = []
        for i in range(len(self.players)):
            if self.players[i]:
                self.seats_in_round.append(i)

    def _process_action(self, seat, cards, takes_control):
        """Updates the state of the game including possibly ending the game."""
        if takes_control:
            self.in_control_seat = self.next_to_act_seat
            self.common_cards = cards
            for card in cards:
                self.player_cards[seat].remove(card)
        else:
            # If player doesn't take control, he is not qualified to act anymore
            self.seats_in_round.remove(seat)

        self.next_to_act_seat = self._get_next_to_act_seat()

        # If control returns back to player, wipe out common cards
        if self.next_to_act_seat == self.in_control_seat:
            self.common_cards = []

        # Reset the round if there is only one player or if common_cards is empty
        if len(self.seats_in_round) == 1 or len(self.common_cards) == 0:
            self._process_new_round()

        # Raise events
        # this.events.push(action)
        # this.emitter.emit(GAME_EVENT_ID, action)

        # Check if the game is in a completed state
        #if self.completed:
        #    pass

