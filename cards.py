from manas import ManaBlue, ManaWhite, ManaBlack, ManaGreen, ManaRed, ManaColorless
from util import color_string
from events import Event
from game_controller import GameController
from event_controller import EventController


class CardTypeMixin(object):
    type_name = ''

    def card_type_init(self):
        EventController.register(self, Event.PLAY, self.play_card_event)

    def play_card_event(self, player, **kwargs):
        if self.mana_cost:
            if not GameController.can_spend_mana(player, self.mana_cost):
                GameController.print_message('ERROR cannot play card, not enough mana: %s\n' % self)
                return

        player.hand.remove(self)
        player.battlefield.append(self)
        player.spend_mana(self.mana_cost)
        GameController.print_message(GameController.get_mana_string(player))
        GameController.print_message('player played a card: %s\n' % self)


class BasicLand(CardTypeMixin):
    type_name = 'Basic Land'
    mana_type = None

    def card_type_init(self):
        super(BasicLand, self).card_type_init()
        EventController.register(self, Event.TAP, self.tap_land_event)
        # self.events[self.Event.TAP].append(self.tap_land_event)

    def tap_land_event(self, player, **kwargs):
        if not self.tapped:
            GameController.add_mana(player=player, mana_type=self.mana_type)
            self.tapped = True
            GameController.print_message("tapped card: %s\n" % self)

        elif GameController.can_remove_mana(player=player, mana_type=self.mana_type):
            GameController.remove_mana(player=player, mana_type=self.mana_type)
            self.tapped = False
            GameController.print_message("untapped card: %s\n" % self)

        else:
            self.tapped = True
            GameController.print_message("Error untapping card, not enough mana: %s\n" % self)


class Card(object):
    name = ''
    abilities = ()
    counters = ()
    mana_cost = ()
    # color = ''
    tapped = False
    events = None

    def __init__(self):
        self.card_type_init()

    def __str__(self):
        tapped = ''
        if self.tapped:
            tapped = ': TAPPED'

        if self.get_color():
            return color_string(self.type_name + ' - ' + self.name + tapped, self.get_color())

        return self.type_name + ' - ' + self.name + tapped

    def tap_card(self, **kwargs):
        EventController.fire_events(obj=self, event=Event.TAP, **kwargs)
        # self.fire_event(self.Event.TAP, **kwargs)

    def play_card(self, **kwargs):
        EventController.fire_events(obj=self, event=Event.PLAY, **kwargs)
        # self.fire_event(self.Event.PLAY, **kwargs)

    # def register_event(self, event_code, event_callback):
    #     self.events[event_code].append(event_callback)

    # def fire_event(self, event_code, **kwargs):
    #     for event in self.events[event_code]:
    #         event(**kwargs)

    def get_color(self):
        colors = []
        for mana in self.mana_cost:
            if mana is not ManaColorless:
                colors.append(mana.color)

        if not colors:
            return 'colorless'
        elif len(colors) == 1:
            return colors[0]
        return 'gold'


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
