class Weapon:
    """
    The parent class for a weapon

    Attributes
    ----------
    - type : str
      Type of the item picked up
    - name : str
      Name of the weapon
    - description : str
      Description of the weapon
    - attack : int
      Numerical value added to the attack of the the character
    - move : str
      Name of the weapon's attack
    - win_front : str
      The front half of the weapon's killing message
    - win_back : str
      The back half of the weapon's killing message
    """

    def __init__(self) -> None:
        self.type = "weapon"
        self.name = ""
        self.description = ""
        self.attack = 0
        self.move = ""
        self.win_front = ""
        self.win_back = ""
        self.aoe = False

    def get_save_name(self):
        return self.name.replace(" ", "")

class BusterSword(Weapon):
    """
    A weapon that inherits from the Weapon class
    """

    def __init__(self):
        super().__init__()
        self.name = "Buster Sword"
        self.attack = 10
        self.description = f"The Buster Sword is an enormous broadsword. From tip to handle, it is approximately five to six feet long, with a single-edged large blade approximately one foot wide\nDeals {self.attack} damage"
        self.move = " used Focused Thrust"
        self.win_front = " used braver and smashed "
        self.win_back = " into the ground"

class MasterSword(Weapon):
    """
    A weapon that inherits from the Weapon class
    """

    def __init__(self):
        super().__init__()
        self.name = "Master Sword"
        self.attack = 10
        self.description = f"The Master Sword is a divine magic sword with the power to vanquish evil. Infused with the sacred flames provided by the Golden Goddesses and blessed with Hylia's power\nDeals {self.attack} damage"
        self.move = " used Sword beam"
        self.win_front = " used the power of the triforce to vanquish "
        self.win_back = " from the face of the earth"

class LeviathanAxe(Weapon):
    """
    A weapon that inherits from the Weapon class
    """

    def __init__(self):
        super().__init__()
        self.name = "Leviathan Axe"
        self.attack = 40
        self.description = f"The Leviathan axe legendary two-handed battle axe imbuded with elemental magic allowing it to return to the user\nDeals {self.attack} damage"
        self.move = " threw the Leviathan Axe"
        self.win_front = " lunged towards "
        self.win_back = " and decapitated it"

class VirtuousTreaty(Weapon):
    """
    A weapon that inherits from the Weapon class
    """

    def __init__(self):
        super().__init__()
        self.name = "Virtuous Treaty"
        self.attack = 50
        self.description = f"The Virtuous Treaty is a pure white samurai blade not sullied by a single drop of blood\nDeals {self.attack} damage"
        self.move = " used Virtuous Treaty"
        self.win_front = " struck "
        self.win_back = " down in one clean slash"

class Coronacht(Weapon):
    """
    A weapon that inherits from the Weapon class
    """

    def __init__(self):
        super().__init__()
        self.name = "Coronacht"
        self.attack = 60
        self.description = f"The Coronacht is an infernal arm, the finest bow ever concevied, once weilded by Mistress Hera\nDeals {self.attack} damage"
        self.move = " used power shot"
        self.win_front = " used the aspect of Hera to shoot a power shot right through "

class Zenith(Weapon):
    """
    A weapon that inherits from the Weapon class
    """

    def __init__(self):
        super().__init__()
        self.name = "Zenith"
        self.attack = 70
        self.description = f"The Zenith is a legendary blade crafted using 10 different powerful swords\nDeals {self.attack} damage"
        self.move = " used The Zenith"
        self.win_front = " obliterated "
        self.win_back = " using the power of 10 swords"

class RGXButterflyKnife(Weapon):
    """
    A weapon that inherits from the Weapon class
    """

    def __init__(self):
        super().__init__()
        self.name = "RGX Butterfly Knife"
        self.attack = 60
        self.description = f"The RGX Butterfly Knife is the most powerful butterfly knife on earth due to its RGB\nDeals {self.attack} damage"
        self.move = " used behind the 8 ball"
        self.win_front = " performed the valorant inspect flawlessly causing "
        self.win_back = " to self destruct"

class Wand(Weapon):
    """
    A weapon that inherits from the Weapon class
    """

    def __init__(self):
        super().__init__()
        self.name = "Wand"
        self.attack = 5
        self.description = f"A generic wand\nDeals {self.attack} damage"
        self.move = " threw the wand"
        self.win_front = " poked "
        self.win_back = " to death"

class MarksmanRevolver(Weapon):
    """
    A weapon that inherits from the Weapon class
    """

    def __init__(self):
        super().__init__()
        self.name = "Marksman Revolver"
        self.attack = 50
        self.description = f"A revolver. Every few seconds a coin pops out of the bottom of the gun. The purpose of this function is lost on you\nDeals {self.attack} damage"
        self.move = " used +HEADSHOT"
        self.win_front = " threw $4.32 of change at "
        self.win_back = ", knocking it out"

class ToyKnife(Weapon):
    """
    A weapon that inherits from the Weapon class
    """

    def __init__(self):
        super().__init__()
        self.name = "Toy Knife"
        self.attack = 1
        self.description = f"Made of plastic. A rarity nowadays\nDeals {self.attack} damage"
        self.move = " used stab"
        self.win_front = " stabbed "
        self.win_back = " so much it died"

class XBaton(Weapon):
    """
    A weapon that inherits from the Weapon class
    """

    def __init__(self):
        super().__init__()
        self.name = "X Baton"
        self.attack = 100
        self.description = f"The X Baton is a police baton capable of transforming between three different styles, each with their own unique abilities and merits\nDeals {self.attack} damage"
        self.move = " used blaster mode"
        self.win_front = " activated Gladius Mode and decimated "