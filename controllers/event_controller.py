from collections import defaultdict
from events import Event

class EventController(object):
    registry = defaultdict(lambda: defaultdict(list))

    @staticmethod
    def init():
        pass

    @staticmethod
    def register(obj, event, callback):
        EventController.registry[obj][event].append(callback)

    @staticmethod
    def fire_events(player, obj, event, **kwargs):
        for event in EventController.registry[obj][event]:
            return event(player=player, **kwargs)