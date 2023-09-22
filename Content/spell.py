class Spell:
    """
    The parent class for a spell

    Attributes
    ----------
    - type : str
      The type of spell it is
    - name : str
      Name of the spell
    - description : str
      Description of the spell
    - attack : int
      The amount of damage the spell does
    - cost : int
      The amount of mana the spell uses
    - move : str
      The name of the spell's attack
    - win_front : str
      The front half of the spell's killing message
    - win_back : str
      The back half of the spell's killing message
    """

    def __init__(self) -> None:
        self.type = "spell"
        self.name = ""
        self.description = ""
        self.attack = 0
        self.cost = 0
        self.aoe = False
        self.move = ""
        self.win_front = ""
        self.win_back = ""

    def get_save_name(self):
        return self.name.replace(" ", "")

class WingardiumLeviosa(Spell):
    """
    A spell that inherits from the Spell class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Wingardium Leviosa"
        self.attack = 10
        self.cost = 20
        self.description = f"Wingardium Leviosa is a magic spell that can make objects levitate\nDeals {self.attack} damage to a single enemy\nCost {self.cost} mana"
        self.move = " used levitation"
        self.win_front = " levitated "
        self.win_back = " so high that it breached the atmosphere and exploded"
    
class VengefulSpirit(Spell):
    """
    A spell that inherits from the Spell class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Vengeful Spirit"
        self.attack = 40
        self.cost = 25
        self.description = f"Vengeful spirit is a spirit that will fly forward and burn foes in its path\nDeals {self.attack} damage to a single enemy\nCost {self.cost} mana"
        self.move = " used Vengeful Spirit"
        self.win_front = " charged up all your soul and shot a massive vengeful spirit at "

class Megidolaon(Spell):
    """
    A spell that inherits from the Spell class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Megidolaon"
        self.attack = 60
        self.cost = 60
        self.description = f"Megidolaon is a damage dealing almighty spell\nDeals {self.attack} damage to all enemies\nCost {self.cost} mana"
        self.move = " used Megidolaon"
        self.win_back = " was blown away by the blast."
        self.aoe = True

class GlintstoneCometshard(Spell):
    """
    A spell that inherits from the Spell class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Glintstone Cometshard"
        self.attack = 150
        self.cost = 40
        self.description = f"Glintstone Cometshard fires a comet that moves forward while leaving a trail\nDeals {self.attack} damage to a single enemy\nCost {self.cost} mana"
        self.move = " shot a Glinstone Cometshard"
        self.win_front = " Shredded "
        self.win_back = " into a million pieces"

class WillOTheWisp(Spell):
    """
    A spell that inherits from the Spell class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Will O The Wisp"
        self.attack = 250
        self.cost = 60
        self.description = f"Will O The Wisp causes the enemy to explode\nDeals {self.attack} damage to a single enemy\nCost {self.cost} mana"
        self.move = " cast Will O The Wisp"
        self.win_front = " exploded "
        self.win_back = " until it burnt to a crisp"