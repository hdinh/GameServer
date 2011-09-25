"""Unit tests for game.py"""

import unittest
import mock
import tienlen.game
from tienlen.misc import TienlenException

#pylint: disable=C0103,C0111,R0904

class GameTests(unittest.TestCase):

    def testDeckShouldHave52Cards(self):
        deck = tienlen.game.deck()
        self.assertEqual(52, len(deck))

    def testShuffledDeckShouldBeValid(self):
        passed = True
        deck = tienlen.game.deck()
        for i in range(52):
            passed = passed and deck[i] < 52
        self.assertTrue(passed)

    def testShuffledDeckShouldBeUnique(self):
        deck = tienlen.game.deck()
        passed = True
        for i in range(51):
            for j in range(i+1, 52):
                passed = passed and deck[i] != deck[j]
        self.assertTrue(passed)

    def testDeckShouldHaveOneOfEach(self):
        deck = tienlen.game.deck()
        for i in range(51):
            self.assertTrue(i in deck)

    def testDecksShouldBeUnique(self):
        deck1 = tienlen.game.deck()
        deck2 = tienlen.game.deck()
        self.assertNotEqual(deck1, deck2)

    #def testGameConstructorThrowsExceptionIfInfoIsNull(self):
    #    Should be next...
    #    self.assertRaises(Exception, tienlen.game.Game())

    #def testGameConstructorThrowsExceptionIfPlayersIsNull(self):
    #    Should be next...
    #    self.assertRaises(Exception, tienlen.game.Game(players=None))

    def testShouldSetUniqueGameId(self):
        plist = [mock.Mock(), mock.Mock(), mock.Mock()]
        game = tienlen.game.Game(players=plist)
        self.assertTrue(isinstance(game.game_id, int))

    def testShouldSeatPlayers(self):
        plist = [mock.Mock(), mock.Mock()]
        game = tienlen.game.Game(players=plist)
        self.assertTrue(2, len(game.players))

    def testShouldThrowIfNotEnoughPlayers(self):
        plist = [None, None, None, mock.Mock()]
        self.assertRaises(TienlenException, tienlen.game.Game, players=plist)

    def testShouldThrowIfPlayersArrayOverFound(self):
        plist = [mock.Mock() for _ in range(5)]
        self.assertRaises(TienlenException, tienlen.game.Game, players=plist)

    def testStartPlayersShouldBeDealtAtStartTime(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        self.assertEqual(1, player1.on_cards.call_count)
        self.assertEqual(1, player2.on_cards.call_count)

    def testPlayersShouldHaveThirteenCardsAtStartup(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        cardcount = len(player1.on_cards.call_args[0][0])
        self.assertEqual(13, cardcount)

    def testPlayersCardsShouldBeSorted(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        cards = player1.on_cards.call_args[0][0]
        for i in range(1, len(cards) - 1):
            carda = cards[i]
            cardb = cards[i-1]
            if carda <= cardb:
                self.fail()

    def testPlayersShouldAllHaveUniqueCards(self):
        plist = [mock.MagicMock(),
                 mock.MagicMock(),
                 mock.MagicMock(),
                 mock.MagicMock()]
        game = tienlen.game.Game(players=plist)
        game.start()
        all_cards = []
        for player in plist:
            for card in player.on_cards.call_args[0][0]:
                if card not in all_cards:
                    all_cards.append(card)
        self.assertEqual(52, len(all_cards))

    def testConstructorShouldSetProperties(self):
        plist = [mock.Mock(), mock.Mock()]
        game = tienlen.game.Game(players=plist)
        self.assertEqual(False, game.started)
        self.assertEqual(False, game.completed)

    def testStartGameShouldSetProperties(self):
        plist = [mock.Mock(), mock.Mock()]
        game = tienlen.game.Game(players=plist)
        game.start()
        self.assertEqual(True, game.started)
        self.assertEqual(False, game.completed)

    def testShouldEmitEventsOnGameStart(self):
        observer = mock.Mock()
        plist = [mock.Mock(), mock.Mock()]
        game = tienlen.game.Game(players=plist)
        game.subscribe(observer)
        game.start()
        methods = [e[0][0] for e in observer.call_args_list]
        self.assertTrue('cards_dealt' in methods)
        self.assertTrue('game_started' in methods)

    def testCardDealingShouldHandleEmptySeats(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        self.assertEqual(13, len(player1.on_cards.call_args[0][0]))
        self.assertEqual(13, len(player2.on_cards.call_args[0][0]))

    def testNextToActShouldBeFirstSeatedPlayer(self):
        game = tienlen.game.Game(players=[None, None, mock.Mock(), mock.Mock()])
        game.start()
        self.assertEqual(2, game.next_to_act_seat)

    def testTryActionShouldContainMessage(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        result = game.try_action(seat=0,
                                 cards=[player1.on_cards.call_args[0][0][0]])
        self.assertTrue(result.message != None)

    def testFirstSeatInNewGameShouldBeFirstToAct(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        result = game.try_action(seat=0,
                                 cards=[player1.on_cards.call_args[0][0][0]])
        self.assertEqual(1, result.next_to_act_seat)
        self.assertEqual(0, result.in_control_seat)

    def testSecondSeatInNewGameShouldNotBeFirstToAct(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        result = game.try_action(seat=0,
                                 cards=[player1.on_cards.call_args[0][0][0]])
        self.assertTrue(result.valid)

    def testActionShouldBeInvalidifCardsNotInPlayersHand(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        result = game.try_action(seat=0,
                                 cards=[player2.on_cards.call_args[0][0][0]])
        self.assertFalse(result.valid)

    def testActionShouldBeInvalidIfCardsDontMakeHand(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        thecards = [player2.on_cards.call_args[0][0][0],
                    player2.on_cards.call_args[0][0][8]]
        result = game.try_action(seat=0, cards=thecards)
        self.assertFalse(result.valid)

    def testNextToActShouldIncrementAfterValidAction(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        player3 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2, None, player3])
        game.start()
        self.assertEqual(0, game.next_to_act_seat)
        self.assertEqual(0, game.in_control_seat)
        result = game.try_action(seat=0,
                                 cards=[player1.on_cards.call_args[0][0][0]])
        self.assertEqual(1, game.next_to_act_seat)
        self.assertEqual(0, game.in_control_seat)
        self.assertEqual(1, result.next_to_act_seat)
        self.assertEqual(0, result.in_control_seat)
        result = game.try_action(seat=1,
                                 cards=[player2.on_cards.call_args[0][0][7]])
        self.assertEqual(3, game.next_to_act_seat)
        self.assertEqual(1, game.in_control_seat)
        self.assertEqual(3, result.next_to_act_seat)
        self.assertEqual(1, result.in_control_seat)
        result = game.try_action(seat=3,
                                 cards=[player3.on_cards.call_args[0][0][12]])
        self.assertEqual(0, game.next_to_act_seat)
        self.assertEqual(3, game.in_control_seat)
        self.assertEqual(0, result.next_to_act_seat)
        self.assertEqual(3, result.in_control_seat)

    def testPlayerNoCardsShouldsShouldPassPlayersTurn(self):
        plist = [mock.MagicMock(),
                 mock.MagicMock(),
                 None,
                 mock.MagicMock()]
        game = tienlen.game.Game(players=plist)
        game.start()
        self.assertEqual(0, game.next_to_act_seat)
        game.try_action(seat=0, cards=[plist[0].on_cards.call_args[0][0][0]])
        self.assertEqual(1, game.next_to_act_seat)
        self.assertEqual(0, game.in_control_seat)
        game.try_action(seat=1, cards=[])
        self.assertEqual(3, game.next_to_act_seat)
        self.assertEqual(0, game.in_control_seat)

    def testAfterEveryActionCommonCardsShouldUpdate(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        game.try_action(seat=0, cards=[player1.on_cards.call_args[0][0][0]])
        self.assertEqual([player1.on_cards.call_args[0][0][0]],
                         game.common_cards)
        game.try_action(seat=1, cards=[player2.on_cards.call_args[0][0][12]])
        self.assertEqual([player2.on_cards.call_args[0][0][12]],
                         game.common_cards)

    def testAfterEveryActionCardsShouldBeRemovedFromPlayer(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        game.try_action(seat=0, cards=[player1.on_cards.call_args[0][0][0]])
        self.assertEqual(12, len(game.player_cards[0]))
        self.assertFalse(
            player1.on_cards.call_args[0][0][0] in game.player_cards[0])
        game.try_action(seat=1, cards=[player2.on_cards.call_args[0][0][7]])
        self.assertEqual(12, len(game.player_cards[1]))
        self.assertFalse(
            player2.on_cards.call_args[0][0][7] in game.player_cards[1])
        self.assertEqual(0, game.next_to_act_seat)
        game.try_action(seat=0, cards=[player1.on_cards.call_args[0][0][11]])
        self.assertEqual(11, len(game.player_cards[0]))
        self.assertFalse(
            player1.on_cards.call_args[0][0][11] in game.player_cards[0])

    def testAfterEveryPassOriginalPlayerShoudlBeInControL(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        game.try_action(seat=0, cards=[player1.on_cards.call_args[0][0][0]])
        game.try_action(seat=1, cards=[])
        self.assertEqual(0, game.next_to_act_seat)
        self.assertEqual(0, game.in_control_seat)
        self.assertEqual(0, len(game.common_cards))

    def testResultOfTryActionShouldContainNextToActProperties(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[player1, player2])
        game.start()
        result1 = game.try_action(seat=0,
                                  cards=[player1.on_cards.call_args[0][0][0]])
        self.assertEqual(1, result1.next_to_act_seat)
        self.assertEqual(0, result1.in_control_seat)
        result2 = game.try_action(seat=1,
                                  cards=[player2.on_cards.call_args[0][0][6]])
        self.assertEqual(0, result2.next_to_act_seat)
        self.assertEqual(1, result2.in_control_seat)
        result3 = game.try_action(seat=0,
                                  cards=[player1.on_cards.call_args[0][0][11]])
        self.assertEqual(1, result3.next_to_act_seat)
        self.assertEqual(0, result3.in_control_seat)

    def testInRoundShouldBeAllPlayersInRoundAtStartup(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game = tienlen.game.Game(players=[None, player1, player2])
        game.start()
        self.assertTrue(0 not in game.seats_in_round)
        self.assertTrue(1 in game.seats_in_round)
        self.assertTrue(2 in game.seats_in_round)
        self.assertTrue(3 not in game.seats_in_round)

    def testInRoundShouldRemovePlayerThatPassed(self):
        plist = [mock.MagicMock(),
                 mock.MagicMock(),
                 mock.MagicMock()]
        game = tienlen.game.Game(players=plist)
        game.start()

        # P1 plays
        game.try_action(seat=0, cards=[plist[0].on_cards.call_args[0][0][0]])
        self.assertTrue(0 in game.seats_in_round)
        self.assertTrue(1 in game.seats_in_round)
        self.assertTrue(2 in game.seats_in_round)

        # P2 passes
        game.try_action(seat=1, cards=[])
        self.assertTrue(0 in game.seats_in_round)
        self.assertTrue(1 not in game.seats_in_round)
        self.assertTrue(2 in game.seats_in_round)

        # P3 plays
        game.try_action(seat=2, cards=[plist[2].on_cards.call_args[0][0][5]])
        self.assertTrue(0 in game.seats_in_round)
        self.assertTrue(1 not in game.seats_in_round)
        self.assertTrue(2 in game.seats_in_round)

        # P1 plays (should stkip player #1 and go to player #2)
        game.try_action(seat=0, cards=[plist[0].on_cards.call_args[0][0][9]])
        self.assertTrue(0 in game.seats_in_round)
        self.assertTrue(1 not in game.seats_in_round)
        self.assertTrue(2 in game.seats_in_round)

        # P3 plays (round should be reset)
        game.try_action(seat=2, cards=[])
        self.assertTrue(0 in game.seats_in_round)
        self.assertTrue(1 in game.seats_in_round)
        self.assertTrue(2 in game.seats_in_round)

    def testInRoundShouldNotEliminatePlayerWhenEverybodyIsQualified(self):
        plist = [mock.MagicMock(),
                 mock.MagicMock(),
                 mock.MagicMock()]
        game = tienlen.game.Game(players=plist)
        game.start()
        game.try_action(seat=0, cards=[])
        self.assertTrue(0 in game.seats_in_round)

    def testInRoundShouldSkipIntermediatePlayerWhenNewRoundIsProcessed(self):
        plist = [mock.MagicMock(),
                 None,
                 mock.MagicMock(),
                 mock.MagicMock()]
        game = tienlen.game.Game(players=plist)
        game.start()
        game.try_action(seat=0, cards=[])
        game.try_action(seat=2, cards=[plist[2].on_cards.call_args[0][0][0]])
        game.try_action(seat=3, cards=[])
        self.assertTrue(3 not in game.seats_in_round)

    def testTryActionNotPlayersTurnShouldReturnFalse(self):
        plist = [mock.MagicMock(),
                 mock.MagicMock()]
        game = tienlen.game.Game(players=plist)
        game.start()
        result = game.try_action(seat=1,
                                 cards=[plist[1].on_cards.call_args[0][0][0]])
        self.assertFalse(result.valid)

    def testTryActionNotValidHandTurnShouldReturnFalse(self):
        plist = [mock.MagicMock(),
                 mock.MagicMock()]
        game = tienlen.game.Game(players=plist)
        game.start()
        result = game.try_action(seat=0,
                                 cards=[plist[0].on_cards.call_args[0][0][0],
                                        plist[0].on_cards.call_args[0][0][8]])
        self.assertFalse(result.valid)

    def testTryActionAreNotBetterThanCommonTurnShouldReturnFalse(self):
        plist = [mock.MagicMock(),
                 mock.MagicMock()]
        game = tienlen.game.Game(players=plist)
        game.start()
        game.try_action(seat=0,
                        cards=[plist[0].on_cards.call_args[0][0][12]])
        result = game.try_action(seat=1,
                                 cards=[plist[1].on_cards.call_args[0][0][0]])
        self.assertFalse(result.valid)

if __name__ == '__main__':
    unittest.main()

