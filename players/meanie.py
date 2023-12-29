from interface import IPrisoner


class Meanie(IPrisoner):
    def get_action(self):
        return self.DEFECT
