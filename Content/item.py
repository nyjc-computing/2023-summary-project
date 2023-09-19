class Item:
    """
    The parent class for an item

    Attributes
    ----------
    - name : str
      Name of the item
    - description : str
      Description of the item
    - health : int
      Numerical value added to the health of the the character
    - mana : int
      Numerical value added to the mana of the the character
    """
    
    def __init__(self):
        self.type = "item"
        self.name = ""
        self.description = ""
        self.health = 0
        self.mana = 0
        self.cost = 0

    def get_save_name(self):
        return self.name.replace(" ", "")

class FlaskOfCrimsonTears(Item):
    """
    An item that inherits from the Item class
    """

    def __init__(self):
        super().__init__()
        self.name = "Flask of Crimson Tears"
        self.health = 50
        self.description = f"The Flask of Crimson Tears is a sacred flask modelled after a golden holy chalice that was once graced by a tear of life\nHeals {self.health} health"

class FlaskOfCeruleanTears(Item):
    """
    An item that inherits from the Item class
    """

    def __init__(self):
        super().__init__()
        self.name = "Flask of Cerulean Tears"
        self.mana = 50
        self.description = f"The Flask of Cerulean Tears is a sacred flask modelled after a golden holy chalice that was once graced by a tear of life\nHeals {self.mana} mana"

class DectusMedallionRight(Item):
    """
    An item that inherits from the Item class
    """

    def __init__(self):
        super().__init__()
        self.name = "Dectus Medallion (right)"
        self.description = "The right half of a medallion with the power to break a powerful spell"

class DectusMedallionLeft(Item):
    """
    An item that inherits from the Item class
    """

    def __init__(self):
        super().__init__()
        self.name = "Dectus Medallion (left)"
        self.description = "The left half of a medallion with the power to break a powerful spell"

class MementoMortem(Item):
    """
    An accessory that inherits from the Accessory class
    """

    def __init__(self):
        super().__init__()
        self.name = "Memento Mortem"
        self.description = "The Memento Mortem is a mystical pocket watch that allows the user to view the moment of a person's death"

class BlackBox(Item):
    """
    An accessory that inherits from the Accessory class
    """

    def __init__(self):
        super().__init__()
        self.name = "Black Box"
        self.description = "An item created by reusing the core of a machine lifeform, explodes when triggered"

class RustyKey(Item):

    def __init__(self):
        super().__init__()
        self.name = "Rusty Key"
        self.description = "A Rusty Key"

class ScotchWhiskey(Item):
    def __init__(self):
        super().__init__()
        self.name = "Scotch Whiskey"
        self.description = "A bottle of Scotch Whiskey, a popular alcholic drink"
        self.cost = 100

class RoboticArm(Item):
    def __init__(self):
        super().__init__()
        self.name = "Robotic Arm"
        self.description = "A robotic left arm that still looks functional"