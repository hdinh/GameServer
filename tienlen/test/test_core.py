"""Unit tests for core.py"""

import unittest
import tienlen.core
from tienlen.misc import TienlenException

#pylint: disable=C0103,C0111,R0904

class CoreTests(unittest.TestCase):

    def testCardMask8s(self):
        mask = tienlen.core.cardmask('8d')
        self.assertEqual(8, tienlen.core.cardrank(mask))
        self.assertEqual(2, tienlen.core.cardsuit(mask))
        self.assertEqual(22, tienlen.core.cardindex(mask))

    def testCardMask3s(self):
        mask = tienlen.core.cardmask('3s')
        self.assertEqual(3, tienlen.core.cardrank(mask))
        self.assertEqual(0, tienlen.core.cardsuit(mask))
        self.assertEqual(0, tienlen.core.cardindex(mask))

    def testCardMask2h(self):
        mask = tienlen.core.cardmask('2h')
        self.assertEqual(15, tienlen.core.cardrank(mask))
        self.assertEqual(3, tienlen.core.cardsuit(mask))
        self.assertEqual(51, tienlen.core.cardindex(mask))

    def testCardMask0(self):
        mask = tienlen.core.cardmask(0)
        self.assertEqual(3, tienlen.core.cardrank(mask))
        self.assertEqual(0, tienlen.core.cardsuit(mask))

    def testCardMask10(self):
        mask = tienlen.core.cardmask(10)
        self.assertEqual(5, tienlen.core.cardrank(mask))
        self.assertEqual(2, tienlen.core.cardsuit(mask))
        self.assertEqual(10, tienlen.core.cardindex(mask))

    def testCardMask51(self):
        mask = tienlen.core.cardmask(51)
        self.assertEqual(15, tienlen.core.cardrank(mask))
        self.assertEqual(3, tienlen.core.cardsuit(mask))

    def testCardMaskP3(self):
        self.assertRaises(TienlenException, tienlen.core.cardmask, 'P3')

    def testCardMask52(self):
        self.assertRaises(TienlenException, tienlen.core.cardmask, 52)

    def testCardMaskNegative1(self):
        self.assertRaises(TienlenException, tienlen.core.cardmask, -1)

    def testCardMaskNone(self):
        self.assertRaises(TienlenException, tienlen.core.cardmask, None)

    def testHandLenShouldBe52On52Cards(self):
        hand = tienlen.core.handmask(range(52))
        self.assertEqual(52, tienlen.core.handlen(hand))

    def testHandMaskSouldReturnSameObject(self):
        """Unclear behavior."""
        #hand1 = tienlen.core.handmask('8s Jd')
        #hand2 = tienlen.core.handmask(hand1)
        #self.assertEqual(hand1, hand2)

    def testHandMask_3s_2c_Qh(self):
        hand = tienlen.core.handmask('3s 2c Qh')
        self.assertEqual(3, tienlen.core.handlen(hand))
        self.assertEqual(3, tienlen.core.handrank(hand, 0))
        self.assertEqual(0, tienlen.core.handsuit(hand, 0))
        self.assertEqual(15, tienlen.core.handrank(hand, 1))
        self.assertEqual(1, tienlen.core.handsuit(hand, 1))
        self.assertEqual(12, tienlen.core.handrank(hand, 2))
        self.assertEqual(3, tienlen.core.handsuit(hand, 2))

    def testHighCard_5h_As(self):
        hand = tienlen.core.handmask('5h As')
        high = tienlen.core.highcard(hand)
        self.assertEqual(tienlen.core.cardmask('As'), high)

    def testHighCard_2s_2h_2d(self):
        hand = tienlen.core.handmask('2s 2h 2d')
        high = tienlen.core.highcard(hand)
        self.assertEqual(tienlen.core.cardmask('2h'), high)

    def testHandMask_8h_2d_9p_mm_2s_6c_Td_Jh_2h(self):
        """Unclear behavior. Probably throw exception."""
        #hand = tienlen.core.handmask('8h 2d 9p mm 2s 6c Td Jh 2h')
        #self.assertEqual(2, tienlen.core.handlen(hand))

    def testHandMask_0_51_8(self):
        hand = tienlen.core.handmask([0, 51, 8])
        self.assertEqual(3, tienlen.core.handrank(hand, 0))
        self.assertEqual(0, tienlen.core.handsuit(hand, 0))
        self.assertEqual(15, tienlen.core.handrank(hand, 1))
        self.assertEqual(3, tienlen.core.handsuit(hand, 1))
        self.assertEqual(5, tienlen.core.handrank(hand, 2))
        self.assertEqual(0, tienlen.core.handsuit(hand, 2))

    def testHandMaskShouldBeSameForStrAndArray(self):
        handarray = tienlen.core.handmask([0, 4, 8, 12, 13])
        handstr = tienlen.core.handmask('3s 4s 5s 6s 6c')
        self.assertEqual(handarray, handstr)

    def testHandMask_None(self):
        self.assertRaises(TienlenException, tienlen.core.handmask, None)

if __name__ == '__main__':
    unittest.main()

