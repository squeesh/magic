from util import color_string


class Controller(object):
    players = ()

    @staticmethod
    def init():
        from gameboard import Player, Deck
        Controller.players = []
        Controller.players.append(Player(Deck.generate_deck()))

        # TODO: For testing...
        player_one = Controller.players[0]
        from creatures import AngelicOverseer, GoblinDeathraiders, RagingGoblin
        from cards import BasicPlains, BasicMountain
        player_one.hand.extend([AngelicOverseer(), GoblinDeathraiders(), RagingGoblin()])
        player_one.battlefield.extend([BasicPlains(), BasicPlains(), BasicPlains(), BasicMountain(), BasicMountain()])
        # End Testing

    @staticmethod
    def main_loop():
        while(True):
            input = raw_input()

            tokens = input.split(' ')

            input_dict = {
                'draw':         Controller.draw_card,
                'hand':         Controller.show_hand,
                'detail':       Controller.detail_card,
                'discard':      Controller.discard,
                'play':         Controller.play_card,
                'battlefield':  Controller.show_battlefield,
                'graveyard':    Controller.show_graveyard,
                'tap':          Controller.tap_card,
                'mana':         Controller.show_mana,
            }

            error = None

            try:
                input_dict[tokens[0]](player=Controller.players[0], tokens=tokens)
            except KeyError, e:
                error = e
            except IndexError, e:
                error = e

            if error:
                # import traceback
                # traceback.print_exc()
                print e
                print
                print 'Available commands: '
                for key in input_dict:
                    print '    ' + key

    @staticmethod
    def draw_card(player, tokens, **kwargs):
        card_num = 1
        if len(tokens) > 1:
            card_num = int(tokens[1])

        for i in range(card_num):
            Controller.print_message('player drew a card: %s' % player.draw_card())

        Controller.print_message()

    @staticmethod
    def discard(player, tokens, **kwargs):
        card_num = int(tokens[1])
        Controller.print_message('player discarded a card: %s\n' % player.discard(card_num))

    @staticmethod
    def play_card(player, tokens, **kwargs):
        card_num = int(tokens[1])
        player.play_card(card_num)

    @staticmethod
    def show_hand(player, **kwargs):
        Controller.print_message(player.hand)

    @staticmethod
    def show_battlefield(player, **kwargs):
        Controller.print_message(player.battlefield)

    @staticmethod
    def show_graveyard(player, **kwargs):
        Controller.print_message(player.graveyard)

    @staticmethod
    def show_mana(player, **kwargs):
        Controller.get_mana_string(player)

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
        Controller.print_message(Controller.get_mana_string(player))

    @staticmethod
    def add_mana(player, mana_type, count=1):
        player.add_mana(mana_type, count=count)
        Controller.print_message(Controller.get_mana_string(player))

    @staticmethod
    def can_remove_mana(player, mana_type, count=1):
        return player.can_remove_mana(mana_type, count=count)

    @staticmethod
    def remove_mana(player, mana_type, count=1):
        player.remove_mana(mana_type, count=count)
        Controller.print_message(Controller.get_mana_string(player))

    @staticmethod
    def print_message(string=''):
        print string

    @staticmethod
    def get_mana_string(player):
        mana_list = []

        for color_type in player.mana:
            curr_string = ''

            if player.mana[color_type] > 0:
                curr_string = color_string('O', color_type.color)
                curr_string *= player.mana[color_type]

            if curr_string:
                mana_list.append(curr_string)

        return 'player mana:\n  %s' % ' '.join(mana_list)


    @staticmethod
    def detail_card(player, tokens, **kwargs):
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
            {{card_abilities}}
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

        args_dict['card_type'] = '|' + player.hand[int(card_num)].type_name
        args_dict['card_type'] += (' ' * (29 - len(args_dict['card_type']))) + '|'

        args_dict['card_power'] = '|'
        power_toughness = '{}/{}'.format(curr_card.power, curr_card.toughness)
        args_dict['card_power'] += ' ' * (28 - len(power_toughness))
        args_dict['card_power'] += power_toughness
        args_dict['card_power'] += '|'

        card_abilities = ''
        if curr_card.abilities:
            card_abilities = '|'

            abilities = []
            for ability in curr_card.abilities:
                abilities = ability.display_text
            card_abilities += abilities
            card_abilities += ' ' * (28 - len(abilities))
            card_abilities += '|'

        card_art = card_template.format(**args_dict)
        card_art = card_art.format(card_abilities=card_abilities)

        Controller.print_message(card_art)


Controller.init()
