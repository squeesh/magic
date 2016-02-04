from abilities import Trample, Haste
from cards import Card
from cards.mixins import CardTypeMixin
from manas import ManaBlue, ManaWhite, ManaBlack, ManaGreen, ManaRed, ManaColorless
from controllers.game_controller import GameController


class InstantType(CardTypeMixin):
    type_name = 'Instant'
    mana_cost = None
    abilities = ()

    def play_card_event(self, player, **kwargs):
        if self.mana_cost:
            if not GameController.can_spend_mana(player, self.mana_cost):
                GameController.print_message('ERROR cannot play card, not enough mana: %s\n' % self)
                return

        player.hand.remove(self)
        player.graveyard.append(self)
        player.spend_mana(self.mana_cost)
        GameController.print_message(GameController.get_mana_string(player))
        GameController.print_message('player played a card: %s\n' % self)


class WarReport(Card, InstantType):
    name = 'War Report'
    color = 'white'
    mana_cost = {
        ManaColorless: 3,
        ManaWhite: 1,
    }
    ability_text = 'You gain life equal to the number of creatures on the battlefield'\
        'plus the number of artifacts on the battlefield'

    def play_card_event(self, player, **kwargs):
        super(WarReport, self).play_card_event(player, **kwargs)
        count = GameController.get_battlefield_creature_count()
        count += GameController.get_battlefield_artifact_count()
        player.add_health(count)


