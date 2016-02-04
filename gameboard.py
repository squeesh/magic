import random


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
        from cards.lands.basic_lands import BasicMountain, BasicPlains
        from cards.creatures import AngelicOverseer, GoblinCavaliers, GoblinDeathraiders
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

