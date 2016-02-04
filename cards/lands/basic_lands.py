from controllers.event_controller import EventController
from controllers.game_controller import GameController
from events import Event
from manas import ManaWhite, ManaBlack, ManaRed, ManaColorless
from util import color_string
from cards.mixins import CardTypeMixin
from cards import Card


class BasicLandType(CardTypeMixin):
    type_name = 'Basic Land'
    mana_type = None

    def card_type_init(self):
        super(BasicLandType, self).card_type_init()
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


class BasicSwamp(Card, BasicLandType):
    name = 'Swamp'
    color = 'black'
    mana_type = ManaBlack


class BasicMountain(Card, BasicLandType):
    name = 'Mountain'
    color = 'red'
    mana_type = ManaRed


class BasicPlains(Card, BasicLandType):
    name = 'Plains'
    color = 'white'
    mana_type = ManaWhite

