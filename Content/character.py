#importing from other files
from Content.armour import *
from Content.weapon import *
from Content.accessory import *
from Content.spell import *
from Content.item import *
from Content.upgrade import *

class Character:
    """
    A class that creates an instance of the player

    Attributes
    ----------
    - name : str
      Name of the player
    - health : int
      Amount of health the player has
    - max_health : int
      Maximum health of the player
    - spells : list[Spell]
      List of spells the player knows
    - attack : int
      Amount of extra damage the player deals
    - mana: int
      Amount of mana the player has
    - max_mana : int
      Maximum mana of the player
    - defence : int
      Amount of damage the player resists
    - armour : Armour
      The armour the player is wearing
    - armours : list[Armour]
      List of armours the player owns
    - weapon : Weapon
      The weapon the player is using
    - weapons : list[Weapon]
      List of weapons the player owns
    - accessory : Accessory
      The accessory the player is using
    - accessories : list[Accessory]
      List of accessories the player owns
    - health_flask : int
      Number of Flask of Crimson Tears the player owns
    - mana_flask : int
      Number of Flask of Cerulean Tears the player owns
    - items : list[Item]
      List of items the player owns

    """
    
    def __init__(self) -> None:
        self.name = ""
        self.health = 0
        self.max_health = 0
        self.spells = []
        self.attack = 0
        self.mana = 0
        self.max_mana = 0
        self.defence = 0
        self.armour = None
        self.armours = []
        self.weapon = None
        self.weapons = []
        self.accessory = None
        self.accessories = []
        self.health_flask = 0
        self.mana_flask = 0
        self.items = []
        self.upgrades = []
        self.shield = None
        self.shields = []
        self.money = 0
        self.shop = False
        self.shop_inventory = [ScotchWhiskey()]
        self.gamble = False
        self.additional_shop = False
        self.completion = 0

    def get_spells(self):
        spells = []
        for spell in self.spells:
            spells.append(spell.name)
        return spells

    def get_armours(self):
        armours = []
        for armour in self.armours:
            armours.append(armour.name)
        return armours

    def get_weapons(self):
        weapons = []
        for weapon in self.weapons:
            weapons.append(weapon.name)
        return weapons

    def get_accessories(self):
        accessories = []
        for accessory in self.accessories:
            accessories.append(accessory.name)
        return accessories

    def get_items(self):
        items = []
        for item in self.items:
            items.append(item.name)
        return items

    def get_upgrades(self):
        upgrades = []
        for upgrade in self.upgrades:
            upgrades.append(upgrade.name)
        return upgrades

    def get_shields(self):
        shields = []
        for shield in self.shields:
            shields.append(shield.name)
        return shields

    def get_shop_inventory(self):
        items = []
        for item in self.shop_inventory:
            items.append(item.name)
        return items
        
