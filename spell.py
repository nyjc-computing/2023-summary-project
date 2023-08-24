class Spell:

    def __init__(self):
        self.type = "spell"
        self.name = ""
        self.description = ""
        self.attack = 0
        self.cost = 0
        self.move = ""
        self.win_front = ""
        self.win_back = ""

    def get_type(self):
        return self.type
    
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_description(self, description):
        self.description = description
        
    def get_description(self):
        return self.description

    def set_attack(self, attack):
        self.attack = attack

    def get_attack(self):
        return self.attack

    def set_cost(self, cost):
        self.cost = cost

    def get_cost(self):
        return self.cost

    def set_move(self, move):
        self.move = move
        
    def get_move(self):
        return self.move

    def set_win_front(self, win_front):
        self.win_front = win_front
        
    def get_win_front(self):
        return self.win_front

    def set_win_back(self, win_back):
        self.win_back = win_back
        
    def get_win_back(self):
        return self.win_back

class WingardiumLeviosa(Spell):
    def __init__(self):
        super().__init__()
        self.set_name("Wingardium Leviosa")
        self.set_attack(5)
        self.set_cost(5)
        self.set_description(f"Wingardium Leviosa is a magic spell that can make objects levitate\nDeals {self.get_attack()} damage\nCost {self.get_cost()} mana")
        self.set_move(" used levitation")
        self.set_win_front(" levitated ")
        self.set_win_back(" so high that it breached the atmosphere and exploded")
    
class VengefulSpirit(Spell):

    def __init__(self):
        super().__init__()
        self.set_name("Vengeful Spirit")
        self.set_attack(10)
        self.set_cost(10)
        self.set_description(f"Vengeful spirit is a spirit that will fly forward and burn foes in its path\nDeals {self.get_attack()} damage\nCost {self.get_cost()} mana")
        self.set_move(" used Vengeful Spirit")
        self.set_win_front(" charged up all your soul and shot a massive vengeful spirit at ")
        self.set_win_back("")

class Megidolaon(Spell):

    def __init__(self):
        super().__init__()
        self.set_name("Megidolaon")
        self.set_attack(30)
        self.set_cost(20)
        self.set_description(f"Megidolaon is a damage dealing almighty spell\nDeals {self.get_attack()} damage\nCost {self.get_cost()} mana")
        self.set_move(" used Megidolaon")
        self.set_win_front(" summoned your persona Satanael and dealt massive almighty damage to ")
        self.set_win_back("")

class GlintstoneCometshard(Spell):

    def __init__(self):
        super().__init__()
        self.set_name("Glintstone Cometshard")
        self.set_attack(40)
        self.set_cost(25)
        self.set_description(f"Glintstone Cometshard fires a comet that moves forward while leaving a trail\nDeals {self.get_attack()} damage\nCost {self.get_cost()} mana")
        self.set_move(" shot a Glinstone Cometshard")
        self.set_win_front(" Shredded ")
        self.set_win_back(" into a million pieces")

class WillOTheWisp(Spell):

    def __init__(self):
        super().__init__()
        self.set_name("Will O The Wisp")
        self.set_attack(50)
        self.set_cost(30)
        self.set_description(f"Will O The Wisp causes the enemy to explode\nDeals {self.get_attack()} damage\nCost {self.get_cost()} mana")
        self.set_move(" exploded")
        self.set_win_front(" exploded ")
        self.set_win_back(" until it burnt to a crisp")