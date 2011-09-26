"""Unit tests for table.py"""

import unittest
import mock
import tienlen.table

#pylint: disable=C0103,C0111,R0904

class TableTests(unittest.TestCase): 

    def testConstructorShouldSetProperties(self):
        gameManager = mock.Mock()
        table = tienlen.table.Table(name='ttt',
                                    manager=gameManager)
        self.assertEqual(0, len(table.events))
        self.assertEqual(4, len(table.seats))
        self.assertEqual(None, table.seats[0])
        self.assertEqual(None, table.seats[1])
        self.assertEqual(None, table.seats[2])
        self.assertEqual(None, table.seats[3])

    def testStartValidGameShouldBeValid(self):
        gameManager = mock.Mock()
        gameManager.next_game_id.return_value = 123
        table = tienlen.table.Table(name='table0A1',
                                    manager=gameManager)
        p1 = mock.Mock()
        p1.name = 'A'
        p2 = mock.Mock()
        p2.name = 'B'

        table.sit_player(0, p1)
        table.sit_player(3, p2)
        table.start_game()
        self.assertEqual(table.game.game_id, 123)
        self.assertEqual(1, gameManager.next_game_id.call_count)

    def testManagerShouldBeAbleToBeNone(self):
        table = tienlen.table.Table(name='table1',
                                    manager=None)

        p1 = mock.Mock()
        p1.name = 'A'
        p2 = mock.Mock()
        p2.name = 'B'

        table.sit_player(0, p1)
        table.sit_player(3, p2)
        table.start_game()
        self.assertTrue(isinstance(table.game.game_id, int))
 
