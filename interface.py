from abc import abstractmethod


class IPrisoner:
    COOPERATE = 'C'
    DEFECT = 'D'

    def __init__(self):
        self.opponent_action_history = []

    @abstractmethod
    def get_action(self):
        """
        Returns either COOPERATE or DEFLECT
        """
        pass
