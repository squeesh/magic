from util import color_string


class GameController(object):
    players = ()

    @staticmethod
    def init():
        from gameboard import Deck
        from players import Player
        GameController.players = []
        GameController.players.append(Player(Deck.generate_deck()))

        # TODO: For testing...
        player_one = GameController.players[0]
        from cards.creatures import AngelicOverseer, GoblinDeathraiders, RagingGoblin
        from cards.lands.basic_lands import BasicPlains, BasicMountain, BasicSwamp
        player_one.hand.extend([AngelicOverseer(), GoblinDeathraiders(), RagingGoblin()])
        player_one.battlefield.extend([
            BasicPlains(), BasicPlains(), BasicPlains(), BasicPlains(),
            BasicMountain(), BasicMountain(), BasicMountain(), BasicMountain(),
            BasicSwamp(), BasicSwamp(), BasicSwamp(), BasicSwamp(),
        ])
        # End Testing

    @staticmethod
    def main_loop():
        while(True):
            tokens = input().split(' ')

            input_dict = {
                'draw':         GameController.draw_card,
                'hand':         GameController.show_hand,
                'detail':       GameController.detail_card,
                'discard':      GameController.discard,
                'play':         GameController.play_card,
                'battlefield':  GameController.show_battlefield,
                'graveyard':    GameController.show_graveyard,
                'tap':          GameController.tap_card,
                'mana':         GameController.show_mana,
            }

            error = None

            try:
                input_dict[tokens[0]](player=GameController.players[0], tokens=tokens)
            except KeyError as e:
                error = e
            except IndexError as e:
                error = e

            if error:
                # import traceback
                # traceback.print_exc()
                print(error)
                print()
                print('Available commands: ')
                for key in input_dict:
                    print('    ' + key)

    @staticmethod
    def draw_card(player, tokens, **kwargs):
        card_num = 1
        if len(tokens) > 1:
            card_num = int(tokens[1])

        for i in range(card_num):
            GameController.print_message('player drew a card: %s' % player.draw_card())

        GameController.print_message()

    @staticmethod
    def discard(player, tokens, **kwargs):
        card_num = int(tokens[1])
        GameController.print_message('player discarded a card: %s\n' % player.discard(card_num))

    @staticmethod
    def play_card(player, tokens, **kwargs):
        card_num = int(tokens[1])
        player.play_card(card_num)

    @staticmethod
    def show_hand(player, **kwargs):
        GameController.print_message(player.hand)

    @staticmethod
    def show_battlefield(player, **kwargs):
        GameController.print_message(player.battlefield)

    @staticmethod
    def show_graveyard(player, **kwargs):
        GameController.print_message(player.graveyard)

    @staticmethod
    def show_mana(player, **kwargs):
         GameController.print_message(GameController.get_mana_string(player))

    @staticmethod
    def tap_card(player, tokens, **kwargs):
        card_num = int(tokens[1])
        player.tap_card(card_num)

    @staticmethod
    def can_spend_mana(player, mana_cost):
        return player.can_spend_mana(mana_cost)

    @staticmethod
    def spend_mana(player, mana_type, count=1):
        player.spend_mana(mana_type, count=count)
        GameController.print_message(GameController.get_mana_string(player))

    @staticmethod
    def add_mana(player, mana_type, count=1):
        player.add_mana(mana_type, count=count)
        GameController.print_message(GameController.get_mana_string(player))

    @staticmethod
    def can_remove_mana(player, mana_type, count=1):
        return player.can_remove_mana(mana_type, count=count)

    @staticmethod
    def remove_mana(player, mana_type, count=1):
        player.remove_mana(mana_type, count=count)
        GameController.print_message(GameController.get_mana_string(player))

    @staticmethod
    def print_message(string=''):
        print(string)

    @staticmethod
    def get_mana_string(player):
        mana_list = []

        for color_type in player.mana_pool:
            curr_string = ''

            if player.mana_pool[color_type] > 0:
                curr_string = color_string('O', color_type.color)
                curr_string *= player.mana_pool[color_type]

            if curr_string:
                mana_list.append(curr_string)

        return 'player mana:\n  %s' % ' '.join(mana_list)


    @staticmethod
    def detail_card(player, tokens, **kwargs):
        from cards.creatures import CreatureType

        card_num = int(tokens[1])
        curr_card = player.hand[card_num]

        card_template = """
            ==============================
            {card_header}
            ==============================
            |(Fancy image goes here)     |
            |                            |
            |                            |
            |                            |
            |                            |
            |                            |
            ==============================
            {card_type}
            ==============================
            {card_abilities}
            |                            |
            |                            |
            |                            |
            |                            |
            {card_power}
            ==============================
        """

        args_dict = {}
        args_dict['card_header'] = '|' + color_string(curr_card.name, curr_card.get_color())
        args_dict['card_header'] += (' ' * (28 - len(curr_card.name)))

        if curr_card.mana_cost:
            mana_count = sum([curr_card.mana_cost[mana] for mana in curr_card.mana_cost])
            mana_str = ''.join([color_string(mana.short_name * curr_card.mana_cost[mana], mana.color) for mana in curr_card.mana_cost])
            args_dict['card_header'] = args_dict['card_header'][:mana_count * -1] + mana_str

        args_dict['card_header'] += '|'

        args_dict['card_type'] = '|' + player.hand[int(card_num)].type_name.ljust(28) + '|'

        if isinstance(curr_card, CreatureType):
            power_toughness = '{}/{}'.format(curr_card.power, curr_card.toughness)
            args_dict['card_power'] = '|' + power_toughness.rjust(28) + '|'

            ability_text = ''
            if curr_card.abilities:
                ability_text = ', '.join([ability.display_text for ability in curr_card.abilities])
            args_dict['card_abilities'] = '|' + ability_text.ljust(28) + '|'
        else:
            args_dict['card_power'] = '|' + (' ' * 28) + '|'
            args_dict['card_abilities'] = '|' + (' ' * 28) + '|'

        card_art = card_template.format(**args_dict)

        GameController.print_message(card_art)


GameController.init()
