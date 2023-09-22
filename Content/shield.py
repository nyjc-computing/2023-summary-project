class Shield:
    def __init__(self):
        self.type = "shield"
        self.name = ""
        self.description = ""
        self.negation = 0

    def get_save_name(self):
        return self.name.replace(" ", "")

class HylianShield(Shield):
    def __init__(self):
        super().__init__()
        self.name = "Hylian Shield"
        self.negation = 50
        self.description = f"The Hylian Shield was passed down through the Hyrulean royal family, along with the legend of the hero who wielded it\nNegates {self.negation}% damage when defending"