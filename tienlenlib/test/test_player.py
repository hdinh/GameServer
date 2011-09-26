"""Unit tests for player.py"""

import unittest
import tienlen.player

#pylint: disable=C0103,C0111,R0904

class PlayerTests(unittest.TestCase):

    def testShouldSetName(self):
        player = tienlen.player.Player('PlayerName')
        self.assertEqual('PlayerName', player.name)
