import random
from interface import IPrisoner


class Rogue(IPrisoner):
    def get_action(self):
        if random.random() > 0.5:
            return self.DEFECT
        else:
            return self.COOPERATE
