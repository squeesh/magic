import random
from manas import *


class CardContainer(list):
    def __repr__(self):
        if not len(self):
            return '[Empty]'
        return '[<%s>]' % '>, <'.join(['%s' % item for item in self])


class Deck(CardContainer):
    def shuffle(self):
        random.shuffle(self)

    @staticmethod
    def generate_deck():
        from cards import BasicMountain, BasicPlains
        from creatures import AngelicOverseer, GoblinCavaliers, GoblinDeathraiders
        curr_deck = Deck()

        for i in range(10):
            curr_deck.append(BasicMountain())
            curr_deck.append(BasicPlains())

        for i in range(4):
            curr_deck.append(AngelicOverseer())

        for i in range(4):
            curr_deck.append(GoblinCavaliers())

        for i in range(4):
            curr_deck.append(GoblinDeathraiders())

        curr_deck.shuffle()
        return curr_deck


class Hand(CardContainer):
    pass


class Battlefield(CardContainer):
    pass


class Graveyard(CardContainer):
    pass


class Player(object):
    def __init__(self, library):
        self.library = library
        self.hand = Hand()

        # TODO: For testing...
        from creatures import AngelicOverseer, GoblinDeathraiders, RagingGoblin
        self.hand.append(AngelicOverseer())
        self.hand.append(GoblinDeathraiders())
        self.hand.append(RagingGoblin())
        # End Testing

        self.battlefield = Battlefield()
        self.graveyard = Graveyard()
        self.mana = {
            ManaBlue: 0,
            ManaWhite: 0,
            ManaBlack: 0,
            ManaGreen: 0,
            ManaRed: 0,
            ManaColorless: 0,
        }

    def draw_card(self):
        drawn_card = self.library.pop(0)
        self.hand.append(drawn_card)

        return drawn_card

    def discard(self, card_num):
        discarded_card = self.hand.pop(card_num)
        self.graveyard.append(discarded_card)

        return discarded_card

    def play_card(self, card_num):
        self.hand[card_num].play_card(player=self)

    def tap_card(self, card_num):
        self.battlefield[card_num].tap_card(player=self)

    def can_spend_mana(self, mana_cost):
        from copy import copy
        can_spend = True
        copied_mana = copy(self.mana)

        for mana_type in mana_cost:
            if mana_type != ManaColorless:
                if mana_cost[mana_type] > copied_mana[mana_type]:
                    can_spend = False

                else:
                    copied_mana[mana_type] -= mana_cost[mana_type]

        if ManaColorless in mana_cost:
            remaining_mana = sum(copied_mana.values())

            if mana_cost[ManaColorless] > remaining_mana:
                can_spend = False

        return can_spend

    def spend_mana(self, mana_cost):
        if mana_cost:
            for mana_type, count in mana_cost.iteritems():
                if mana_type != ManaColorless:
                    self.remove_mana(mana_type, count)

            mana_type = ManaColorless
            count = mana_cost[ManaColorless]
            assert sum(self.mana.values()) >= count
            self.remove_mana(mana_type, count)

    def add_mana(self, mana_type, count=1):
        assert mana_type and count > 0
        self.mana[mana_type] += count

    def can_remove_mana(self, mana_type, count=1):
        can_remove = True

        if mana_type != ManaColorless:
            if count > self.mana[mana_type]:
                can_remove = False

        elif count > sum(self.mana.values()):
            can_remove = False

        return can_remove

    def remove_mana(self, mana_type, count=1):
        assert mana_type and count > 0
        if mana_type != ManaColorless:
            self.mana[mana_type] -= count
        else:
            count -= self.mana[ManaColorless]
            if count < 0:
                self.mana[ManaColorless] = count * -1
                count = 0
            else:
                self.mana[ManaColorless] = 0

            for curr_mana_type in self.mana:
                count -= self.mana[curr_mana_type]
                if count < 0:
                    self.mana[curr_mana_type] = count * -1
                    count = 0
                else:
                    self.mana[curr_mana_type] = 0
        assert self.mana[mana_type] >= 0
