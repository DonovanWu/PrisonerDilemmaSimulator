from interface import IPrisoner


class TitForTat(IPrisoner):
    def get_action(self):
        if len(self.opponent_action_history) == 0:
            return self.COOPERATE
        else:
            return self.opponent_action_history[-1]
