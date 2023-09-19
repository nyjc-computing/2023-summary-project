#importing from other files
from Content.armour import *
from Content.weapon import *
from Content.accessory import *
from Content.spell import *
from Content.item import *
from Content.upgrade import *
from Content.shield import *

class Enemy:
    """
    The parent class for an enemy

    Attributes
    ----------
    - name : str
      Name of the enemy
    - health : int
      Amount of health the enemy has
    - attack : int
      Amount of damage the enemy deals
    - loot : Item
      The loot the enemy drops when killed
    - description : str
      Description of the enemy
    - move : str
      Description of the enemy's attack
    """

    def __init__(self) -> None:
        self.name = ""
        self.health = 0
        self.attack = 0
        self.loot = None
        self.description = ""
        self.move = ""
        self.defence = 0
        self.money = 50
        self.music = "General_Mugen.mp3"

    def get_save_name(self):
        return self.name.replace(" ", "")


class TheRadiance(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "The Radiance"
        self.health = 500
        self.attack = 50
        self.move = "Wall of Light"
        self.loot = ShadeCloak()
        self.music = "The_Radiance.mp3"

class TheHollowKnight(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "The Hollow Knight"
        self.health = 100
        self.description = "a tall, armored, and humanoid figure with a dark, hollow, and mask-like visage. Its armor is ornate and tarnished, adorned with intricate patterns and spikes. It wields a large nail as a weapon, and its appearance exudes a sense of somber and eerie presence"
        self.attack = 10
        self.move = "Triple Slash"
        self.loot = VengefulSpirit()
        self.music = "The_Hollow_Knight.mp3"

class MrOshiro(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Mr Oshiro"
        self.health = 80
        self.description = "a well-meaning but tormented ghostly hotel owner in Celeste, haunted by his past and struggling to maintain his crumbling establishment"
        self.attack = 8
        self.move = "Charge"
        self.loot = GoldenFeather()
        self.music = "Mr_Oshiro.mp3"

class TheHighDragun(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "The High Dragun"
        self.health = 80
        self.description = "a powerful dragon armed to the teeth with an array of deadly attacks and a formidable challenge for any gungeoneer"
        self.attack = 15
        self.move = "Bullet Stream"
        self.loot = MasterRound()

class Malenia(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Malenia, Blade of Miquella"
        self.health = 170
        self.description = "a menacing warrior who has never known defeat. Wields a legendary katana using her prosthetic arm"
        self.attack = 25
        self.move = "Waterfowl Dance"
        self.loot = GlintstoneCometshard()
        self.music = "Malenia.mp3"

class Glados(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "GLaDOS"
        self.health = 3000
        self.description = "a malevolent AI antagonist, known for her dark sense of humor and penchant for testing subjects with life-threatening puzzles"
        self.attack = 20
        self.move = "Neurotoxin Gas"
        self.loot = PortalGun()
        self.music = "Glados.mp3"

class Yaldabaoth(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Yaldabaoth"
        self.health = 100
        self.description = "an imposing and god-like antagonist, representing the oppressive control and distorted order imposed upon society"
        self.attack = 15
        self.move = "Divine Punishment"
        self.loot = Megidolaon()
        self.music = "Persona_5.mp3"

class Ridley(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Ridley"
        self.health = 500
        self.description = "a fearsome space pirate leader and recurring antagonist, known for his ruthless cruelty and iconic draconic appearance"
        self.attack = 45
        self.move = "Fireball"
        self.loot = PowerSuit()

class Emil(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Emil"
        self.health = 400
        self.description = "a nightmarish and relentless foe, with multiple heads and powerful attacks"
        self.attack = 40
        self.move = "Emil Clones"
        self.loot = VirtuousTreaty()

class TheBoneHyrda(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "The Bone Hydra"
        self.health = 150
        self.description = "a fearsome and multi-headed boss, a relentless adversary that guards the underworld's entrance and challenges you with its deadly attacks."
        self.attack = 20
        self.move = "Ground Slam"
        self.loot = Coronacht()
        self.music = "Bone_Hydra.mp3"

class GeneralMugen(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "General Mugen"
        self.health = 350
        self.description = "a formidable and ruthless military leader, known for his strategic prowess and unwavering dedication to his nation's conquest"
        self.attack = 35
        self.move = "Ordained Punishment"
        self.loot = DragonMail()
        self.music = "General_Mugen.mp3"

class DoctorEggman(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Doctor Eggman"
        self.health = 200
        self.description = "a brilliant yet perpetually thwarted scientist with a penchant for constructing nefarious machines and plots to conquer the world"
        self.attack = 20
        self.move = "his Robot Army"
        self.loot = ChaosEmerald()

class TheMoonLord(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "The Moon Lord"
        self.health = 300
        self.description = "a towering eldritch entity with a menacing appearance and an array of devastating attacks that challenge you to your limits"
        self.attack = 30
        self.move = "Phantasmal Eyes"
        self.loot = Zenith()
        self.music = "Moon_Lord.mp3"

class Mithrix(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Mithrix"
        self.health = 120
        self.description = "a vengeful and godlike being with the power to manipulate time and space, posing a significant threat to whoever attempts to escape"
        self.attack = 20
        self.move = "Lunar Hammer Smash"
        self.loot = WillOTheWisp()
        self.music = "Mithrix.mp3"

class Sephiroth(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Sephiroth"
        self.health = 20
        self.description = "a brooding and immensely powerful warrior with a deep-seated desire to harness the destructive force of the planet for his own malevolent purposes"
        self.attack = 10
        self.move = "Super Nova"
        self.loot = BusterSword()
        self.music = "Sephiroth.mp3"

class Ganondorf(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Ganondorf"
        self.health = 20
        self.description = "a malevolent Gerudo sorcerer who seeks to obtain the Triforce's power and plunge Hyrule into darkness and chaos"
        self.attack = 10
        self.move = "Dark Magic"
        self.loot = MasterSword()
        self.music = "Ganondorf.mp3"

class TheEnderDragon(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "The Ender Dragon"
        self.health = 20
        self.description = "a fearsome and colossal winged creature that challenges you with its destructive abilities and formidable strength"
        self.attack = 10
        self.move = "Dragon's breath"
        self.loot = NetheriteArmour()
        self.music = "The_Ender_Dragon.mp3"

class Shibusawa(Enemy):  
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Shibusawa"
        self.health = 20
        self.description = "a ruthless and power-hungry underworld figure who manipulates events to achieve his sinister goals within the criminal landscape of Kamurocho"
        self.attack = 10
        self.move = "Beast Style"
        self.loot = DragonAmulet()
        self.music = "Shibusawa.mp3"

class Enchantress(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Enchantress"
        self.health = 20
        self.description = "a mastermind behind the Order of No Quarter, shrouded in mystery and wielding dark magic"
        self.attack = 10
        self.move = "Pyrokinetic Flames"
        self.loot = OrnatePlate()

class Freya(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Freya"
        self.health = 20
        self.description = "a formidable and relentless adversary, harnessing her powerful magic and fierce determination to protect her son, Baldur"
        self.attack = 10
        self.move = "Thamur"
        self.loot = LeviathanAxe()

class Reyna(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Reyna"
        self.health = 100
        self.description = "a deadly duelist agent with the ability to absorb the souls of defeated enemies, empowering herself to become an even more formidable threat on the battlefield"
        self.attack = 10
        self.move = "Reaver Vandal"
        self.loot = RGXButterflyKnife()

class Voldemort(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Voldemort"
        self.health = 800
        self.description = "a malevolent dark wizard, seeking power and immortality while spreading fear and chaos throughout the wizarding world"
        self.attack = 50
        self.move = "Avada Kedavra"

class Gabriel(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Gabriel, Apostate of Hate"
        self.health = 400
        self.description = "a seething red angelic crusader wielding twin swords, desperate to prove himself to the council"
        self.attack = 20
        self.move = "Sword Throw"
        self.loot = MarksmanRevolver()
        self.music = "Gabriel.mp3"

class Papyrus(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Papyrus"
        self.health = 350
        self.description = "a malevolent flower with a cunning and manipulative personality"
        self.attack = 35
        self.move = "Flamethrower"
        self.loot = ToyKnife()
        self.music = "Papyrus.mp3"

class Sans(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Sans"
        self.health = 350
        self.description = "a malevolent flower with a cunning and manipulative personality"
        self.attack = 35
        self.move = ""
        self.loot = None
        self.music = "Sans.mp3"

class TheHeir(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "The Heir"
        self.health = 400
        self.description = "a formidable and relentless opponent, putting the your combat skills to the test in a challenging battle within its enchanting yet treacherous world."
        self.attack = 40
        self.move = "Dark Energy"
        self.loot = HolyCross()

class JenaAnderson(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Jena Anderson"
        self.health = 400
        self.description = "a formidable and challenging adversary, wielding her scientific knowledge and powerful Legion to confront you in an intense battle."
        self.attack = 40
        self.move = "Legion"
        self.loot = XBaton()

class TheKraken(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "The Kraken"
        self.health = 300
        self.description = "a massive tentacled sea monster that terrorised the ill-fated crew of the ship"
        self.attack = 30
        self.move = "Tentacles"
        self.loot = MementoMortem()

class Bowser(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Bowser"
        self.health = 300
        self.description = "the king koopa with a imposing stature and fire-breathing abilities"
        self.attack = 30
        self.move = "Koopa Army"
        self.loot = Cappy()

class Sentinel(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Sentinels"
        self.health = 300
        self.description = "formidable and relentless enforcers of the oppressive regime in Walled City 99. Clad in black, with masks obscuring their faces, they are known for their cold efficiency and unwavering loyalty to the city's rulers, striking fear into the hearts of those who dare to defy them"
        self.attack = 30
        self.move = "Shocking Railgun"

class KingBoo(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "King Boo"
        self.health = 300
        self.description = "formidable and relentless enforcers of the oppressive regime in Walled City 99. Clad in black, with masks obscuring their faces, they are known for their cold efficiency and unwavering loyalty to the city's rulers, striking fear into the hearts of those who dare to defy them"
        self.attack = 30
        self.move = "Shocking Railgun"
        self.loot = VirtualBoo()

class Dio(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Dio Brando"
        self.health = 1000
        self.attack = 60
        self.move = ""

class CalamityGanon(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Calamity Ganon"
        self.health = 500
        self.attack = 50
        self.move = "Fire Axe"
        self.loot = HylianShield()

class Glados_Turret(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Turret"
        self.health = 50
        self.attack = 15
        self.move = "Resolution Pellets"
        self.loot = None

class Glados_Rocket(Enemy):
    """
    An enemey that inherits from the Enemy class
    """
    
    def __init__(self):
        super().__init__()
        self.name = "Rocket Sentry"
        self.health = 50
        self.attack = 50
        self.move = "Rocket Launcher"
        self.loot = None