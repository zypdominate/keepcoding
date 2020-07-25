
class Bus(object):
    def __init__(self, passengers = None):
        if passengers is None:
            self.passagers = []
        else:
            self.passagers = list(passengers)

    def up(self, someone):
        if someone in self.passagers:
            assert 0, f'{someone} is in bus already'
        self.passagers.append(someone)

    def down(self, someone):
        if someone not in self.passagers:
            assert 0, f'{someone} is not in bus now'
        self.passagers.remove(someone)
