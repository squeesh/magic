from util import color_string


class Controller(object):
    players = ()

    @staticmethod
    def init():
        from gameboard import Player, Deck
        Controller.players = []
        Controller.players.append(Player(Deck.generate_deck()))

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
            }

            error = None

            try:
                input_dict[tokens[0]](player=Controller.players[0], tokens=tokens)
            except KeyError, e:
                error = e
            except IndexError, e:
                error = e

            if error:
                print 'Error: ', e
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
        Controller.print_message("player's hand: %s\n" % player.hand)

    @staticmethod
    def show_battlefield(player, **kwargs):
        Controller.print_message("player's battlefield: %s\n" % player.battlefield)

    @staticmethod
    def show_graveyard(player, **kwargs):
        Controller.print_message("player's graveyard: %s\n" % player.graveyard)

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
                curr_string = color_string('O', color_type.name)
                curr_string *= player.mana[color_type]

            if curr_string:
                mana_list.append(curr_string)

        return 'player mana updated:\n  %s' % ' '.join(mana_list)


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

            ==============================
        """

        args_dict = {}
        args_dict['card_header'] = '|' + curr_card.name
        args_dict['card_header'] += (' ' * (29 - len(args_dict['card_header'])))

        if curr_card.mana_cost:
            mana_cost = ''.join([(item.short_name * curr_card.mana_cost[item]) for item in curr_card.mana_cost])
            args_dict['card_header'] = args_dict['card_header'][:len(mana_cost) * -1] + mana_cost

        args_dict['card_header'] += '|'


        args_dict['card_type'] = '|' + player.hand[int(card_num)].type_name
        args_dict['card_type'] += (' ' * (29 - len(args_dict['card_type']))) + '|'

        Controller.print_message(card_template.format(**args_dict))


Controller.init()
