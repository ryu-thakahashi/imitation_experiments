from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'network_pd'
    PLAYERS_PER_GROUP = 20
    NUM_ROUNDS = 15
    K = 4  # number of neighbors in the circle network


class Subsession(BaseSubsession):
    def creating_session(self):
        for g in self.get_groups():
            g.condition = random.choice(['提示群', '非提示群'])


class Group(BaseGroup):
    condition = models.StringField()

    def get_neighbors(self, player: Player):
        players = self.get_players()
        idx = player.id_in_group - 1
        neighbors = []
        half_k = int(C.K / 2)
        for i in range(1, half_k + 1):
            neighbors.append(players[(idx - i) % C.PLAYERS_PER_GROUP])
            neighbors.append(players[(idx + i) % C.PLAYERS_PER_GROUP])
        return neighbors

    def set_payoffs_and_info(self):
        matrix = {
            ('A', 'A'): (2, 2),
            ('A', 'B'): (0, 3),
            ('B', 'A'): (3, 0),
            ('B', 'B'): (1, 1),
        }

        for p in self.get_players():
            payoff = 0
            for n in self.get_neighbors(p):
                payoff += matrix[(p.choice, n.choice)][0]
            p.payoff = payoff


class Player(BasePlayer):
    choice = models.StringField(
        choices=[('A', 'A'), ('B', 'B')], widget=widgets.RadioSelect
    )
    payoff = models.CurrencyField()


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['choice']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs_and_info'


class Results(Page):
    def vars_for_template(self):
        return {
            'neighbors': self.group.get_neighbors(self.player),
            'show_payoff': self.group.condition == '提示群',
        }


page_sequence = [MyPage, ResultsWaitPage, Results]
