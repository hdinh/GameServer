"""Unit tests for table.py"""

import unittest
import mock
import tienlen.table

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

