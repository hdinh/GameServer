"""Unit tests for handvalue.py"""

import unittest
import tienlen.handvalue

#pylint: disable=C0103,C0111,R0904

class HandValueTests(unittest.TestCase):

    def testHandMask_empty(self):
        hand = tienlen.core.handmask([])
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(0, tienlen.handvalue.seq(value))
        self.assertEqual(0, tienlen.handvalue.dup(value))

    def testHandMask_5s(self):
        hand = tienlen.core.handmask('5s')
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(1, tienlen.handvalue.seq(value))
        self.assertEqual(1, tienlen.handvalue.dup(value))
        self.assertEqual(True, tienlen.handvalue.valid(value))
        expectedhi = tienlen.core.cardindex(tienlen.core.cardmask('5s'))
        self.assertEqual(expectedhi, tienlen.handvalue.hicard(value))

    def testHandMask_8s9h(self):
        hand = tienlen.core.handmask('8s 9h')
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(False, tienlen.handvalue.valid(value))

    def testHandMask_4s5s(self):
        hand = tienlen.core.handmask('4s 5s')
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(False, tienlen.handvalue.valid(value))

    def testHandMask_5689T(self):
        hand = tienlen.core.handmask('5s 6h 8d 9s Td')
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(False, tienlen.handvalue.valid(value))

    def testHandMask_445566(self):
        hand = tienlen.core.handmask('4s 4d 5h 5d 6d 6s')
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(3, tienlen.handvalue.seq(value))
        self.assertEqual(2, tienlen.handvalue.dup(value))
        self.assertEqual(True, tienlen.handvalue.valid(value))
        expectedhi = tienlen.core.cardindex(tienlen.core.cardmask('6d'))
        self.assertEqual(expectedhi, tienlen.handvalue.hicard(value))

    def testHandMask_3s4d5h(self):
        hand = tienlen.core.handmask('3d 4d 5h')
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(3, tienlen.handvalue.seq(value))
        self.assertEqual(1, tienlen.handvalue.dup(value))
        self.assertEqual(True, tienlen.handvalue.valid(value))
        expectedhi = tienlen.core.cardindex(tienlen.core.cardmask('5h'))
        self.assertEqual(expectedhi, tienlen.handvalue.hicard(value))

    def testHandMask_3d4s4c4h5s5d(self):
        hand = tienlen.core.handmask('3d 4s 4c 4h 5s 5d')
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(False, tienlen.handvalue.valid(value))

    def testHandMask_3456789TJQKA(self):
        hand = tienlen.core.handmask('3s 4d 5h 6h 7s 8c 9c Ts Jh Qd Kh As')
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(12, tienlen.handvalue.seq(value))
        self.assertEqual(1, tienlen.handvalue.dup(value))
        self.assertEqual(True, tienlen.handvalue.valid(value))
        expectedhi = tienlen.core.cardindex(tienlen.core.cardmask('As'))
        self.assertEqual(expectedhi, tienlen.handvalue.hicard(value))

    def testHandMask_TTTTJJJJQQQQKKKK(self):
        hand = tienlen.core.handmask(
            'Ts Tc Td Th Js Jc Jd Jh Qs Qc Qd Qh Ks Kc Kd Kh')
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(4, tienlen.handvalue.seq(value))
        self.assertEqual(4, tienlen.handvalue.dup(value))
        self.assertEqual(True, tienlen.handvalue.valid(value))
        expectedhi = tienlen.core.cardindex(tienlen.core.cardmask('Kh'))
        self.assertEqual(expectedhi, tienlen.handvalue.hicard(value))

    def testHandMask_7777(self):
        hand = tienlen.core.handmask('7s 7c 7d 7h')
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(1, tienlen.handvalue.seq(value))
        self.assertEqual(4, tienlen.handvalue.dup(value))
        self.assertEqual(True, tienlen.handvalue.valid(value))
        expectedhi = tienlen.core.cardindex(tienlen.core.cardmask('7h'))
        self.assertEqual(expectedhi, tienlen.handvalue.hicard(value))

    def testHandMask_33(self):
        hand = tienlen.core.handmask('3s 3d')
        value = tienlen.handvalue.handvalue(hand)
        self.assertEqual(1, tienlen.handvalue.seq(value))
        self.assertEqual(2, tienlen.handvalue.dup(value))
        self.assertEqual(True, tienlen.handvalue.valid(value))
        expectedhi = tienlen.core.cardindex(tienlen.core.cardmask('3d'))
        self.assertEqual(expectedhi, tienlen.handvalue.hicard(value))

    #def testCardStrings(self):
        #Seems like testing internal private behavior.
        #self.assertEqual('3s', tienlen.handvalue.CARD_STRINGS.get(0))
        #self.assertEqual('Js', tienlen.handvalue.CARD_STRINGS.get(32))
        #self.assertEqual('6h', tienlen.handvalue.CARD_STRINGS.get(15))
        #self.assertEqual('2d', tienlen.handvalue.CARD_STRINGS.get(50))
        #self.assertEqual('2h', tienlen.handvalue.CARD_STRINGS.get(51))

    def testLowCardShouldReturnLowestRankCard(self):
        hand = tienlen.core.handmask([5, 38, 4, 50, 15, 20])
        self.assertEqual(tienlen.core.cardmask(4), tienlen.core.lowcard(hand))

    def testIsBetter_3s_Empty(self):
        hand1 = tienlen.handvalue.handvalue(tienlen.core.handmask([0]))
        hand2 = tienlen.handvalue.handvalue(tienlen.core.handmask([]))
        self.assertTrue(tienlen.handvalue.isbetter(hand1, hand2))

    def testIsBetter_8s_7s(self):
        hand1 = tienlen.handvalue.handvalue(tienlen.core.handmask([14]))
        hand2 = tienlen.handvalue.handvalue(tienlen.core.handmask([20]))
        self.assertFalse(tienlen.handvalue.isbetter(hand1, hand2))

    def testIsBetter_3s4s5d_3c4c5c(self):
        hand1 = tienlen.handvalue.handvalue(tienlen.core.handmask('3s 4s 5d'))
        hand2 = tienlen.handvalue.handvalue(tienlen.core.handmask('3c 4c 5c'))
        self.assertTrue(tienlen.handvalue.isbetter(hand1, hand2))

    def testIsBetter_2s2c2d_AhAdAc(self):
        hand1 = tienlen.handvalue.handvalue(tienlen.core.handmask('2s 2c 2d'))
        hand2 = tienlen.handvalue.handvalue(tienlen.core.handmask('Ah Ad Ac'))
        self.assertTrue(tienlen.handvalue.isbetter(hand1, hand2))

    def testIsBetter_3s8s_Empty(self):
        hand1 = tienlen.handvalue.handvalue(tienlen.core.handmask([0, 32]))
        hand2 = tienlen.handvalue.handvalue(tienlen.core.handmask([]))
        self.assertFalse(tienlen.handvalue.isbetter(hand1, hand2))

if __name__ == '__main__':
    unittest.main()

