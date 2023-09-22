class Accessory:
    """
    The parent class for an accessory

    Attributes
    ----------
    - type : str
      Type of the item picked up
    - name : str
      Name of the accessory
    - description : str
      Description of the accessory
    - health_boost : int
      Numerical value added to the health of the the character
    - attack_boost : int
      Numerical value added to the attack of the the character
    - mana_boost : int
      Numerical value added to the mana of the the character
    - defence_boost : int
      Numerical value added to the defence of the the character
    """

    def __init__(self) -> None:
        self.type = "accessory"
        self.name = ""
        self.descripton = ""
        self.health_boost = 0
        self.attack_boost = 0
        self.mana_boost = 0
        self.defence_boost = 0
        
    def get_save_name(self):
        return self.name.replace(" ", "")

class GoldenFeather(Accessory):
    """
    An accessory that inherits from the Accessory class
    """

    def __init__(self):
        super().__init__()
        self.name = "Golden Feather"
        self.mana_boost = 30
        self.description = f"The Golden Feather is a coveted and shimmering collectible that enhances your mobility. Its radiant appearance and unique functionality make it a symbol of progress and determination\nBoost mana by {self.mana_boost} points"
        

class MasterRound(Accessory):
    """
    An accessory that inherits from the Accessory class
    """

    def __init__(self):
        super().__init__()
        self.name = "Master Round"
        self.health_boost = 30
        self.description = f"The Master Round is a prestigious and rare item that boost the player's health and also serve as a symbol of their mastery of challenging battles\nBoost health by {self.health_boost} points"

class DragonAmulet(Accessory):
    """
    An accessory that inherits from the Accessory class
    """

    def __init__(self):
        super().__init__()
        self.name = "Dragon Amulet"
        self.attack_boost = 20
        self.description = f"The Dragon Amulet is a prized and ornate accessory and a symbol of membership in the Dojima Family. It features a dragon motif that represents a connection to the Yakuza world\nBoost attack by {self.attack_boost} points"
        

class ChaosEmerald(Accessory):
    """
    An accessory that inherits from the Accessory class
    """

    def __init__(self):
        super().__init__()
        self.name = "Chaos Emerald"
        self.health_boost = 20
        self.mana_boost = 10
        self.description = f"The Chaos Emerald is a mystical, multicolored gemstone of immense power. The gemstones is known for its ability to grant incredible abilities, including the power of super transformation\nBoost health by {self.health_boost} points\nBoost mana by {self.mana_boost} points"

class HolyCross(Accessory):
    """
    An accessory that inherits from the Accessory class
    """

    def __init__(self):
        super().__init__()
        self.name = "Holy Cross"
        self.defence_boost = 20
        self.description = f"The Holy Cross powerful, sacred artifact that bestows unique abilities upon the player\nBoost defence by {self.defence_boost} points"


