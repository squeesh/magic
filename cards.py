from manas import *
from util import color_string
from controllers import Controller
from abilities import Trample, Haste


class CardTypeMixin(object):
    type_name = ''

    def card_type_init(self):
        self.events = {
            self.Event.TAP: [],
            self.Event.PLAY: [self.play_card_event],
        }

    def play_card_event(self, player, **kwargs):
        if self.mana_cost:
            if not Controller.can_spend_mana(player, self.mana_cost):
                Controller.print_message('ERROR cannot play card, not enough mana: %s\n' % self)
                return

        player.hand.remove(self)
        player.battlefield.append(self)
        player.spend_mana(self.mana_cost)
        Controller.print_message(Controller.get_mana_string(player))
        Controller.print_message('player played a card: %s\n' % self)


class BasicLand(CardTypeMixin):
    type_name = 'Basic Land'
    mana_type = None

    def card_type_init(self):
        super(BasicLand, self).card_type_init()
        self.events[self.Event.TAP].append(self.tap_land_event)

    def tap_land_event(self, player, **kwargs):
        if not self.tapped:
            Controller.add_mana(player=player, mana_type=self.mana_type)
            self.tapped = True
            Controller.print_message("tapped card: %s\n" % self)

        elif Controller.can_remove_mana(player=player, mana_type=self.mana_type):
            Controller.remove_mana(player=player, mana_type=self.mana_type)
            self.tapped = False
            Controller.print_message("untapped card: %s\n" % self)

        else:
            self.tapped = True
            Controller.print_message("Error untapping card, not enough mana: %s\n" % self)


class Creature(CardTypeMixin):
    type_name = 'Creature'
    power = 0
    toughness = 0
    mana_cost = None
    abilities = []


class CreatureAngel(Creature):
    type_name = 'Creature - Angel'


class CreatureGoblin(Creature):
    type_name = 'Creature - Goblin'


class CreatureGoblinWarrior(CreatureGoblin):
    type_name = 'Creature - Goblin Warrior'


class CreatureGoblinBerserker(CreatureGoblin):
    type_name = 'Creature - Goblin Berserker'


class Card(object):
    class Event:
        TAP = 'event_tap'
        PLAY = 'event_play'

    name = ''
    abilities = ()
    counters = ()
    mana_cost = None
    color = ''
    tapped = False
    events = None

    def __init__(self):
        self.card_type_init()

    def __str__(self):
        tapped = ''
        if self.tapped:
            tapped = ': TAPPED'

        if self.color:
            return color_string(self.type_name + ' - ' + self.name + tapped, self.color)

        return self.type_name + ' - ' + self.name + tapped

    def tap_card(self, **kwargs):
        self.fire_event(self.Event.TAP, **kwargs)

    def play_card(self, **kwargs):
        self.fire_event(self.Event.PLAY, **kwargs)

    def register_event(self, event_code, event_callback):
        self.events[event_code].append(event_callback)

    def fire_event(self, event_code, **kwargs):
        for event in self.events[event_code]:
            event(**kwargs)


class AngelicOverseer(Card, CreatureAngel):
    name = 'Angelic Overseer'
    color = 'white'
    power = 5
    toughness = 3
    mana_cost = {
        ManaColorless: 3,
        ManaWhite: 2,
    }


class GoblinCavaliers(Card, CreatureGoblin):
    name = 'Goblin Cavaliers'
    color = 'red'
    power = 3
    toughness = 2
    mana_cost = {
        ManaColorless: 2,
        ManaRed: 1,
    }


class GoblinDeathraiders(Card, CreatureGoblinWarrior):
    name = 'Goblin Deathraiders'
    color = 'black & red'
    power = 3
    toughness = 1
    mana_cost = {
        ManaBlack: 1,
        ManaRed: 1,
    }
    abilities = [Trample]


class RagingGoblin(Card, CreatureGoblinBerserker):
    name = 'Raging Goblin'
    color = 'red'
    power = 1
    toughness = 1
    mana_cost = {
        ManaRed: 1,
    }
    abilities = [Haste]


class BasicSwamp(Card, BasicLand):
    name = 'Swamp'
    color = 'black'
    mana_type = ManaBlack


class BasicMountain(Card, BasicLand):
    name = 'Mountain'
    color = 'red'
    mana_type = ManaRed


class BasicPlains(Card, BasicLand):
    name = 'Plains'
    color = 'white'
    mana_type = ManaWhite
