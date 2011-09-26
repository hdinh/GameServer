"""Core functions for Tienlen business logic."""

from tienlen.misc import TienlenException

CARD_STRINGS = {
  '3s':0,  '3c':1,  '3d':2,  '3h':3,
  '4s':4,  '4c':5,  '4d':6,  '4h':7,
  '5s':8,  '5c':9,  '5d':10, '5h':11,
  '6s':12, '6c':13, '6d':14, '6h':15,
  '7s':16, '7c':17, '7d':18, '7h':19,
  '8s':20, '8c':21, '8d':22, '8h':23,
  '9s':24, '9c':25, '9d':26, '9h':27,
  'Ts':28, 'Tc':29, 'Td':30, 'Th':31,
  'Js':32, 'Jc':33, 'Jd':34, 'Jh':35,
  'Qs':36, 'Qc':37, 'Qd':38, 'Qh':39,
  'Ks':40, 'Kc':41, 'Kd':42, 'Kh':43,
  'As':44, 'Ac':45, 'Ad':46, 'Ah':47,
  '2s':48, '2c':49, '2d':50, '2h':51}

RANK_OFFSET = 3
CARD_BITLENGTH = 16
CARD_MASK = (1 << CARD_BITLENGTH) - 1
HANDCOUNT_BITLENGTH = 6
HANDCOUNT_MASK = (1 << HANDCOUNT_BITLENGTH) - 1

def create_cardmask(index):
    """Creates a mask for the given index."""
    return index / 4 << 8 | index % 4 << 6 | index

def cardrank(mask):
    """Returns the rank of the card mask."""
    return (mask >> 8) + RANK_OFFSET

def cardsuit(mask):
    """Returns the suit of the card mask."""
    return mask >> 6 & 0x3

def cardindex(mask):
    """Returns the index of the card mask."""
    return mask & 0x3F

def cardmask_str(card):
    """Returns the cardmask of the card string."""
    if card in CARD_STRINGS:
        mask = create_cardmask(CARD_STRINGS.get(card))
    else:
        raise TienlenException('card string %s is not valid' % card)
    return mask

def cardmask(card):
    """Returns the card mask associated with the card object"""
    if isinstance(card, str):
        mask = cardmask_str(card)
    elif isinstance(card, int):
        if card < 52 and card > -1:
            mask = create_cardmask(card)
        else:
            raise TienlenException('card index %s is not valid' % card)
    else:
        raise TienlenException('card %s type is not known' % str(card))
    return mask

def handlen(mask):
    """Returns how many cards are contained in the hand mask."""
    return mask & HANDCOUNT_MASK

def handrank(mask, index):
    """Returns rank of card at the specified index of hand."""
    mask = mask >> (HANDCOUNT_BITLENGTH + (index * CARD_BITLENGTH))
    return cardrank(CARD_MASK & mask)

def handsuit(mask, index):
    """Returns suit of card at the specified index of hand."""
    mask = mask >> (HANDCOUNT_BITLENGTH + (index * CARD_BITLENGTH))
    return cardsuit(CARD_MASK & mask)

def create_handmask(hand_iter):
    """Returns handmask."""
    i = 0
    mask = 0

    # OR all the card masks
    for cardmaskvalue in hand_iter:
        mask |= cardmaskvalue << (i * CARD_BITLENGTH)
        i += 1

    # then, write the # cards in the first for bits
    mask <<= HANDCOUNT_BITLENGTH
    mask |= i
    return mask

def create_handmask_str(hand_str):
    """Preprocesses hand_str for handmask."""
    def hand_iterator():
        """Local iterator with scope of hand_str."""
        cards = hand_str.split(' ')
        for card in cards:
            yield cardmask_str(card)
    return create_handmask(hand_iterator())

def create_handmask_list(hand_list):
    """Preprocesses hand_list for handmask."""
    def hand_iterator():
        """Local iterator with scope of hand_list."""
        for card in hand_list:
            yield create_cardmask(card)
    return create_handmask(hand_iterator())

def handmask(hand):
    """Creates a mask for the given hand value."""
    if isinstance(hand, str):
        mask = create_handmask_str(hand)
    elif isinstance(hand, list):
        mask = create_handmask_list(hand)
    else:
        raise TienlenException('hand %s is not valid' % str(hand))
    return mask

def handgenerator(hand):
    """Returns a card iterator for the hand."""
    for i in range(handlen(hand)):
        mask = hand >> (HANDCOUNT_BITLENGTH  + (i * CARD_BITLENGTH))
        card = CARD_MASK & mask
        yield card

def highcard(hand):
    """Returns high card of hand."""
    hirank = -1
    hicard = 0
    for card in handgenerator(hand):
        cardhi = cardindex(card)
        if cardhi > hirank:
            hirank = cardhi
            hicard = card
    return hicard

def lowcard(hand):
    """Returns high card of hand."""
    lorank = 255
    locard = 0
    for card in handgenerator(hand):
        cardlo = cardindex(card)
        if cardlo < lorank:
            lorank = cardlo
            locard = card
    return locard

