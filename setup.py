# importing from other files
from Content.room import *
from Content.character import *
from Content.weapon import *
from Content.spell import *
from Content.item import *
from Content.upgrade import *
import map

def link_left(room1, room2):
    room1.left = room2
    room2.right = room1

def link_right(room1, room2):
    room1.right = room2
    room2.left = room1

def link_forward(room1, room2):
    room1.forward = room2
    room2.back = room1

def link_back(room1, room2):
    room1.back = room2
    room2.forward = room1

def setup(load=False) -> [Room, Character]:
    """
    Generates the map and the character and returns it in a list
    """

    character = Character()

    output_map = map.game_map()

    zebes = Zebes()
    kingdomOfKu = KingdomOfKu()
    bunker = Bunker()
    greenhillZone = GreenhillZone()
    theMushroomKingdom = TheMushroomKingdom()
    asphodel = Asphodel()
    commencement = Commencement()
    walledCity99 = WalledCity99()
    mementos = Mementos()
    shoresOfNine = ShoresOfNine()
    theForge = TheForge()
    midgar = Midgar()
    dirtmouth = Dirtmouth()
    theEndDimension = TheEndDimension()
    principalsOffice = PrincipalsOffice()
    hyruleKingdom = HyruleKingdom()
    celestialResort = CelestialResort()
    ascent = Ascent()
    sixthCircleOfHell = SixthCircleOfHell()
    towerOfFate = TowerOfFate()
    miquellasHaligtree = MiquellasHaligtree()
    theHallow = TheHallow()
    theObraDinn = TheObraDinn()
    kamurocho = Kamurocho()
    snowdin = Snowdin()
    theAstralPlane = TheAstralPlane()
    apertureLab = ApertureLab()
    theSealedTemple = TheSealedTemple()
    theLastResort = TheLastResort()

    enemies = {TheRadiance().get_save_name() : TheRadiance(),
               TheHollowKnight().get_save_name() : TheHollowKnight(),
               MrOshiro().get_save_name() : MrOshiro(),
               TheHighDragun().get_save_name() : TheHighDragun(),
               Malenia().get_save_name() : Malenia(),
               Glados().get_save_name() : Glados(),
               Yaldabaoth().get_save_name() : Yaldabaoth(),
               Ridley().get_save_name() : Ridley(),
               Emil().get_save_name() : Emil(),
               TheBoneHyrda().get_save_name() : TheBoneHyrda(),
               GeneralMugen().get_save_name() : GeneralMugen(),
               DoctorEggman().get_save_name() : DoctorEggman(),
               TheMoonLord().get_save_name() : TheMoonLord(),
               Mithrix().get_save_name() : Mithrix(),
               Sephiroth().get_save_name() : Sephiroth(),
               Ganondorf().get_save_name() : Ganondorf(),
               TheEnderDragon().get_save_name() : TheEnderDragon(),
               Shibusawa().get_save_name() : Shibusawa(),
               Enchantress().get_save_name() : Enchantress(),
               Freya().get_save_name() : Freya(),
               Reyna().get_save_name() : Reyna(),
               Voldemort().get_save_name() : Voldemort(),
               Gabriel().get_save_name() : Gabriel(),
               Papyrus().get_save_name() : Papyrus(),
               TheHeir().get_save_name() : TheHeir(),
               JenaAnderson().get_save_name() : JenaAnderson(),
               TheKraken().get_save_name() : TheKraken(),
               Bowser().get_save_name() : Bowser(),
               Sentinel().get_save_name() : Sentinel(),
               KingBoo().get_save_name() : KingBoo(),
               Dio().get_save_name() : Dio(),
               CalamityGanon().get_save_name() : CalamityGanon()}


    rooms = {zebes.get_save_name() : zebes, 
             kingdomOfKu.get_save_name() : kingdomOfKu, 
             bunker.get_save_name() : bunker, 
             greenhillZone.get_save_name() : greenhillZone, 
             theMushroomKingdom.get_save_name() : theMushroomKingdom, 
             asphodel.get_save_name() : asphodel, 
             commencement.get_save_name() : commencement, 
             walledCity99.get_save_name() : walledCity99, 
             mementos.get_save_name() : mementos, 
             shoresOfNine.get_save_name() : shoresOfNine, 
             theForge.get_save_name() : theForge, 
             midgar.get_save_name() : midgar, 
             dirtmouth.get_save_name() : dirtmouth, 
             theEndDimension.get_save_name() : theEndDimension, 
             principalsOffice.get_save_name() : principalsOffice, 
             hyruleKingdom.get_save_name() : hyruleKingdom, 
             celestialResort.get_save_name() : celestialResort, 
             ascent.get_save_name() : ascent, 
             sixthCircleOfHell.get_save_name() : sixthCircleOfHell, 
             towerOfFate.get_save_name() : towerOfFate, 
             miquellasHaligtree.get_save_name() : miquellasHaligtree, 
             theHallow.get_save_name() : theHallow, 
             theObraDinn.get_save_name() : theObraDinn, 
             kamurocho.get_save_name() : kamurocho, 
             snowdin.get_save_name() : snowdin, 
             theAstralPlane.get_save_name() : theAstralPlane, 
             theSealedTemple.get_save_name() : theSealedTemple,
             theLastResort.get_save_name() : theLastResort,
             apertureLab.get_save_name() : apertureLab}
    
    loots = {FlaskOfCrimsonTears().get_save_name() : FlaskOfCeruleanTears(),
             FlaskOfCeruleanTears().get_save_name() : FlaskOfCeruleanTears(),
             DectusMedallionLeft().get_save_name() : DectusMedallionLeft(),
             DectusMedallionRight().get_save_name() : DectusMedallionRight(),
             RustyKey().get_save_name() : RustyKey(),
             BlackBox().get_save_name() : BlackBox(),
             RoboticArm().get_save_name() : RoboticArm()}
    
    spells = {WingardiumLeviosa().get_save_name() : WingardiumLeviosa(),
              VengefulSpirit().get_save_name() : VengefulSpirit(),
              Megidolaon().get_save_name() : Megidolaon(),
              GlintstoneCometshard().get_save_name() : GlintstoneCometshard(),
              WillOTheWisp().get_save_name() : WillOTheWisp()}
    
    armours = {NetheriteArmour().get_save_name() : NetheriteArmour(),
               OrnatePlate().get_save_name() : OrnatePlate(),
               PowerSuit().get_save_name() : PowerSuit(),
               DragonMail().get_save_name() : DragonMail(),
               Cappy().get_save_name() : Cappy()}
    
    weapons = {BusterSword().get_save_name() : BusterSword(),
               MasterSword().get_save_name() : MasterSword(),
               LeviathanAxe().get_save_name() : LeviathanAxe(),
               VirtuousTreaty().get_save_name() : VirtuousTreaty(),
               Coronacht().get_save_name() : Coronacht(),
               Zenith().get_save_name() : Zenith(),
               RGXButterflyKnife().get_save_name() : RGXButterflyKnife(),
               Wand().get_save_name() : Wand(),
               MarksmanRevolver().get_save_name() : MarksmanRevolver(),
               ToyKnife().get_save_name() : ToyKnife(),
               XBaton().get_save_name() : XBaton()}
    
    accessories = {GoldenFeather().get_save_name() : GoldenFeather(),
                   MasterRound().get_save_name() : MasterRound(),
                   DragonAmulet().get_save_name() : DragonAmulet(),
                   ChaosEmerald().get_save_name() : ChaosEmerald(),
                   HolyCross().get_save_name() : HolyCross()}
    
    shields = {HylianShield().get_save_name() : HylianShield()}

    items = {DectusMedallionLeft().get_save_name() : DectusMedallionLeft(),
             DectusMedallionRight().get_save_name() : DectusMedallionRight(),
             RustyKey().get_save_name() : RustyKey(),
             MementoMortem().get_save_name() : MementoMortem(),
             BlackBox().get_save_name() : BlackBox(),
             ScotchWhiskey().get_save_name() : ScotchWhiskey(),
             RoboticArm().get_save_name() : RoboticArm()}
    
    upgrades = {VirtualBoo().get_save_name() : VirtualBoo(),
                PortalGun().get_save_name() : PortalGun(),
                ShadeCloak().get_save_name() : ShadeCloak(),
                SmokeBombs().get_save_name() : SmokeBombs()}
    
    shops = {ScotchWhiskey().get_save_name() : ScotchWhiskey(),
             SmokeBombs().get_save_name() : SmokeBombs()}

    output_rooms = []
    secret_passage = False

    if load:
        with open("save.txt", "r") as f:
            out = f.readlines()
            current_room = out[2].split()[1]
            visited_rooms = out[4].split()
            character_stats = [x.split() for x in out[8:34]]
            all_rooms  = []
            for i in range(29):
                all_rooms.append([out[35+i*6].strip(), out[37+i*6].split()[1], out[38+i*6].split()[1], out[39+i*6].split()[1]])

        for room in visited_rooms[1:]:
            output_rooms.append(rooms[room])

        all_room_names = []

        for room in all_rooms:
            all_room_names.append(room[0])
    
        for name in visited_rooms[1:]:
            
            room = all_rooms[all_room_names.index(name)]

            if room[1] == "None":
                rooms[room[0]].enemy = None
            else:
                rooms[room[0]].enemy = enemies[room[1]]

            if room[2] == "None":
                rooms[room[0]].loot = None
            else:
                rooms[room[0]].loot = loots[room[2]]

            if room[3] == "True":
                rooms[room[0]].secret = True
            else:
                rooms[room[0]].secret = False

            if room[0] == "WalledCity99" and room[3] == "False":
                secret_passage = True
                output_map.meow_reveal()

            if rooms[room[0]].name == "Dirtmouth":
                output_map.dirtmouth_enter()
            elif rooms[room[0]].name == "Celestial Resort":
                output_map.celestial_resort_enter()
            elif rooms[room[0]].name == "The Forge":
                output_map.forge_enter()
            elif rooms[room[0]].name == "Miquella's Haligtree":
                output_map.haligtree_enter()
            elif rooms[room[0]].name == "Aperture Lab":
                output_map.aperture_enter()
            elif rooms[room[0]].name == "Zebes":
                output_map.zebes_enter()
            elif rooms[room[0]].name == "Bunker":
                output_map.bunker_enter()
            elif rooms[room[0]].name == "Asphodel":
                output_map.asphodel_enter()
            elif rooms[room[0]].name == "Kingdom of Ku":
                output_map.kingdom_ku_enter()
            elif rooms[room[0]].name == "Greenhill Zone":
                output_map.greenhill_enter()
            elif rooms[room[0]].name == "The Hallow":
                output_map.hallow_enter()
            elif rooms[room[0]].name == "Commencement":
                output_map.commencement_enter()
            elif rooms[room[0]].name == "Midgar":
                output_map.midgar_enter()
            elif rooms[room[0]].name == "Hyrule Kingdom":
                output_map.hyrule_enter()
            elif rooms[room[0]].name == "The End Dimension":
                output_map.end_dimension_enter()
            elif rooms[room[0]].name == "Kamurocho":
                output_map.kamurocho_enter()
            elif rooms[room[0]].name == "Tower of Fate":
                output_map.tower_enter()
            elif rooms[room[0]].name == "Shores of Nine":
                output_map.shores_enter()
            elif rooms[room[0]].name == "Mementos":
                output_map.mementos_enter()
            elif rooms[room[0]].name == "Ascent":
                output_map.ascent_enter()
            elif rooms[room[0]].name == "The Shrieking Shack":
                output_map.office_enter()
            elif rooms[room[0]].name == "6th Circle of Hell":
                output_map.sixth_circle_enter()
            elif rooms[room[0]].name == "Snowdin":
                output_map.snowdin_enter()
            elif rooms[room[0]].name == "The Sealed Temple":
                output_map.sealed_temple_enter()
            elif rooms[room[0]].name == "The Astral Plane":
                output_map.astral_plane_enter()
            elif rooms[room[0]].name == "The Obra Dinn":
                output_map.obradinn_enter()
            elif rooms[room[0]].name == "The Mushroom Kingdom":
                output_map.mushroom_enter()
            elif rooms[room[0]].name == "Walled City 99":
                output_map.walled_enter()
            elif rooms[room[0]].name == "The Last Resort":
                output_map.last_resort_enter()
        
            if room[1] == "None" and room[2] == "None" and room[3] == "False":
                if rooms[room[0]].name == "Dirtmouth":
                    output_map.dirtmouth_clear()
                elif rooms[room[0]].name == "Celestial Resort":
                    output_map.celestial_resort_clear()
                elif rooms[room[0]].name == "The Forge":
                    output_map.forge_clear()
                elif rooms[room[0]].name == "Miquella's Haligtree":
                    output_map.haligtree_clear()
                elif rooms[room[0]].name == "Aperture Lab":
                    output_map.aperture_clear()
                elif rooms[room[0]].name == "Zebes":
                    output_map.zebes_clear()
                elif rooms[room[0]].name == "Bunker":
                    output_map.bunker_clear()
                elif rooms[room[0]].name == "Asphodel":
                    output_map.asphodel_clear()
                elif rooms[room[0]].name == "Kingdom of Ku":
                    output_map.kingdom_ku_clear()
                elif rooms[room[0]].name == "Greenhill Zone":
                    output_map.greenhill_clear()
                elif rooms[room[0]].name == "The Hallow":
                    output_map.hallow_clear()
                elif rooms[room[0]].name == "Commencement":
                    output_map.commencement_clear()
                elif rooms[room[0]].name == "Midgar":
                    output_map.midgar_clear()
                elif rooms[room[0]].name == "Hyrule Kingdom":
                    output_map.hyrule_clear()
                elif rooms[room[0]].name == "The End Dimension":
                    output_map.end_dimension_clear()
                elif rooms[room[0]].name == "Kamurocho":
                    output_map.kamurocho_clear()
                elif rooms[room[0]].name == "Tower of Fate":
                    output_map.tower_clear()
                elif rooms[room[0]].name == "Shores of Nine":
                    output_map.shores_clear()
                elif rooms[room[0]].name == "Mementos":
                    output_map.mementos_clear()
                elif rooms[room[0]].name == "Ascent":
                    output_map.ascent_clear()
                elif rooms[room[0]].name == "The Shrieking Shack":
                    output_map.office_clear()
                elif rooms[room[0]].name == "6th Circle of Hell":
                    output_map.sixth_circle_clear()
                elif rooms[room[0]].name == "Snowdin":
                    output_map.snowdin_clear()
                elif rooms[room[0]].name == "The Sealed Temple":
                    output_map.sealed_temple_clear()
                elif rooms[room[0]].name == "The Astral Plane":
                    output_map.astral_plane_clear()
                elif rooms[room[0]].name == "The Obra Dinn":
                    output_map.obradinn_clear()
                elif rooms[room[0]].name == "The Mushroom Kingdom":
                    output_map.mushroom_clear()
                elif rooms[room[0]].name == "Walled City 99":
                    output_map.walled_clear()
                elif rooms[room[0]].name == "The Last Resort":
                    output_map.last_resort_clear()
        
    link_forward(walledCity99, commencement)
    link_right(commencement, asphodel)
    link_back(asphodel, greenhillZone)
    link_right(greenhillZone, theMushroomKingdom)
    link_back(greenhillZone, kingdomOfKu)
    link_left(kingdomOfKu, bunker)
    link_right(kingdomOfKu, zebes)
    link_right(asphodel, mementos)
    link_forward(mementos, shoresOfNine)
    link_back(mementos, theForge)
    link_right(theForge, midgar)
    link_right(midgar, dirtmouth)
    link_forward(dirtmouth, theEndDimension)
    link_forward(theEndDimension, principalsOffice)
    link_right(dirtmouth, hyruleKingdom)
    link_back(hyruleKingdom, celestialResort)
    link_back(celestialResort, sixthCircleOfHell)
    link_right(sixthCircleOfHell, ascent)
    link_forward(ascent, towerOfFate)
    link_right(ascent, miquellasHaligtree)
    link_forward(miquellasHaligtree, theHallow)
    link_forward(theHallow, theObraDinn)
    link_back(miquellasHaligtree, kamurocho)
    link_left(kamurocho, snowdin)
    link_left(snowdin, apertureLab)
    link_forward(snowdin, theAstralPlane)
    link_back(snowdin, theSealedTemple) 
    if secret_passage:
        link_back(walledCity99, theLastResort)

    # Sets the default statistics of the character
    if load:
        for info in character_stats:
            name = info[0]
            stat = info[1:]

            if name == "name":
                character.name = stat[0]

            elif name in ["health", "max_health", "attack", "mana", "max_mana", "defence", "health_flask", "mana_flask", "money", "completion"]:
                setattr(character, name, int(stat[0]))

            elif name == "spells":
                temp = []
                if stat[0] != "None":
                    for spell in stat:
                        temp.append(spells[spell])
                character.spells = temp

            elif name == "armour":
                if stat[0] == "None":
                    character.armour = None
                else:
                    character.armour = armours[stat[0]]

            elif name == "armours":
                temp = []
                if stat[0] != "None":
                    for armour in stat:
                        temp.append(armours[armour])
                character.armours = temp
            
            elif name == "weapon":
                if stat[0] == "None":
                    character.weapon = None
                else:
                    character.weapon = weapons[stat[0]]

            elif name == "weapons":
                temp = []
                if stat[0] != "None":
                    for weapon in stat:
                        temp.append(weapons[weapon])
                character.weapons = temp

            elif name == "accessory":
                if stat[0] == "None":
                    character.accessory = None
                else:
                    character.accessory = accessories[stat[0]]

            elif name == "accessories":
                temp = []
                if stat[0] != "None":
                    for accessory in stat:
                        temp.append(accessories[accessory])
                character.accessories = temp

            elif name == "shield":
                if stat[0] == "None":
                    character.shield = None
                else:
                    character.shield = shields[stat[0]]

            elif name == "shields":
                temp = []
                if stat[0] != "None":
                    for shield in stat:
                        temp.append(shields[shield])
                character.shields = temp

            elif name == "items":
                temp = []
                if stat[0] != "None":
                    for item in stat:
                        temp.append(items[item])
                character.items = temp

            elif name == "upgrades":
                temp = []
                if stat[0] != "None":
                    for upgrade in stat:
                        temp.append(upgrades[upgrade])
                character.upgrades = temp

            elif name == "shop_inventory":
                temp = []
                if stat[0] != "None":
                    for item in stat:
                        temp.append(shops[item])
                character.shop_inventory = temp

            elif name in ["shop", "additional_shop", "gamble"]:
                if stat [0] == "True":
                    setattr(character, name, True)
                else:
                    setattr(character, name, False)
        if character.additional_shop:
            theForge.secret_message = "You notice that Ox is missing his left arm"
            
    else:
        character.spells.append(WingardiumLeviosa())
        character.weapon = Wand()
        character.weapons.append(character.weapon)
        character.health = 100
        character.max_health = 100
        character.mana = 50
        character.max_mana = 50
        character.health_flask = 2
        character.mana_flask = 2
    
    if load:
        return [rooms[current_room], character, output_rooms, output_map]
    else:
        return [dirtmouth, character, output_rooms, output_map]