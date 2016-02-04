from controllers.event_controller import EventController
from controllers.game_controller import GameController
from events import Event
from manas import ManaWhite, ManaBlack, ManaRed, ManaColorless
from util import color_string


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

