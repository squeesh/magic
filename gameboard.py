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
        self.battlefield = Battlefield()
        self.graveyard = Graveyard()
        self.mana_pool = {
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
        copied_mana = copy(self.mana_pool)

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
            for mana_type, count in mana_cost.items():
                if mana_type != ManaColorless:
                    self.remove_mana(mana_type, count)

            mana_type = ManaColorless
            count = mana_cost.get(ManaColorless, 0)
            if count:
                assert sum(self.mana_pool.values()) >= count
                self.remove_mana(mana_type, count)

    def add_mana(self, mana_type, count=1):
        assert mana_type and count > 0
        self.mana_pool[mana_type] += count

    def can_remove_mana(self, mana_type, count=1):
        can_remove = True

        if mana_type != ManaColorless:
            if count > self.mana_pool[mana_type]:
                can_remove = False

        elif count > sum(self.mana_pool.values()):
            can_remove = False

        return can_remove

    def remove_mana(self, mana_type, count=1):
        assert mana_type and count > 0
        if mana_type != ManaColorless:
            self.mana_pool[mana_type] -= count  # Assumption, we have already determined they have the available mana
        else:
            # TODO: Comment this...
            count -= self.mana_pool[ManaColorless]
            if count < 0:
                self.mana_pool[ManaColorless] = count * -1
                count = 0
            else:
                self.mana_pool[ManaColorless] = 0

            for curr_mana_type in self.mana_pool:
                count -= self.mana_pool[curr_mana_type]
                if count < 0:
                    self.mana_pool[curr_mana_type] = count * -1
                    count = 0
                else:
                    self.mana_pool[curr_mana_type] = 0
        assert self.mana_pool[mana_type] >= 0
