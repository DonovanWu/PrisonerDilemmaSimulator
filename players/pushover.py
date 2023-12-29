from interface import IPrisoner


class PushOver(IPrisoner):
    def get_action(self):
        return self.COOPERATE
