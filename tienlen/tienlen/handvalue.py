"""Functions that compute and provides services for tienlen hand values."""

import tienlen.core

HV_DUPSSTART = tienlen.core.HANDCOUNT_BITLENGTH # max is 64
HV_SEQUENCESTART = HV_DUPSSTART + 4 # max is 16
HV_VALIDSTART = HV_SEQUENCESTART + 4 # max is 2

HV_HICARDMASK = tienlen.core.HANDCOUNT_MASK
HV_DUPSMASK = 0xf
HV_SEQUENCEMASK = 0xf
HV_VALIDMASK = 0x1

def seq(hvalue):
    """Number of sequences for hand value."""
    return hvalue >> HV_SEQUENCESTART & HV_SEQUENCEMASK

def dup(hvalue):
    """Number of duplicates for hand value."""
    return hvalue >> HV_DUPSSTART & HV_DUPSMASK

def valid(hvalue):
    """Whether hand is a valid tienlen hand."""
    return hvalue >> HV_VALIDSTART & HV_VALIDMASK

def hicard(hvalue):
    """High card of the hand."""
    return hvalue & HV_HICARDMASK

def isbetter(hvalue1, hvalue2):
    """Whether hvalue1 hand value is better than hvalue2 hand value."""
    if valid(hvalue1):
        if seq(hvalue2) == 0 or dup(hvalue2) == 0:
            return True
        elif seq(hvalue1) == seq(hvalue2) \
          and dup(hvalue1) == dup(hvalue2):
            return hicard(hvalue1) > hicard(hvalue2)
    return False

def rawseq(hand):
    """Gets number of raw consecutive numbers in hand."""
    cards = [tienlen.core.cardrank(c) for c in tienlen.core.handgenerator(hand)]
    if len(cards) == 0:
        return 0

    cards.sort()
    thesequence = 1
    thevalue = cards[0]
    for i in range(1, len(cards)):
        if cards[i] == thevalue:
            continue
        elif cards[i] == thevalue + 1:
            thevalue += 1
            thesequence += 1
        else:
            return 0
    return thesequence

def rawdup(hand):
    """Gets number of raw duplicates of the first card in hand."""
    result = 0
    firstrank = tienlen.core.handrank(hand, 0)
    for cardmask in tienlen.core.handgenerator(hand):
        if tienlen.core.cardrank(cardmask) == firstrank:
            result += 1
    return result

def handvalue(hand):
    """Returns the handvalue of the hand.
    Mask is of such: (1|4|4|6).
    """
    rseq = rawseq(hand)
    rdups = rawdup(hand)

    # Quick valid check
    count = len(list(tienlen.core.handgenerator(hand)))
    hvvalid = ((rseq * rdups) == count) and rseq != 2
    hvhicard = tienlen.core.cardindex(tienlen.core.highcard(hand))

    return ((hvvalid & HV_VALIDMASK) << HV_VALIDSTART) | \
           ((rseq & HV_SEQUENCEMASK) << HV_SEQUENCESTART) | \
           ((rdups & HV_DUPSMASK) << HV_DUPSSTART) | \
           (hvhicard & HV_HICARDMASK)

