#import from python built in libraries
import time
import random

#import from other files
from setup import *
import tkinter as tk
import map

temp = setup()
selfend = False
selfroom = temp[0]
selfcharacter = temp[1]
selfrooms = []
selfactions = ["look", "move", "loot", "flask", "attack", "equip", "status", "info", "die", "settings", "map", "meow"]
selfdescription = ["Looks around the room","Move to another room", "Search the room for loot", "Drink your flasks", "Attack the enemny", "Change your equipment", "See your statistics", "Find out more about your items", "Ends the game", "Change settings", "Shows map", "Meow"]
selfteleportable = False
selfmap = map.game_map()
currentPressedKey = ""
out = []
with open("settings.txt", "r") as f:
    out = f.readlines()
    out = [x.split()[1] for x in out]
selfsleep = int(out[0])

def sleep(t):
    root.after(int(t*1000), lambda: sleepCount.set(sleepCount.get()+1))
    root.wait_variable(sleepCount)
def write(txt=""):
    text['state'] = 'normal'
    text.insert(tk.END, txt+"\n")
    text['state'] = 'disabled'

def delete():
    text['state'] = 'normal'
    text.delete("1.0", tk.END)
    text['state'] = 'disabled'
def start_typing(e):
    text['state'] = 'normal'
    data = text.get("1.0",'end-1c')
    if e.keysym == "BackSpace":
        if data != 'Tarnished, key in your name: ':
            text.delete('end-2c','end-1c')
    else:
        text.insert(tk.END, e.char)
    text['state'] = 'disabled'


def intro():
    """print introduction for the start of the game """
    
    # Displays the introduction messages
    write('Welcome to Hogwarts School of Witchcraft and Wizardry')
    sleep(selfsleep)
    write("\nThe Dark Lord Voldemort has taken over Hogwarts and opened multiple interdimensional gates, bringing hordes of enemies into the school. Your job as the chosen one is to traverse the school in order to locate The Shrieking Shack and thwart Voldemort's evil plan to take over the world.\n")
    sleep(selfsleep)
    write('Do you wish to enter the school?')
    write('[y] Yes')
    write('[n] No')
    root.bind('<y>', lambda x: pause_var.set("yes"))
    root.bind("<n>", lambda x: pause_var.set("no"))
    root.wait_variable(pause_var)
    decision = pause_var.get()
    root.unbind('<y>')
    root.unbind('<n>')
    delete()
    pause_var.set("")
    
    if decision.lower() == "yes":
        text['state'] = 'normal'
        text.insert(tk.END, "Tarnished, key in your name: ")
        text['state'] = 'disabled'
        text.bind('<Key>', start_typing)
        root.bind('<Return>', lambda x: pause_var.set("done"))
        root.wait_variable(pause_var)
        root.unbind('<Return>')
        text.unbind('<Key>')
        pause_var.set("")
        name = text.get("1.0",'end-1c')[29:]
        delete()
        selfcharacter.name = name
        # Check if the user used the secret easter egg name
        if name == "meow":
            secret()
        else:
            write("You boldly opened the front gates of the school and made your way into the first room\n")
            root.after(selfsleep*1000, run)
            
    elif decision.lower() == "no":
        write("Due to your utter cowardice, voldemort continued to gain power, spreading his control and chaos all over the world, leading to the complete annihilation of the human race.")
        sleep(selfsleep)
        end_game()
        return
    else:
        write("Due to your indecision, voldemort continued to gain power, spreading his control and chaos all over the world, leading to the complete annihlation of the human race.")
        sleep(selfsleep)
        end_game()
        return

def wait_for_key_press():
    write("\nPress any key to continue")
    root.bind('<Key>', lambda x: pause_var.set("done"))
    root.wait_variable(pause_var)
    root.unbind('<Key>')
    pause_var.set("")
    
def show(prompt, options, deletebefore):
    data = text.get("1.0",'end-1c')
    delete()
    keep = ""
    if not deletebefore:
        keep = data.split(prompt)[0]
        
    """main action for user to get the list of possible actions"""
    # Displays the list of actions the user can do
    p = pointer.get()
    write(keep+prompt+"\n")
    for i, e in enumerate(options):
        arrow = " "
        if p == i: arrow = ">"
        write(f"{arrow} {e}")
        
def up_action(prompt, options, delete):
    p = pointer.get()
    if p != 0:
        pointer.set(p-1)
    else:
        pointer.set(len(options)-1)

    show(prompt, options, delete)
def down_action(prompt, options, delete):
    p = pointer.get()
    if p != len(options)-1:
        pointer.set(p+1)
    else:
        pointer.set(0)

    show(prompt, options, delete)
def get_input(prompt, options, displayoptions = None, deletebefore = True):
    """sub action for run() that prompts user for a main action"""
    if displayoptions is None:
        displayoptions = options
    show(prompt, displayoptions, deletebefore)
    root.bind('<Return>', lambda x: pause_var.set("done"))
    root.bind('<Up>', lambda e: up_action(prompt, displayoptions, deletebefore))
    root.bind('<Down>', lambda e: down_action(prompt, displayoptions, deletebefore))
    root.wait_variable(pause_var)
    root.unbind('<Return>')
    root.unbind('<Up>')
    root.unbind('<Down>')
    pause_var.set("")
    decision = options[pointer.get()]
    pointer.set(0)
    delete()
    return decision

        
def run():
    global selfroom
    global selfend
    delete()
    """to be run in a loop to prompt user's action"""
    display_room_name()
    # Checks if the player has entered the room before
    if not selfroom.been_here:
        # Displays a description of the room if the player has not been there before
        display_room_description()
        selfrooms.append(selfroom)
        
        if selfroom.name == "Dirtmouth":
            selfmap.dirtmouth_enter()
        elif selfroom.name == "Celestial Resort":
            selfmap.celestial_resort_enter()
        elif selfroom.name == "The Forge":
            selfmap.forge_enter()
        elif selfroom.name == "Stormveil Castle":
            selfmap.stormveil_enter()
        elif selfroom.name == "Aperture Lab":
            selfmap.aperture_enter()
        elif selfroom.name == "Zebes":
            selfmap.zebes_enter()
        elif selfroom.name == "Bunker":
            selfmap.bunker_enter()
        elif selfroom.name == "Asphodel":
            selfmap.asphodel_enter()
        elif selfroom.name == "Kingdom of Ku":
            selfmap.kingdom_ku_enter()
        elif selfroom.name == "Greenhill Zone":
            selfmap.greenhill_enter()
        elif selfroom.name == "The Hallow":
            selfmap.hallow_enter()
        elif selfroom.name == "Commencement":
            selfmap.commencement_enter()
        elif selfroom.name == "Midgar":
            selfmap.midgar_enter()
        elif selfroom.name == "Hyrule Kingdom":
            selfmap.hyrule_enter()
        elif selfroom.name == "The End Dimension":
            selfmap.end_dimension_enter()
        elif selfroom.name == "Kamurocho":
            selfmap.kamurocho_enter()
        elif selfroom.name == "Tower of Fate":
            selfmap.tower_enter()
        elif selfroom.name == "Shores of Nine":
            selfmap.shores_enter()
        elif selfroom.name == "Mementos":
            selfmap.mementos_enter()
        elif selfroom.name == "Ascent":
            selfmap.ascent_enter()
        elif selfroom.name == "The Shrieking Shack":
            selfmap.shrieking_enter()
        elif selfroom.name == "6th Circle of Hell":
            selfmap.sixth_circle_enter()
        elif selfroom.name == "Snowdin":
            selfmap.snowdin_enter()
        elif selfroom.name == "The Sealed Temple":
            selfmap.sealed_temple_enter()
        elif selfroom.name == "The Astral Plane":
            selfmap.astral_plane_enter()
        elif selfroom.name == "The Obra Dinn":
            selfmap.obradinn_enter()
        elif selfroom.name == "The Mushroom Kingdom":
            selfmap.mushroom_enter()
        elif selfroom.name == "Walled City 99":
            selfmap.walled_enter()
        elif selfroom.name == "The Last Resort":
            selfmap.last_resort_enter()
    
    decision = get_input("What do you wish to do?", selfactions, ["{} ({})".format(a,b) for a,b in zip(selfactions, selfdescription)])

    # Does the action the user selected

    if decision.lower() == "look":
        look(selfroom)
        
    elif decision.lower() == "move":
        move(selfroom)
        
    elif decision.lower() == "attack":
        attack(selfcharacter, selfroom.enemy)

    elif decision.lower() == "loot":
        loot(selfcharacter, selfroom.loot)

    elif decision.lower() == "flask":
        flask(selfcharacter)

    elif decision.lower() == "equip":
        equip(selfcharacter)

    elif decision.lower() == "status":
        status(selfcharacter)

    elif decision.lower() == "info":
        info(selfcharacter)

    elif decision.lower() == "die":
        die()

    elif decision.lower() == "meow":
        meow()

    elif decision.lower() == "settings":
        settings()

    elif selfteleportable == True and decision.lower() == "teleport":
        teleport()

    elif decision.lower() == "map":
        display_map()

    if selfroom.enemy == None and selfroom.loot == None:
        if selfroom.name == "Dirtmouth":
            selfmap.dirtmouth_clear()
        elif selfroom.name == "Celestial Resort":
            selfmap.celestial_resort_clear()
        elif selfroom.name == "The Forge":
            selfmap.forge_clear()
        elif selfroom.name == "Stormveil Castle":
            selfmap.stormveil_clear()
        elif selfroom.name == "Aperture Lab":
            selfmap.aperture_clear()
        elif selfroom.name == "Zebes":
            selfmap.zebes_clear()
        elif selfroom.name == "Bunker":
            selfmap.bunker_clear()
        elif selfroom.name == "Asphodel":
            selfmap.asphodel_clear()
        elif selfroom.name == "Kingdom of Ku":
            selfmap.kingdom_ku_clear()
        elif selfroom.name == "Greenhill Zone":
            selfmap.greenhill_clear()
        elif selfroom.name == "The Hallow":
            selfmap.hallow_clear()
        elif selfroom.name == "Commencement":
            selfmap.commencement_clear()
        elif selfroom.name == "Midgar":
            selfmap.midgar_clear()
        elif selfroom.name == "Hyrule Kingdom":
            selfmap.hyrule_clear()
        elif selfroom.name == "The End Dimension":
            selfmap.end_dimension_clear()
        elif selfroom.name == "Kamurocho":
            selfmap.kamurocho_clear()
        elif selfroom.name == "Tower of Fate":
            selfmap.tower_clear()
        elif selfroom.name == "Shores of Nine":
            selfmap.shores_clear()
        elif selfroom.name == "Mementos":
            selfmap.mementos_clear()
        elif selfroom.name == "Ascent":
            selfmap.ascent_clear()
        elif selfroom.name == "The Shrieking Shack":
            selfmap.shrieking_clear()
        elif selfroom.name == "6th Circle of Hell":
            selfmap.sixth_circle_clear()
        elif selfroom.name == "Snowdin":
            selfmap.snowdin_clear()
        elif selfroom.name == "The Sealed Temple":
            selfmap.sealed_temple_clear()
        elif selfroom.name == "The Astral Plane":
            selfmap.astral_plane_clear()
        elif selfroom.name == "The Obra Dinn":
            selfmap.obradinn_clear()
        elif selfroom.name == "The Mushroom Kingdom":
            selfmap.mushroom_clear()
        elif selfroom.name == "Walled City 99":
            selfmap.walled_clear()
        elif selfroom.name == "The Last Resort":
            selfmap.last_resort_clear()
    if not selfend:
        root.after(1,run)
        

        
def look(room):
    """main action to look around the room including rooms linked to the room and enemies in the room"""
    write()

    # Displays the connected rooms
    if room.left != None:
        write(f"To the left is {room.left.name}")
        
    if room.right != None:
        write(f"To the right is {room.right.name}")
        
    if room.forward != None:
        write(f"In front of you is {room.forward.name}")
        
    if room.back != None:
        write(f"Behind you is {room.back.name}")

    sleep(selfsleep)
    upgrades = selfcharacter.get_upgrades()

    if "Virtual Boo" in upgrades:
        if room.enemy != None:
            write(f"\nIn the middle of the room is {room.enemy.name}, {room.enemy.description}")
            sleep(selfsleep)
            write(f"\n{room.enemy.name} has {room.enemy.health} health")
            sleep(selfsleep)
        if room.loot != None:
            write(f"\nThere is {room.loot.name} hidden in {room.name}")
            sleep(selfsleep)
        else:
            write(f"\nThere is no loot hidden in {room.name}")
            sleep(selfsleep)
        
    elif room.enemy != None:
    # Displays the enemy in the room
        write(f"\nIn the middle of the room is {room.enemy.name}, {room.enemy.description}")
    wait_for_key_press()

def move(room):
    global selfroom
    """main action for user to traverse from one room to another"""
    movement = get_input('Which direction do you wish to move in?', ['left', 'right', 'forward','back'])

    # Generate a random number to see if you managed to sneak past the enemy
    caught = False

    if selfcharacter.name == "meow":
        chance = 2
    else:
        chance = random.randint(1, 3)
        
    if room.enemy != None:
        if chance == 1:
            caught = True
        else:
            write(f"\nYou managed to sneak past {room.enemy.name}")
            sleep(selfsleep)

    if not caught:
        if movement.lower() == "left":
            if room.left == None:
                write("\nYou walked to the left and smashed into a wall")
                sleep(selfsleep)

            else:
                selfroom = room.left

        if movement.lower() == "right":
            if room.right == None:
                write("\nYou walked to the right and smashed into a wall")
                sleep(selfsleep)
            else:
                selfroom = room.right

        if movement.lower() == "forward":
            if room.forward == None:
                write("\nYou walked forward and smashed into a wall")
                sleep(selfsleep)
            # Check if you are going to the final boss room
            elif room.forward.name == "The Shrieking Shack":
                items = selfcharacter.get_items()
                # Checks if you have the required items to enter the final boss room
                if "Dectus Medallion (right)" in items and "Dectus Medallion (left)" in items:
                    write("\nCongratulations, you placed the two Dectus Medallions together releasing trememndous amounts of energy, breaking the powerful spell on the door")
                    sleep(selfsleep)
                    selfroom = room.forward
                else:
                    write("\nYou tried entering the The Shrieking Shack but the door was locked by a powerful spell")
                    sleep(selfsleep)
                    write("\nYou probably need to find a special item to break the spell (remember to loot all the rooms)")
                    sleep(selfsleep)
            else:
                selfroom = room.forward

        if movement.lower() == "back":
            if room.back == None:
                write("\nYou turned back and smashed into a wall")
                sleep(selfsleep)
            else:
                selfroom = room.back

    else:
        write(f"\nYou tried to sneak to another room but {room.enemy.name} noticed you")
        sleep(selfsleep)
        attack(selfcharacter, room.enemy)

def loot(user, loot):
    """main action for user to search the room for loot"""

    # Generate a random number to see if you successfully loot the room whithout the enemy noticing
    caught = False

    if user.name == "meow":
        chance = 1
    else:
        chance = random.randint(1, 3)

    if selfroom.enemy != None:
        if chance != 1:
            caught = True
        else:
            write(f"\nBy some miracle you managed to loot the room without {selfroom.enemy.name} noticing")
            
            sleep(selfsleep)

    if not caught:
        # Allow the user to loot the room
        if loot == None:
            write("\nYou searched every nook and cranny but there was nothing to be found")
            sleep(selfsleep)
        
        elif loot.name == "Flask of Crimson Tears":
            write(f"\nYou found a {loot.name}, a powerful flask")
            sleep(selfsleep)
            user.health_flask += 1
            selfroom.loot = None

        elif loot.name == "Flask of Cerulean Tears":
            write(f"\nYou found a {loot.name}, a powerful flask")
            sleep(selfsleep)
            user.mana_flask += 1
            selfroom.loot = None
            
        elif loot.name == "Dectus Medallion (right)":
            write(f"\nYou found a {loot.name}, a powerful item")
            sleep(selfsleep)
            user.items.append(loot)
            selfroom.loot = None

        elif loot.name == "Dectus Medallion (left)":
            write(f"\nYou found a {loot.name}, a powerful item")
            sleep(selfsleep)
            user.items.append(loot)
            selfroom.loot = None

    else:
        write(f"\n{selfroom.enemy.name} noticed you while you tried to loot the room")
        sleep(selfsleep)
        attack(user, selfroom.enemy)

def flask(user):
    """main action for user to drink their flasks"""
    # Check if the user still has available flasks
    if (user.health_flask + user.mana_flask) == 0:
        write("\nYou ran out of flasks\n")
        sleep(selfsleep)
    else:
        use_flask(user)

def attack(attacker, victim):
    """main action for user to attack the enemy in the room"""
    # Check if there is an enemy in the room
    if victim == None:
        write("\nYou attacked the air and realised how insane you looked")
        sleep(selfsleep)
    else:
        while attacker.health > 0:
            # Display users health and mana
            write(f"\n{'-'*50}\n")
            write(f"{attacker.name} has {attacker.health} health")
            write(f"{attacker.name} has {attacker.mana} mana")
            write(f"{attacker.name} has {attacker.health_flask} Flask of Crimson Tears")
            write(f"{attacker.name} has {attacker.mana_flask} Flask of Cerulean Tears")
            sleep(selfsleep)
            # Display enemy's health
            write(f"\n{victim.name} has {victim.health} health\n")
            sleep(selfsleep)

            decision = get_choice(attacker).lower()
            
            if decision == "flask":
                use_flask_battle(attacker)
                if victim.health > 0:
                    damage = max(1, victim.attack - attacker.defence)
                    attacker.health = attacker.health - damage
                    write(f"\n{victim.name} used {victim.move}, dealing {damage} damage to {attacker.name}")
                    sleep(selfsleep)
                
            else:
                damage, weapon = get_attack(attacker, decision)

                # Deal damage to enemy
                damage += attacker.attack
                victim.health = victim.health - damage
                # Check if enemy died
                if victim.health > 0:
                    write(f"\n{attacker.name}{weapon.move}, dealing {damage} damage to {victim.name}")
                    sleep(selfsleep)
                # Allow enemy to attack if it didn't die yet
                if victim.health > 0:
                    damage = max(1, victim.attack - attacker.defence)
                    attacker.health = attacker.health - damage
                    write(f"\n{victim.name} used {victim.move}, dealing {damage} damage to {attacker.name}")
                    sleep(selfsleep)

                else:
                    # Check if dead enemy is the final boss
                    if victim.name == "Voldemort":
                        write("\nInsert transition to second phase or alternate enemy")
                        sleep(selfsleep)
                        selfroom.enemy = Phase2()
                        attack(attacker, selfroom.enemy)
                        return
                    elif victim.name == "Phase 2":
                        win(weapon)
                        return

                    write(f"\n{attacker.name}{weapon.win_front}{victim.name}{weapon.win_back}")
                    sleep(selfsleep)
                    if victim.name == "Sentinels":
                        secret_room()
                        selfroom.enemy = None
                        return
                    write(f"\n{victim.name} dropped a {victim.loot.name}")
                    sleep(selfsleep)
                    choice = get_input(f"\nDo you want to pick {victim.loot.name}?",["yes","no"])
                    if choice.lower() == "yes":
                        collect_loot(attacker, victim.loot)
                        sleep(selfsleep)
                        write(f"\n{victim.loot.description}")
                        sleep(selfsleep)

                    elif choice.lower() == "no":
                        write(f"\nYou left {victim.loot.name} on the ground and allowed the resourceful rat to steal it")
                        sleep(selfsleep)
                    else:
                        write(f"\nYour indecisiveness allowed the resourceful rat to steal the {victim.loot.name} when you weren't looking")
                        sleep(selfsleep)
                    wait_for_key_press()
                    # Removes the enemy from the room
                    selfroom.enemy = None
                    break
        # Check if the user died
        if attacker.health <= 0:
            end_game()

def get_choice(user):
    """sub action from attack() to prompt user for attack methods or use of flask"""
    cost = []
    for spell in user.spells:
        cost.append(spell.cost)
    valid = False
    while not valid:
        decision = get_input(f"What do you want to use?", [f"{user.weapon.name}", "Spell", "Flask"], None, False)

        # Get a list of spell cost

        valid = True
        if decision.lower() not in [user.weapon.name.lower(), "spell", "flask"]:
            write(f"\nYou tried to use {decision} but nothing happened")
            valid = False
        # Check if user has enough mana to cast spells
        elif decision.lower() == "spell" and user.mana < min(cost):
            write("\nYou do not have enough mana to cast spells\n")
            valid = False
        # Check if user has any flask to drink
        elif decision.lower() == "flask" and (user.health_flask + user.mana_flask) == 0:
            write("\nYou ran out of flasks\n")
            valid = False
    return decision
    
def get_attack(user, decision):
    """sub action from attack() to get total damage done to victim"""

    # Check if user used his weapon
    if decision.lower() == user.weapon.name.lower():
        return user.weapon.attack, user.weapon

    # check if user used spells
    elif decision.lower() == "spell":
        spells = []
        for spell in user.spells:
            spells.append(spell.name.lower())
        choice = get_input("\nWhich spell would you like to cast?",spells, [f"{x.name} ({x.cost} mana)" for x in user.spells])
        choice = choice.lower()
        cost = user.spells[spells.index(choice)].cost
        write(f"\nYou used up {cost} mana points")
        sleep(selfsleep)
        user.mana = user.mana - cost
        return user.spells[spells.index(choice)].attack, user.spells[spells.index(choice)]

def display_flask(user):
    """sub action from use_flask to display flask in inventory"""
    out = []
    out.append(f"Flask of Crimson Tears ({user.health_flask}) (restores {FlaskOfCrimsonTears().health} health)")
    out.append(f"Flask of Cerulean Tears ({user.mana_flask}) (restores {FlaskOfCeruleanTears().mana} mana)\n")
    return out
    
def use_flask_battle(user):
    """sub action from get_choice() to prompt user for the flask to drink"""
    valid = False
    while not valid:
        selection = get_input("Which flask would you like to drink?", ["flask of crimson tears", "flask of cerulean tears"], display_flask(user))
        valid = True
        if selection.lower() == "flask of crimson tears" and user.health_flask == 0:
            write("\nYou ran out of Flask of Crimson Tears\n")
            sleep(selfsleep)
            valid = False
        # Checks if the user has enough flask of cerulean tears
        elif selection.lower() == "flask of cerulean tears" and user.mana_flask == 0:
            write("\nYou ran out of Flask of Cerulean Tears\n")
            sleep(selfsleep)
            valid = False

    if selection.lower() == "flask of crimson tears":
        # Makes sure the health healed does not exceed the maximum health
        final_health = min(user.max_health, user.health + FlaskOfCrimsonTears().health)
        healing = final_health - user.health
        write(f"\nYou drank a Flask of Crimson Tears and gained {healing} health")
        sleep(selfsleep)
        user.health = final_health
        user.health_flask -= 1
        
    elif selection.lower() == "flask of cerulean tears":
        # Makes sure the mana gained does not exceed the maximum mana
        final_mana = min(user.max_mana, user.mana + FlaskOfCeruleanTears().mana)
        healing = final_mana - user.mana
        write(f"\nYou drank a Flask of Cerulean Tears and gained {healing} mana")
        sleep(selfsleep)
        user.mana = final_mana
        user.mana_flask -= 1
                
def use_flask(user):
    """Function to allow the user to use flask but also allows them to cancel the action"""
    display_flask(user)
    selection = input("Which flask would you like to drink? (type cancel to quit): ")
    valid = False
    while not valid:
        valid = True
        # Validates user selection
        if selection.lower() not in ["flask of crimson tears", "flask of cerulean tears", "cancel"]:
            write(f"\nYou tried drinking {selection} but nothing happened\n")
            sleep(selfsleep)
            selection = input("Which flask would you like to drink?: ")
            valid = False
        # Checks if the user has enough flask of crimson tears
        elif selection.lower() == "flask of crimson tears" and user.health_flask == 0:
            write("\nYou ran out of Flask of Crimson Tears\n")
            sleep(selfsleep)
            selection = input("Which flask would you like to drink?: ")
            valid = False
        # Checks if the user has enough flask of cerulean tears
        elif selection.lower() == "flask of cerulean tears" and user.mana_flask == 0:
            write("\nYou ran out of Flask of Cerulean Tears\n")
            sleep(selfsleep)
            selection = input("Which flask would you like to drink?: ")
            valid = False

        elif selection.lower() == "cancel":
            return

    if selection.lower() == "flask of crimson tears":
        # Makes sure the health healed does not exceed the maximum health
        final_health = min(user.max_health, user.health + FlaskOfCrimsonTears().health)
        healing = final_health - user.health
        write(f"\nYou drank a Flask of Crimson Tears and gained {healing} health")
        sleep(selfsleep)
        user.health = final_health
        user.health_flask -= 1
        
    elif selection.lower() == "flask of cerulean tears":
        # Makes sure the mana gained does not exceed the maximum mana
        final_mana = min(user.max_mana, user.mana + FlaskOfCeruleanTears().mana)
        healing = final_mana - user.mana
        write(f"\nYou drank a Flask of Cerulean Tears and gained {healing} mana")
        sleep(selfsleep)
        user.mana = final_mana
        user.mana_flask -= 1
    
        
def equip(self):
    """main action for user to equip various items"""

    display_equipment(user)

    decision = input("\ndo you want to change your equipment? ( yes / no ): ")

    while decision.lower() not in ["yes", "no"]:
        write("You briefly ponder the heavily nuanced and deeply intricate question of a choice between yes and no.")
        sleep(selfsleep)
        decision = input("\ndo you want to change your equipment? ( yes / no ): ")

    if decision.lower() == "no":
        return

    elif decision.lower() == "yes":
        choice = ""
        while choice != "finish":
            choice = input("\nwhat do you want to change? (type finish to quit): ")
            while choice.lower() not in ["armour", "weapon", "accessory", "finish"]:
                write(f"\nYou tried changing your {choice} but nothing happened")
                choice = input("\nwhat do you want to change? (type finish to quit): ")

            if choice.lower() == "armour":
                equip_armour(user)

            elif choice.lower() == "weapon":
                equip_weapon(user)

            elif choice.lower() == "accessory":
                equip_accessory(user)
    
def display_equipment(user):
    """sub action for equip() to display equipments that the user have"""
    
    if user.armour == None:
        write("\nArmour : Empty")
    else:
        write(f"\nArmour : {user.armour.name}")

    if user.weapon == None:
        write("Weapon : Empty")
    else:
        write(f"Weapon : {user.weapon.name}")

    if user.accessory == None:
        write("Accessory : Empty")
    else:
        write(f"Accessory : {user.accessory.name}")
    sleep(selfsleep)



def equip_armour(user):
    """sub action from equip() for user to choose an armour to equip"""
    if len(user.armours) == 0:
        write("\nYou do not have any armour to equip")
        sleep(selfsleep)
    else:
        # Displays the armours the user owns
        write("\nIn your inventory you have: ")
        armours = user.get_armours()
        for armour in armours:
            write(f"- {armour.name}")
        sleep(selfsleep)
        option = input("\nWhich armour do you want to equip?: ")
        # Validates the users choice
        if option.lower() not in armours:
            write(f"\nYou tried equipping {option} but realised you cant create things out of thin air")
            sleep(selfsleep)
        else:
            write(f"\nYou equipped {option}")
            sleep(selfsleep)
            # Removes the defence increase of the previous armour
            if user.armour != None:
                user.defence = user.defence - user.armour.defence
            armour = user.armours[items.index(option.lower())]
            # Adds the defence of the new armour
            user.defence = user.defence + armour.defence
            user.armour = armour
            display_equipment(user)

def equip_weapon(user):
    """sub action from equip() for user to choose a weapon to equip"""
    if len(user.weapons) == 0:
        write("\nYou do not have any weapon to equip")
        sleep(selfsleep)
    else:
        # Displays the weapons the user owns
        write("\nIn your inventory you have: ")
        weapons = user.get_weapons()
        for weapon in weapons:
            write(f"- {weapon.name}")
        sleep(selfsleep)
        # Validates the user's choice
        option = input("\nWhich weapon do you want to equip?: ")
        if option.lower() not in weapons:
            write(f"\nYou tried equipping {option} but realised you cant create things out of thin air")
        else:
            write(f"\nYou equipped {option}")
            sleep(selfsleep)
            user.weapon = user.weapons[items.index(option.lower())]
            display_equipment(user)

def equip_accessory(user):
    """sub action from equip() for user to choose an accessory to equip"""
    if len(user.accessories) == 0:
        write("\nYou do not have any accessories to equip")
        sleep(selfsleep)
    else:
        write("\nIn your inventory you have: ")
        accessories = user.get_accessories()
        for accessory in accessories:
            write(f"- {accessory.name}")
        sleep(selfsleep)
        option = input("\nWhich accessory do you want to equip?: ")
        if option.lower() not in accessories:
            write(f"\nYou tried equipping {option} but realised you cant create things out of thin air")
        else:
            write(f"\nYou equipped {option}")
            sleep(selfsleep)

            # Removes the stat boost from the previous accessory
            if user.accessory != None:
                user.max_health = user.max_health - user.accessory.health_boost

                new_health = min(max(1, user.health - user.accessory.health_boost), user.max_health)
                user.health = new_health
                
                user.max_mana -= user.accessory.mana_boost

                new_mana = min(max(0, user.mana - user.accessory.mana_boost), user.max_mana)
                user.mana = new_mana

                user.attack -= user.accessory.attack_boost

                user.defence -= user.accessory.defence_boost

            # Adds the stat boost from the new accessory
            accessory = user.accessories[items.index(option.lower())]
            user.health += accessory.health_boost
            user.max_health += accessory.health_boost
            user.attack += accessory.attack_boost
            user.mana += accessory.mana_boost
            user.max_mana += accessory.mana_boost
            user.defence += user.accessory.defence_boost
            
            user.accessory = accessory
            display_equipment(user)

def status(user):
    """main action that prints user's status"""
    # Displays the users statistics
    write(f"\nName: {user.name}")
    write(f"Health: {user.health} / {user.max_health}")
    write(f"Mana: {user.mana} / {user.max_mana}")
    write(f"Defence: {user.defence}")
    write(f"Strength: {user.attack}")
    wait_for_key_press()

def info(user):
    """main action that prompts user for the type of item to find out more information about"""
    options = ["weapons", "spells", "armours", "accessories", "flasks", "items"]
    choice = get_input("What do you want to find out more about? ", [x.capitalize() for x in options]).lower()
    
    if choice not in options:
        write(f"\nYou do not own any {choice}")

    elif choice == "weapons":
        weapon_info(user)

    elif choice == "spells":
        spell_info(user)

    elif choice == "armours":
        armour_info(user)

    elif choice == "accessories":
        accessory_info(user)

    elif choice == "flasks":
        flask_info()

    elif choice == "items":
        item_info(user)
                
def weapon_info(user):
    """sub action from equip() that prompts user for specific weapon to find out more about"""
    # Check if the user owns any weapons
    if len(user.weapons) == 0:
        write("\nYou do not own any weapons yet")

    else:
        # Displays the weapons the user owns
        weapons = user.get_weapons()
        decision = get_input("\nWhich weapon do you want to find out more about?", weapons)
        if decision not in weapons:
            write(f"You do not own {decision}")

        else:
            # Displays the description of the weapon
            write(user.weapons[weapons.index(decision)].description)
            sleep(selfsleep)
            wait_for_key_press()

def spell_info(user):
    """sub action from equip() that prompts user for specific spell to find out more about"""
    # Check if the user knows any spells
    if len(user.spells) == 0:
        write("\nYou do not own any spells yet")

    else:
        # Displays the spells the user knows
        spells = user.get_spells()
        write("\nIn your inventory you have: ")
        for spell in spells:
            write(f"- {spell.name}")
        sleep(selfsleep)

        decision = input("\nWhich spell do you want to find out more about? : ")
        if decision.lower() not in spells:
            write(f"You do not own {decision}")

        else:
            # Displays the description of the spell
            write("\n", end="")
            write(user.spells[spells.index(decision)].description)
            sleep(selfsleep)

def armour_info(user):
    """sub action from equip() that prompts user for specific armour to find out more about"""
    # Check if the user owns any armours
    if len(user.armours) == 0:
        write("\nYou do not own any amours yet")

    else:
        # Displays the armours the user owns
        armours = user.get_armours()
        write("\nIn your inventory you have: ")
        for armour in armours:
            write(f"- {armour.name}")
        sleep(selfsleep)

        decision = input("\nWhich armour do you want to find out more about? : ")
        if decision.lower() not in armours:
            write(f"You do not own {decision}")

        else:
            # Displays the description of the armour
            write("\n", end="")
            write(user.armours[armours.index(decision)].description)
            sleep(selfsleep)

def accessory_info(user):
    """sub action from equip() that prompts user for specific accessory to find out more about"""
    # Checks if the user owns any accessories
    if len(user.accessories) == 0:
        write("\nYou do not own any accessories yet")

    else:
        # Displays the accessories the user owns
        accessories = user.get_accessories()
        write("\nIn your inventory you have: ")
        for accessory in accessories:
            write(f"- {accessory.name}")
        sleep(selfsleep)

        decision = input("\nWhich accesssory do you want to find out more about? : ")
        if decision.lower() not in accessories:
            write(f"You do not own {decision}")

        else:
            # Displays the description of the accessory
            write("\n", end="")
            write(user.accessories[accessories.index(decision)].description)
            sleep(selfsleep)

def flask_info():
    """sub action from equip() that prompts user for specific flask to find out more about"""
    write("\nIn your inventory you have: ")
    write("- Flask of Crimson Tears")
    write("- Flask of Cerulean Tears")

    decision = input("\nWhich accesssory do you want to find out more about? : ")
    if decision.lower() == "flask of crimson tears":
        write("\n", end ="")
        write(FlaskOfCrimsonTears().description)
        sleep(selfsleep)
    elif decision.lower() == "flask of cerulean tears":
        write("\n", end ="")
        write(FlaskOfCeruleanTears().description)
        sleep(selfsleep)
    else:
        write(f"You do not own {decision}")

def item_info(user):
    """sub action from equip() that prompts user for specific special item to find out more about"""
    # Check if the user owns any items
    if len(user.items) == 0:
        write("\nYou do not own any items yet")
    else:
        # Displays the items the user owns
        items = user.get_items()
        write("\nIn your inventory you have: ")
        for item in items:
            write(f"- {item}")
        sleep(selfsleep)

        decision = input("\nWhich item do you want to find out more about? : ")
        if decision.lower() not in items:
            write(f"You do not own {decision}")

        else:
            # Displays the description of the items
            write()
            write(user.items[items.index(decision)].description)
            sleep(selfsleep)
                
def display_room_name():
    """prints the room's name in a cool way"""
    write()
    write("="*25)
    space = " "*int((25-len(selfroom.name))/2)
    write(f"{space}{selfroom.name}{space}")
    write("="*25)

def display_room_description():
    """prints the room's description"""
    write()
    write(selfroom.description)
    sleep(selfsleep)
    look(selfroom)
    selfroom.been_here = True



def collect_loot(attacker, loot):
    """sub method from attack() to collect loot of defeated monster"""
    if loot.type == "weapon":
        attacker.weapons.append(loot)
        write(f"\nYou obtained a {loot.name}, a powerful weapon")
        
    elif loot.type == "spell":
        attacker.spells.append(loot)
        write(f"\nYou obtained a {loot.name}, a powerful spell")

    elif loot.type == "armour":
        attacker.armours.append(loot)
        write(f"\nYou obtained a {loot.name}, a powerful armour")

    elif loot.type == "accessory":
        attacker.accessories.append(loot)
        write(f"\nYou obtained a {loot.name}, a powerful accessory")

    elif loot.type == "upgrade":
        attacker.upgrades.append(loot)
        write(f"\nYou obtained a {loot.name}, a powerful upgrade")
        if loot.name == "Portal Gun":
            selfteleportable = True
            selfactions.append("teleport")
            selfdescription.append("Teleport to any room you have been to before")

    sleep(selfsleep)

def end_game():
    global selfend
    """displays scenario when user dies"""
    write("__   _______ _   _  ______ _____ ___________")
    sleep(0.2)
    write("\ \ / /  _  | | | | |  _  \_   _|  ___|  _  \\")
    sleep(0.2)
    write(" \ V /| | | | | | | | | | | | | | |__ | | | |")
    sleep(0.2)
    write("  \ / | | | | | | | | | | | | | |  __|| | | |")
    sleep(0.2)
    write("  | | \ \_/ / |_| | | |/ / _| |_| |___| |/ /")
    sleep(0.2)
    write("  \_/  \___/ \___/  |___/  \___/\____/|___/ ")
    selfend = True

def win(weapon):
    """displays scenario when user wins"""
    write(f"\nUsing the almighty {weapon.name}, you struck insert final boss down, crippling him of all his powers and stopping his evil tyranny over the school")
    sleep(selfsleep)
    write(" _____ ___________   _____ _       ___  _____ _   _ ")
    sleep(0.2)
    write("|  __ \  _  |  _  \ /  ___| |     / _ \|_   _| \ | |")
    sleep(0.2)
    write("| |  \/ | | | | | | \ `--.| |    / /_\ \ | | |  \| |")
    sleep(0.2)
    write("| | __| | | | | | |  `--. \ |    |  _  | | | | . ` |")
    sleep(0.2)
    write("| |_\ \ \_/ / |/ /  /\__/ / |____| | | |_| |_| |\  |")
    sleep(0.2)
    write(" \____/\___/|___/   \____/\_____/\_| |_/\___/\_| \_/")
    selfend = True

def die():
    """to end the game"""
    end_game()
       
def secret():
    """secret account that gives God like stats by setting name as meow"""
    write("\nWelcome chosen one, the Gods smile upon you and have rained down their blessing")
    sleep(selfsleep)
    selfcharacter.health = 999
    selfcharacter.max_health = 999
    selfcharacter.mana = 999
    selfcharacter.max_mana = 999
    selfcharacter.attack = 999
    selfcharacter.defence = 999
    selfcharacter.health_flask = 999
    selfcharacter.mana_flask = 999
    selfmap.full_reveal()
    selfcharacter.items.append(DectusMedallionLeft())
    selfcharacter.items.append(DectusMedallionRight())

def meow():
    print("meow")
    if selfroom.secret == True:
        write("""       
            
   ____ ___  ___  ____ _      __
  / __ `__ \/ _ \/ __ \ | /| / /
 / / / / / /  __/ /_/ / |/ |/ / 
/_/ /_/ /_/\___/\____/|__/|__/  
                               """)
        sleep(selfsleep)
        write("\nYou started communicating with the cat, leading you to discover a hidden passage\n")
        sleep(selfsleep)
        theLastResort = TheLastResort()
        selfroom.left = theLastResort
        theLastResort.right = selfroom
    else:
        choice = random.randint(1, 9)
        if choice == 1:
            write("""  
            
  __  __  U _____ u U  ___ u             
U|' \/ '|u\| ___"|/  \/"_ \/__        __ 
\| |\/| |/ |  _|"    | | | |\"\      /"/ 
 | |  | |  | |___.-,_| |_| |/\ \ /\ / /\ 
 |_|  |_|  |_____|\_)-\___/U  \ V  V /  U
<<,-,,-.   <<   >>     \\  .-,_\ /\ /_,-.
 (./  \.) (__) (__)   (__)  \_)-'  '-(_/ 
                                        """)
        elif choice == 2:
            write("""       
            
   ____ ___  ___  ____ _      __
  / __ `__ \/ _ \/ __ \ | /| / /
 / / / / / /  __/ /_/ / |/ |/ / 
/_/ /_/ /_/\___/\____/|__/|__/  
                               """)

        elif choice == 3:
            write("""                              
                              
 _ __ ___   ___  _____      __
| '_ ` _ \ / _ \/ _ \ \ /\ / /
| | | | | |  __/ (_) \ V  V / 
|_| |_| |_|\___|\___/ \_/\_/  
                              """)

        elif choice == 4:
            write(""" 
            
 _  _  ____  __   _  _ 
( \/ )(  __)/  \ / )( \
/ \/ \ ) _)(  O )\ /\ /
\_)(_/(____)\__/ (_/\_)
                        """)

        elif choice == 5:
            write("""   
            
 _ __ ___   ___  _____      __
| '_ ` _ \ / _ \/ _ \ \ /\ / /
| | | | | |  __/ (_) \ V  V / 
|_| |_| |_|\___|\___/ \_/\_/  
                              """)

        elif choice == 6:
            write("""                                    
                                    
,--,--,--. ,---.  ,---. ,--.   ,--. 
|        || .-. :| .-. ||  |.'.|  | 
|  |  |  |\   --.' '-' '|   .'.   | 
`--`--`--' `----' `---' '--'   '--' 
                                    """)

        elif choice == 7:
            write(""" 
 __    __     ______     ______     __     __    
/\ "-./  \   /\  ___\   /\  __ \   /\ \  _ \ \   
\ \ \-./\ \  \ \  __\   \ \ \/\ \  \ \ \/ ".\ \  
 \ \_\ \ \_\  \ \_____\  \ \_____\  \ \__/".~\_\ 
  \/_/  \/_/   \/_____/   \/_____/   \/_/   \/_/ 
                                                 """)

        elif choice == 8:
            write("""                                        
                                        
 _ .--..--.  .---.   .--.   _   _   __  
[ `.-. .-. |/ /__\\/ .'`\ \[ \ [ \ [  ] 
 | | | | | || \__.,| \__. | \ \/\ \/ /  
[___||__||__]'.__.' '.__.'   \__/\__/   
                                        """)

        elif choice == 9:
            write(""" 
 _      _____ ____  _     
/ \__/|/  __//  _ \/ \  /|
| |\/|||  \  | / \|| |  ||
| |  |||  /_ | \_/|| |/\||
\_/  \|\____\\____/\_/  \|
                          """)
    sleep(3)
def settings():
    """Show and change settings"""
    settings = []
    with open("settings.txt", "r") as f:
        settings = f.readlines()
        settings_dict = {}
        for row in settings:
            key, val = row.split()
            settings_dict[key] = val

    display_settings(settings_dict)
    
    change = input("\nDo you want to change your settings? ( yes / no ): ").lower()

    while change not in ["yes", "no"]:
        write("You briefly ponder the heavily nuanced and deeply intricate question of a choice between yes and no.")
        sleep(selfsleep)
        change = input("\nDo you want to change your settings? ( yes / no ): ").lower()
    
    if change == "yes":
    
        choice = ""
        accepted = list(settings_dict.keys())
        accepted.append("finish")
        while choice != "finish":
            choice = input("\nWhich setting do you want to change? (type finish to quit): ").lower()
            while choice not in accepted:
                write(f"{choice} is a uniquely unmodifiable property of this realm.")
                choice = input("\nWhich setting do you want to change? (type finish to quit): ").lower()

            if choice == "finish":
                with open("settings.txt", "w") as f:
                    for entry in settings_dict:
                        f.write(entry + " " + settings_dict[entry] + "\n")
                return
            
            if choice == "sleep":
                new = set_sleep(settings_dict["sleep"])
                settings_dict["sleep"] = new

            display_settings(settings_dict)
            
    elif change == "no":
        return

def display_settings(settings):
    """
    display the settings passed in
    """
    write("\nCurrent Settings:\n")
    for set in settings:
        write(f"{set}: {settings[set]}")

def set_sleep(current):
    """
    Change the interval between messages
    returns new value for sleep as string
    """
    count = 0
    write("\nsleep: the interval between messages sent by the game in seconds.")
    write(f"Current value: {current}")
    
    accept = [str(x) for x in range(6)]
    accept.append("cancel")

    new = input("\nEnter a new value for sleep (0-5 seconds), or cancel to cancel: ")
    while new not in accept:
        write("You count up to five on your fingers. Slowly.")
        sleep(selfsleep)
        new = input("\nEnter a new value for sleep (0-5 seconds), or cancel to cancel: ")
    
    if new.lower() == "cancel":
        return current
    else:
        selfsleep = int(new)
        return new
            

def secret_room():
    write("\nAfter you successfully defeated the sentinels, a stray ginger tabby cat emerges from behind a wall and stares at you playfully\n")
    selfroom.secret = True
    sleep(selfsleep)

def teleport():
    write("\nYou can teleport to: ")
    rooms = []
    for room in selfrooms:
        write(f"- {room.name}")
        rooms.append(room.name.lower())
    sleep(selfsleep)

    choice = input("\nWhich room do you want to teleport to?: ")
    
    if choice.lower() not in rooms:
        write(f"\nYou tried teleporting to {choice} but ended up in a dark abyss\n")
        sleep(selfsleep)

    else:
        selfroom = selfrooms[rooms.index(choice.lower())]
def display_map():
    """
    Show the map
    """
    
    legend = """Legend:
    ┌───┐                                   ╭━━━╮
    │   │ = Room has unfinished objectives  ┃   ┃ = Fully Cleared Room
    └───┘                                   ╰━━━╯
    """
    for row in selfmap.map:
        write("".join(row))
    write(legend)
    wait_for_key_press()
    
if __name__ == "__main__":
    root = tk.Tk()
    pause_var = tk.StringVar()
    pointer = tk.IntVar()
    sleepCount = tk.IntVar()
    root.geometry('600x600')
    root.configure(bg='black')
    text = tk.Text(root, height = 560, width = 560, background = "black", foreground = "white")
    text.pack()
    text.focus_set()
    root.after(0,intro)
    root.mainloop()
