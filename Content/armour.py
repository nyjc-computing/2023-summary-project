class Armour:
    """
    The parent class for an armour

    Attributes
    ----------
    - type : str
      Type of the item picked up
    - name : str
      Name of the armour
    - description : str
      Description of the armour
    - defence : int
      Numerical value added to the defence of the the character
    """
    
    def __init__(self) -> None:
        self.type = "armour"
        self.name = ""
        self.description = ""
        self.defence = 0
    
    def get_save_name(self):
        return self.name.replace(" ", "")

class NetheriteArmour(Armour):
    """
    An armour that inherits from the Armour class
    """

    def __init__(self):
        super().__init__()
        self.defence = 10
        self.name = "Netherite Armour"
        self.description = f"Netherite Armour is crafted by combining diamond armor with Netherite ingots, it offers increased damage resistance and durability\nProvides {self.defence} defence"

class OrnatePlate(Armour):
    """
    An armour that inherits from the Armour class
    """

    def __init__(self):
        super().__init__()
        self.defence = 15
        self.name = "Ornate Plate"
        self.description = f"Ornate Plate is a regal and decorative suit of armor that not only enhances the player's defense but also adds a touch of grandeur to their appearance\nProvides {self.defence} defence"

class PowerSuit(Armour):
    """
    An armour that inherits from the Armour class
    """

    def __init__(self):
        super().__init__()
        self.defence = 30
        self.name = "Power Suit"
        self.description = f"The Power Suit provides exceptional protection enabling you to navigate the treacherous alien landscapes and combat formidable foes encountered throughout your missions\nProvides {self.defence} defence"

class DragonMail(Armour):
    """
    An armour that inherits from the Armour class
    """

    def __init__(self):
        super().__init__()
        self.defence = 20
        self.name = "Dragon Mail"
        self.description = f"Dragon Mail is a legendary and formidable piece of armor that offers exceptional defense and protection for the wearer. It features dragon-scale motifs, reflecting its durability and resistance to various forms of damage\nProvides {self.defence} defence"

class Cappy(Armour):
    """
    An armour that inherits from the Armour class
    """

    def __init__(self):
        super().__init__()
        self.defence = 25
        self.name = "Cappy"
        self.description = f"Cappy is a sentient, shape-shifting hat with the ability to possess objects and enemies\nProvides {self.defence} defence"