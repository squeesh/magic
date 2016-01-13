from abilities import Trample, Haste
from cards import Card, CardTypeMixin
from manas import ManaBlue, ManaWhite, ManaBlack, ManaGreen, ManaRed, ManaColorless


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

