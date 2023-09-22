#import from python built in libraries
import time
import random
import platform
#import from other files
from setup import *
import tkinter as tk
import map
import encounter
import Content.enemy as enemy
import Content.games as games

bgm = True
try:
    import pygame
    pygame.mixer.init()
except ModuleNotFoundError:
    bgm = False

selfend = False
selfactions = ["Move", "Attack", "Loot", "Inventory", "Meow", "Map", "Settings"]
currentPressedKey = ""
with open("settings.txt", "r") as f:
    out = f.readlines()
    out = [x.split()[1] for x in out]
selfsleep = int(out[0])
selfmusic = out[1]
selfup = out[2]
selfdown = out[3]
selfreturn = out[4]
selfsaveroom = None
selfsong = None
selfroom = None
selfcharacter = None
selfrooms = None
selfmap = None
selftaglines = []
selfline = 0

def sleep(t):
    root.after(int(t*1000), lambda: sleepCount.set(sleepCount.get()+1))
    root.wait_variable(sleepCount)

def write(txt="", newline=True, color=None):
    global selfline
    text['state'] = 'normal'
    text.insert(tk.END, txt)
    if newline:
        text.insert(tk.END, "\n")
    text['state'] = 'disabled'
    selfline += 1
    if color != None:
        selftaglines.append([color, f"{selfline}.0", f"{selfline}.end"])
        reapply_tag()

def write_animation(txt="", newline=True):
    global time
    def skip(e):
        global time
        time = 0
    time = 0.05
    root.bind(f'<{selfreturn}>', skip)
    for i in txt:
        text['state'] = 'normal'
        text.insert(tk.END, i)
        text['state'] = 'disabled'
        sleep(time)
    root.unbind(f'<{selfreturn}>')
    if newline:
        write()

def delete(keeptag=False):
    global selfline
    global selftaglines
    text['state'] = 'normal'
    text.delete("1.0", tk.END)
    text['state'] = 'disabled'
    selfline = 0

    if not keeptag:
        selftaglines = []
        for tag in text.tag_names():
            text.tag_delete(tag)


def start_typing(e):
    text['state'] = 'normal'
    data = text.get("1.0",'end-1c')
    if e.keysym == "BackSpace":
        if data != '\nWizard, key in your name: ':
            text.delete('end-2c','end-1c')
    else:
        text.insert(tk.END, e.char)
    text['state'] = 'disabled'
def hide_hud(fullscreen = True):
    w = window_width if fullscreen else text_width
    text.place(x = 0, y= 0, height = window_height, width = w)
    hud['state'] = 'normal'
    hud.lower()
    hud.delete("1.0", tk.END)
    hud['state'] = 'disabled'

def show_hud():
    global selfcharacter
    text.place(x = 0, y= 0, height = window_height, width = text_width)
    update_hud(selfcharacter)
    
def update_hud(user):
    
    hud['state'] = 'normal'
    hud.delete("1.0", tk.END)
    
    hud.tag_add('default', '1.0', tk.END)
    hud.tag_config('default', foreground = "#999594")
    hud.tag_add('title', '1.0', tk.END)
    hud.tag_config('title', foreground = "#c9c0bf")
    hud.tag_add('red', '1.0', tk.END)
    hud.tag_config('red', foreground = "red")
    hud.tag_add('blue', '1.0', tk.END)
    hud.tag_config('blue', foreground = "#68c2f5")
    hud.tag_add('green', '1.0', tk.END)
    hud.tag_config('green', foreground = "#67f55b")
    hud.tag_add('gold', '1.0', tk.END)
    hud.tag_config('gold', foreground = "#d9a002")
    hud.tag_add('white', '1.0', tk.END)
    hud.tag_config('white', foreground = "white")
    hud.tag_add('room', '1.0', tk.END)
    hud.tag_config('room', foreground = "white")

    hud.insert('1.0', f"\n{selfroom.name}\n", ('room',))
    hud.insert(tk.END, f"------------------\n\n", ('title',))
    
    hud.insert(tk.END, "Attributes\n", ('title',))
    hud.insert(tk.END, "\nHealth: ", ('default',))
    hud.insert(tk.END, f"{user.health} / {user.max_health} ", ('green',))
    hud.insert(tk.END, "\nMana: ", ('default',))
    hud.insert(tk.END, f"{user.mana} / {user.max_mana}", ('blue',))
    hud.insert(tk.END, "\nDefence: ", ('default',))
    hud.insert(tk.END, f"{user.defence}", ('blue',))
    hud.insert(tk.END, "\nStrength: ", ('default',))
    hud.insert(tk.END, f"{user.attack}", ('red',))
    hud.insert(tk.END, "\nRunes: ", ('default',))
    hud.insert(tk.END, f"{user.money}", ('gold',))
    hud.insert(tk.END, "\nCompletion: ", ('default',))
    hud.insert(tk.END, f"{int((selfcharacter.completion/28)*100)}%", ('white',))
    hud.insert(tk.END, f"\n------------------\n\n", ('title',))
    hud.insert(tk.END, "Equipment\n", ('title',))
    hud.insert(tk.END, "\nArmour: ", ('default',))
    hud.insert(tk.END, f"{user.armour.name if not user.armour is None else 'Empty'}", ('white',))
    hud.insert(tk.END, "\nWeapon: ", ('default',))
    hud.insert(tk.END, f"{user.weapon.name if not user.weapon is None else 'Empty'}", ('white',))
    hud.insert(tk.END, "\nAccessory: ", ('default',))
    hud.insert(tk.END, f"{user.accessory.name if not user.accessory is None else 'Empty'}", ('white',))
    hud.insert(tk.END, "\nShield: ", ('default',))
    hud.insert(tk.END, f"{user.shield.name if not user.shield is None else 'Empty'}", ('white',))
    hud['state'] = 'disabled'

def check_blank_name(e):
    if len(text.get("1.0",'end-1c')[26:].strip()) > 0:
        pause_var.set("done")
    elif text.get("1.0",'end-1c') != 'Wizard, key in your name: ':
        delete()
        write("\nWizard, key in your name: ", False)
    
def intro():
    """print introduction for the start of the game """
    hide_hud(False)
    # Displays the introduction messages
    if bgm and selfmusic == "On":
        pygame.mixer.music.load("Music/Intro.mp3")
        pygame.mixer.music.play(-1, fade_ms=100)
    write_animation('\nWelcome to Hogwarts School of Witchcraft and Wizardry')
    sleep(selfsleep)
    write()
    write_animation("The Dark Lord Voldemort has taken over Hogwarts and opened multiple interdimensional gates, bringing hordes of enemies into the school. Your job as the chosen one is to traverse the school in order to locate Voldemort and thwart his evil plan to take over the world.\n")
    sleep(selfsleep)
    decision = get_input_animation("Do you wish to enter the school?", ["Yes", "No"], None, False)
    delete()
    pause_var.set("")
    
    if decision.lower() == "yes":
        text['state'] = 'normal'
        write_animation("\nWizard, key in your name: ", False)
        text['state'] = 'disabled'
        text.bind('<Key>', start_typing)
        root.bind(f'<{selfreturn}>', check_blank_name)
        root.wait_variable(pause_var)
        root.unbind(f'<{selfreturn}>')
        text.unbind('<Key>')
        pause_var.set("")
        name = text.get("1.0",'end-1c')[26:].strip()
        delete()
        selfcharacter.name = name
        # Check if the user used the secret easter egg name

        if name == "meow":
            secret()
            if bgm and selfmusic == "On":
                pygame.mixer.music.fadeout(100)
            root.after(selfsleep*1000, run)
        else:
            write_animation("\nYou boldly opened the front gates of the school and made your way into the first room")
            wait_for_key_press()
            if bgm and selfmusic == "On":
                pygame.mixer.music.fadeout(100)
            root.after(selfsleep*1000, run)
            
    elif decision.lower() == "no":
        write_animation("Due to your utter cowardice, voldemort continued to gain power, spreading his control and chaos all over the world, leading to the complete annihilation of the human race.")
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
        wait_for_key_press()
        delete()
        root.after(0, title)

def wait_for_key_press():
    write("\nPress any key to continue")
    root.bind('<Key>', lambda x: pause_var.set("done"))
    root.wait_variable(pause_var)
    root.unbind('<Key>')
    pause_var.set("")
    
def show(prompt, options, deletebefore):
    data = text.get("1.0",'end-1c')
    delete(True)
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
    reapply_tag()

def show_animation(prompt, options, deletebefore):
    data = text.get("1.0",'end-1c')
    delete()
    keep = ""
    if not deletebefore:
        keep = data.split(prompt)[0]
        
    """main action for user to get the list of possible actions"""
    # Displays the list of actions the user can do
    p = pointer.get()
    write(keep, False)
    write_animation(prompt+"\n")
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
    root.bind(f'<{selfreturn}>', lambda x: pause_var.set("done"))
    root.bind(f"<{selfup}>", lambda e: up_action(prompt, displayoptions, deletebefore))
    root.bind(f"<{selfdown}>", lambda e: down_action(prompt, displayoptions, deletebefore))
    root.wait_variable(pause_var)
    root.unbind(f'<{selfreturn}>')
    root.unbind(f"<{selfup}>")
    root.unbind(f"<{selfdown}>")
    pause_var.set("")
    decision = options[pointer.get()]
    pointer.set(0)
    delete()
    return decision

def get_input_animation(prompt, options, displayoptions = None, deletebefore = True):
    """sub action for run() that prompts user for a main action"""
    if displayoptions is None:
        displayoptions = options
    show_animation(prompt, displayoptions, deletebefore)
    root.bind(f'<{selfreturn}>', lambda x: pause_var.set("done"))
    root.bind(f"<{selfup}>", lambda e: up_action(prompt, displayoptions, deletebefore))
    root.bind(f"<{selfdown}>", lambda e: down_action(prompt, displayoptions, deletebefore))
    root.wait_variable(pause_var)
    root.unbind(f'<{selfreturn}>')
    root.unbind(f"<{selfup}>")
    root.unbind(f"<{selfdown}>")
    pause_var.set("")
    decision = options[pointer.get()]
    pointer.set(0)
    delete()
    return decision

        
def run():
    global selfroom
    global selfend 
    global selfsong
    if bgm and selfmusic == "On" and selfsong != selfroom.music:
        pygame.mixer.music.load(f"Music/Room/{selfroom.music}")
        pygame.mixer.music.play(-1, fade_ms=100)
        selfsong = selfroom.music
    delete()
    update_hud(selfcharacter)
    """to be run in a loop to prompt user's action"""
    upgrades = selfcharacter.get_upgrades()

    if "Portal Gun" in upgrades and "Teleport" not in selfactions:
        selfactions.insert(-1, "Teleport")

    if "Shop" not in selfactions and selfcharacter.shop and selfroom.name == "The Forge":
        selfactions.insert(-1, "Shop")

    elif "Shop" in selfactions and selfroom.name != "The Forge":
        selfactions.remove("Shop")

    if "Gamble" not in selfactions and selfroom.name == "Kamurocho" and selfcharacter.gamble:
        selfactions.insert(-1, "Gamble")

    elif "Gamble" in selfactions and selfroom.name != "Kamurocho":
        selfactions.remove("Gamble")
    # Checks if the player has entered the room before
    if selfroom not in selfrooms:
        # Displays a description of the room if the player has not been there before
        look_animation(selfroom)
        selfrooms.append(selfroom)
        
        if selfroom.name == "Dirtmouth":
            selfmap.dirtmouth_enter()
        elif selfroom.name == "Celestial Resort":
            selfmap.celestial_resort_enter()
        elif selfroom.name == "The Forge":
            selfmap.forge_enter()
        elif selfroom.name == "Miquella's Haligtree":
            selfmap.haligtree_enter()
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
            selfmap.office_enter()
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
        decision = get_input_animation("What do you wish to do?", selfactions, None, False)
    else:
        look(selfroom)
        decision = get_input("What do you wish to do?", selfactions, None, False)

    # Does the action the user selected
        
    if decision.lower() == "move":
        move(selfroom)
        
    elif decision.lower() == "attack":
        attack(selfroom)

    elif decision.lower() == "loot":
        loot(selfcharacter, selfroom.loot)


    elif decision.lower() == "inventory":
        inventory(selfcharacter)

    elif decision.lower() == "meow":
        meow()

    elif decision.lower() == "settings":
        settings()

    elif decision.lower() == "teleport":
        teleport()

    elif decision.lower() == "map":
        display_map(False)

    elif decision.lower() == "save":
        save()

    elif decision.lower() == "shop":
        shop()

    elif decision.lower() == "gamble":
        gamble()

    if selfroom.enemy == None and selfroom.loot == None and not selfroom.secret and not selfroom.complete:
        if selfroom.name == "Dirtmouth":
            selfmap.dirtmouth_clear()
        elif selfroom.name == "Celestial Resort":
            selfmap.celestial_resort_clear()
        elif selfroom.name == "The Forge":
            selfmap.forge_clear()
        elif selfroom.name == "Miquella's Haligtree":
            selfmap.haligtree_clear()
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
            selfmap.office_clear()
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
        selfcharacter.completion += 1
        selfroom.complete = True

    if not selfend:
        root.after(1,run)
    else:
        if bgm and selfmusic == "On":
            pygame.mixer.music.stop()
            selfsong = None
        selfend = False
        title()

def inventory(user):
    decision = get_input("", ["Equip", "Items", "Information", "Finish"])
    if decision == "Equip":
        equip(selfcharacter)
    elif decision == "Items":
        item()
    elif decision == "Information":
        info(selfcharacter)
    elif decision == "Finish":
        return
        
def look(room):
    """main action to look around the room including rooms linked to the room and enemies in the room"""
    write()

    write(room.description)

    upgrades = selfcharacter.get_upgrades()

    if "Virtual Boo" in upgrades:
        if room.enemy != None:
            write()
            write(f"In the middle of the room is {room.enemy.name}, {room.enemy.description}")
            sleep(selfsleep)
            write()
            write(f"{room.enemy.name} has {room.enemy.health} health")
            sleep(selfsleep)
        if room.loot != None:
            write()
            write(f"There is a {room.loot.name} hidden in {room.name}")
            sleep(selfsleep)
        else:
            write()
            write(f"There is no loot hidden in {room.name}")
            sleep(selfsleep)
        
    elif room.enemy != None:
    # Displays the enemy in the room
        write()
        write(f"In the middle of the room is {room.enemy.name}, {room.enemy.description}")

    if room.enemy == None and room.save:
        write()
        write(f"{room.save_text}")
        
    if room.name == "The Forge":
        if room.enemy == None and room.secret and selfcharacter.shop:
            write()
            write(f"{room.secret_message}", True, "yellow")

    elif room.enemy == None and room.secret:
        write()
        write(f"{room.secret_message}", True, "yellow")
    write()

def look_animation(room):
    """main action to look around the room including rooms linked to the room and enemies in the room"""
    write()

    write_animation(room.description)

    upgrades = selfcharacter.get_upgrades()

    if "Virtual Boo" in upgrades:
        if room.enemy != None:
            write_animation(f"\nIn the middle of the room is {room.enemy.name}, {room.enemy.description}")
            sleep(selfsleep)
            write_animation(f"\n{room.enemy.name} has {room.enemy.health} health")
            sleep(selfsleep)
        if room.loot != None:
            write_animation(f"\nThere is a {room.loot.name} hidden in {room.name}")
            sleep(selfsleep)
        else:
            write_animation(f"\nThere is no loot hidden in {room.name}")
            sleep(selfsleep)
        
    elif room.enemy != None:
    # Displays the enemy in the room
        write_animation(f"\nIn the middle of the room is {room.enemy.name}, {room.enemy.description}")

    if room.enemy == None and room.save:
        write_animation(f"\n{room.save_text}")
        
    if room.name == "The Forge":
        if room.enemy == None and room.secret and selfcharacter.shop:
            write_animation(f"\n{room.secret_message}")

    elif room.enemy == None and room.secret:
        write_animation(f"\n{room.secret_message}")
    write()

def move(room):
    global selfroom
    """main action for user to traverse from one room to another"""
    hide_hud()
    display_map()
    movement = get_input('Which direction do you wish to move in?', ['Left', 'Right', 'Forward','Back', "Cancel"], None, False)

    if movement.lower() == "cancel":
        show_hud()
        return

    # Generate a random number to see if you managed to sneak past the enemy
    caught = False
    upgrades = selfcharacter.get_upgrades()
    
    if room.enemy != None:
        if "Smoke Bombs" in upgrades:
            write_animation(f"\nYou used your Smoke Bombs to sneak past {room.enemy.name}")
            sleep(selfsleep)
        
        elif selfcharacter.name == "meow":
            write_animation(f"\n{room.enemy.name} cowers in your presence, granting you passage through their domain.")
            sleep(selfsleep)
            
        else:
            chance = random.randint(1, 3)
            if chance == 1:
                caught = True
            else:
                write_animation(f"\nYou managed to sneak past {room.enemy.name}")
                sleep(selfsleep)

    if not caught:
        if movement.lower() == "left":
            if room.left == None:
                write_animation("\nYou walked to the left and smashed into a wall")
                wait_for_key_press()
            else:
                selfroom = room.left
                write_animation(f"\nYou walked into {selfroom.name}")
                wait_for_key_press()
                if bgm and selfmusic == "On":
                    pygame.mixer.music.fadeout(100)

        if movement.lower() == "right":
            if room.right == None:
                write_animation("\nYou walked to the right and smashed into a wall")
                wait_for_key_press()
            else:
                selfroom = room.right
                write_animation(f"\nYou walked into {selfroom.name}")
                wait_for_key_press()
                if bgm and selfmusic == "On":
                    pygame.mixer.music.fadeout(100)

        if movement.lower() == "forward":
            if room.forward == None:
                write_animation("\nYou walked forward and smashed into a wall")
                wait_for_key_press()
            # Check if you are going to the final boss room
            elif room.forward.name == "Principal's Office":
                items = selfcharacter.get_items()
                # Checks if you have the required items to enter the final boss room
                if "Dectus Medallion (right)" in items and "Dectus Medallion (left)" in items:
                    write_animation("\nCongratulations, you placed the two Dectus Medallions together releasing trememndous amounts of energy, breaking the powerful spell on the door")
                    selfroom = room.forward
                    wait_for_key_press()
                    if bgm and selfmusic == "On":
                        pygame.mixer.music.fadeout(100)
                else:
                    write_animation("\nYou tried entering the Principal's Office but the door was locked by a powerful spell")
                    sleep(selfsleep)
                    write_animation("\nYou probably need to find a special item to break the spell (remember to loot all the rooms)")
                    wait_for_key_press()
            else:
                selfroom = room.forward
                write_animation(f"\nYou walked into {selfroom.name}")
                wait_for_key_press()
                if bgm and selfmusic == "On":
                    pygame.mixer.music.fadeout(100)

        if movement.lower() == "back":
            if room.back == None:
                write_animation("\nYou turned back and smashed into a wall")
                wait_for_key_press()
            else:
                selfroom = room.back
                write_animation(f"\nYou walked into {selfroom.name}")
                wait_for_key_press()
                if bgm and selfmusic == "On":
                    pygame.mixer.music.fadeout(100)

    else:
        write_animation(f"\nYou tried to sneak to another room but {room.enemy.name} noticed you")
        sleep(selfsleep)
        wait_for_key_press()
        if bgm and selfmusic == "On":
            pygame.mixer.music.fadeout(100)
        attack(room)

    show_hud()

def loot(user, loot):
    """main action for user to search the room for loot"""

    # Generate a random number to see if you successfully loot the room whithout the enemy noticing
    caught = False
    upgrades = user.get_upgrades()

    if selfroom.enemy != None:
        if "Smoke Bombs" in upgrades:
            write_animation(f"\nYou used your Smoke Bombs to loot the room without being caught by {selfroom.enemy.name}")
            sleep(selfsleep)
        
        elif user.name == "meow":
            write_animation(f"\n{selfroom.enemy.name} cowers in your presence, granting you access to their domain.")
            sleep(selfsleep)
        else:
            chance = random.randint(1, 3)
            if chance != 1:
                caught = True
            else:
                write_animation(f"\nBy some miracle you managed to loot the room without {selfroom.enemy.name} noticing")
                sleep(selfsleep)

    if not caught:
        # Allow the user to loot the room
        if loot == None:
            write_animation("\nYou searched every nook and cranny but there was nothing to be found")
            wait_for_key_press()
        
        elif loot.name == "Flask of Crimson Tears":
            write_animation(f"\nYou found a {loot.name}, a powerful flask")
            wait_for_key_press()
            user.health_flask += 1
            selfroom.loot = None

        elif loot.name == "Flask of Cerulean Tears":
            write_animation(f"\nYou found a {loot.name}, a powerful flask")
            wait_for_key_press()
            user.mana_flask += 1
            selfroom.loot = None
            
        elif loot.type == "item":
            write_animation(f"\nYou found a {loot.name}, a powerful item")
            wait_for_key_press()
            user.items.append(loot)
            selfroom.loot = None

    else:
        write_animation(f"\n{selfroom.enemy.name} noticed you while you tried to loot the room")
        sleep(selfsleep)
        wait_for_key_press()
        if bgm and selfmusic == "On":
            pygame.mixer.music.fadeout(100)
        attack(selfroom)

def attack(room):
    global selfend
    """main action for user to attack the enemy in the room"""
    if room.enemy == None:
        delete()
        write_animation("\nYou attacked the air and realised how insane you looked")
        wait_for_key_press()
        
    else:
        outcome = room.encounter.fight(selfcharacter, root, text, hud, room.name, [window_width, window_height, text_width])
        if bgm and selfmusic == "On":
            pygame.mixer.music.load(f"Music/Room/{room.music}")
            pygame.mixer.music.play(-1, fade_ms=100)
        update_hud(selfcharacter)
        if outcome == 1:
            if room.enemy.name == "Voldemort":  
                win(selfcharacter.weapon)
                selfend = True
                return
            else:
                drops(room)
                money(room)
            if room.enemy.name == "Sentinels":
                room.secret = True
                delete()
                write()
                write_animation("After you successfully defeated the sentinels, a stray ginger tabby cat emerges from behind a wall and stares at you playfully")
                wait_for_key_press()
            elif room.enemy.name == "The Hollow Knight":
                room.secret = True
                delete()
                write()
                write_animation(room.secret_message)
                wait_for_key_press()
            elif room.enemy.name == "The Radiance":
                room.secret = False

            elif room.enemy.name == "Ganondorf":
                room.secret = True
                delete()
                write()
                write_animation(room.secret_message)
                wait_for_key_press()

            elif room.enemy.name == "Calamity Ganon":
                room.secret = False

            elif room.enemy.name == "Bowser":
                room.secret = True
                delete()
                write()
                write_animation(room.secret_message)
                wait_for_key_press()

            elif room.enemy.name == "Shibusawa":
                room.secret = True
                delete()
                write()
                write_animation(room.secret_message)
                wait_for_key_press()
                
            room.enemy = None
            if room.save == True:
                delete()
                write()
                write_animation(room.save_text)
                choice = get_input_animation("\nDo you wish to save?", ["Yes", "No"], None, False)
                if choice == "Yes":
                    save()
        elif outcome == 2:
            room.encounter.reset()
            end_game()
        elif outcome == 3:
            wait_for_key_press()
            room.encounter.reset()

def drops(room):
    """obtains drops from defeated enemy"""
    enemy = room.enemy
    player = selfcharacter

    if enemy.loot != None:
        write_animation(f"\n{enemy.name} dropped a {enemy.loot.name}")
        sleep(selfsleep)
        choice = get_input_animation(f"\nDo you want to pick up {enemy.loot.name}?",["Yes","No"],None,False)
        if choice.lower() == "yes":
            collect_loot(player, enemy.loot)
            sleep(selfsleep)
            write_animation(f"\n{enemy.loot.description}")
            wait_for_key_press()
            
        elif choice.lower() == "no":
            write_animation(f"\nYou left {enemy.loot.name} on the ground and allowed the resourceful rat to steal it")
            wait_for_key_press()

def money(room):
    if room.enemy.money != 0:
        delete()
        write_animation(f"\nYou gained {room.enemy.money} runes from defeating {room.enemy.name}")
        sleep(selfsleep)
        selfcharacter.money += room.enemy.money
        update_hud(selfcharacter)
        wait_for_key_press()
        
def equip(user):
    """main action for user to equip various items"""

    display_equipment(user)
    if len(user.get_shields()) == 0:
        options = ["Armour", "Weapon", "Accessory", "Finish"]
    else:
        options = ["Armour", "Weapon", "Accessory", "Shield", "Finish"]
    choice = ""
    while choice != "Finish":
        choice = get_input("\nwhat do you want to change?", options, None, False)

        if choice == "Armour":
            equip_armour(user)

        elif choice == "Weapon":
            equip_weapon(user)

        elif choice == "Accessory":
            equip_accessory(user)

        elif choice == "Shield":
            equip_shield(user)
        update_hud(user)
    inventory(user)
    
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

    if len(user.get_shields()) > 0:
        if user.shield == None:
            write("Shield : Empty")
        else:
            write(f"Shield : {user.shield.name}")

def equip_armour(user):
    """sub action from equip() for user to choose an armour to equip"""
    if len(user.armours) == 0:
        write("\nYou do not have any armour to equip")
        wait_for_key_press()
        delete()
        display_equipment(selfcharacter)
    else:
        # Displays the armours the user owns
        armours = user.get_armours()
        armours.append("Cancel")
        option = get_input("\nWhich armour do you want to equip?", armours)
        if option == "Cancel":
            display_equipment(user)

        else:
            write(f"\nYou equipped {option}")
            wait_for_key_press()
            # Removes the defence increase of the previous armour
            if user.armour != None:
                user.defence = user.defence - user.armour.defence
            armour = user.armours[armours.index(option)]
            # Adds the defence of the new armour
            user.defence = user.defence + armour.defence
            user.armour = armour
            delete()
            display_equipment(user)

def equip_weapon(user):
    """sub action from equip() for user to choose a weapon to equip"""
    # Displays the weapons the user owns
    weapons = user.get_weapons()
    weapons.append("Cancel")
    # Validates the user's choice
    option = get_input("\nWhich weapon do you want to equip?", weapons)
    if option == "Cancel":
        display_equipment(user)
    else:
        write(f"\nYou equipped {option}")
        wait_for_key_press()
        user.weapon = user.weapons[weapons.index(option)]
        delete()
        display_equipment(user)

def equip_shield(user):
    """sub action from equip() for user to choose a weapon to equip"""
    # Displays the weapons the user owns
    shields = user.get_shields()
    shields.append("Cancel")
    # Validates the user's choice
    option = get_input("\nWhich shield do you want to equip?", shields)
    if option == "Cancel":
        display_equipment(user)
    else:
        write(f"\nYou equipped {option}")
        wait_for_key_press()
        user.shield = user.shields[shields.index(option)]
        delete()
        display_equipment(user)

def equip_accessory(user):
    """sub action from equip() for user to choose an accessory to equip"""
    if len(user.accessories) == 0:
        write("\nYou do not have any accessories to equip")
        wait_for_key_press()
        delete()
        display_equipment(selfcharacter)
    else:
        accessories = user.get_accessories()
        accessories.append("Cancel")
        option = get_input("\nWhich accessory do you want to equip?", accessories)
        if option == "Cancel":
            display_equipment(user)

        else:
            write(f"\nYou equipped {option}")
            wait_for_key_press()
    
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
            accessory = user.accessories[accessories.index(option)]
            user.health += accessory.health_boost
            user.max_health += accessory.health_boost
            user.attack += accessory.attack_boost
            user.mana += accessory.mana_boost
            user.max_mana += accessory.mana_boost
            user.defence += accessory.defence_boost
            
            user.accessory = accessory
            delete()
            display_equipment(user)

def info(user):
    """main action that prompts user for the type of item to find out more information about"""
    if len(user.shields) == 0:
        options = ["weapons", "spells", "armours", "accessories", "flasks", "items", "upgrades", "Cancel"]
    else:
        options = ["weapons", "shields", "spells", "armours", "accessories", "flasks", "items", "upgrades", "Cancel"]
    choice = get_input("\nWhat do you want to find out more about? ", [x.capitalize() for x in options]).lower()

    if choice == "weapons":
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

    elif choice == "upgrades":
        upgrade_info(user)

    elif choice == "shields":
        shield_info(user)

    inventory(user)
                
def weapon_info(user):
    """sub action from equip() that prompts user for specific weapon to find out more about"""
        # Displays the weapons the user owns
    weapons = user.get_weapons()
    weapons.append("Cancel")
    decision = get_input("\nWhich weapon do you want to find out more about?", weapons)
    if decision == "Cancel":
        delete()
        info(user)
        return
    # Displays the description of the weapon
    write(user.weapons[weapons.index(decision)].description)
    wait_for_key_press()
    delete()
    weapon_info(user)

def shield_info(user):
    """sub action from equip() that prompts user for specific weapon to find out more about"""
    # Check if the user owns any weapons
    shields = user.get_shields()
    if len(shields) == 0:
        write("\nYou do not own any weapons yet")
        wait_for_key_press()
        delete()
        info(user)
    
    else:
        # Displays the weapons the user owns
        shields.append("Cancel")
        decision = get_input("\nWhich shield do you want to find out more about?", shields)
        if decision == "Cancel":
            delete()
            info(user)
            return
        # Displays the description of the weapon
        write(user.shields[shields.index(decision)].description)
        wait_for_key_press()
        delete()
        shield_info(user)

def spell_info(user):
    """sub action from equip() that prompts user for specific spell to find out more about"""
    # Displays the spells the user knows
    spells = user.get_spells()
    spells.append("Cancel")

    decision = get_input("\nWhich spell do you want to find out more about?", spells)

    if decision == "Cancel":
        delete()
        info(user)
        return

    # Displays the description of the spell
    write(user.spells[spells.index(decision)].description)
    wait_for_key_press()
    delete()
    spell_info(user)

def armour_info(user):
    """sub action from equip() that prompts user for specific armour to find out more about"""
    # Check if the user owns any armours
    if len(user.armours) == 0:
        write("\nYou do not own any amours yet")
        wait_for_key_press()
        delete()
        info(user)

    else:
        # Displays the armours the user owns
        armours = user.get_armours()
        armours.append("Cancel")

        decision = get_input("\nWhich armour do you want to find out more about?", armours)

        if decision == "Cancel":
            delete()
            info(user)
            return
        # Displays the description of the armour
        write(user.armours[armours.index(decision)].description)
        wait_for_key_press()
        delete()
        armour_info(user)

def accessory_info(user):
    """sub action from equip() that prompts user for specific accessory to find out more about"""
    # Checks if the user owns any accessories
    if len(user.accessories) == 0:
        write("\nYou do not own any accessories yet")
        wait_for_key_press()
        delete()
        info(user)

    else:
        # Displays the accessories the user owns
        accessories = user.get_accessories()
        accessories.append("Cancel")

        decision = get_input("\nWhich accesssory do you want to find out more about?", accessories)

        if decision == "Cancel":
            delete()
            info(user)
            return

        # Displays the description of the accessory
        write(user.accessories[accessories.index(decision)].description)
        wait_for_key_press()
        delete()
        accessory_info(user)

def flask_info():
    """sub action from equip() that prompts user for specific flask to find out more about"""

    decision = get_input("\nWhich accesssory do you want to find out more about?", ["Flask of Crimson Tears", "Flask of Cerulean Tears", "Cancel"])
    if decision.lower() == "flask of crimson tears":
        write(FlaskOfCrimsonTears().description)
        wait_for_key_press()
        delete()
        flask_info()
    elif decision.lower() == "flask of cerulean tears":
        write(FlaskOfCeruleanTears().description)
        wait_for_key_press()
        delete()
        flask_info()
    elif decision == "Cancel":
        delete()
        info(selfcharacter)

def item_info(user):
    """sub action from equip() that prompts user for specific special item to find out more about"""
    # Check if the user owns any items
    if len(user.items) == 0:
        write("\nYou do not own any items yet")
        wait_for_key_press()
        delete()
        info(user)
    else:
        # Displays the items the user owns
        items = user.get_items()
        items.append("Cancel")

        decision = get_input("\nWhich item do you want to find out more about?", items)

        if decision == "Cancel":
            delete()
            info(user)
            return
        # Displays the description of the items
        write(user.items[items.index(decision)].description)
        wait_for_key_press()
        delete()
        item_info(user)

def upgrade_info(user):
    if len(user.upgrades) == 0:
        write("\nYou do not own any upgrades yet")
        wait_for_key_press()
        delete()
        info(user)
    else:
        upgrades = user.get_upgrades()
        upgrades.append("Cancel")

        decision = get_input("\nWhich upgrade do you want to find out more about?", upgrades)

        if decision == "Cancel":
            delete()
            info(user)

        else:
            write(user.upgrades[upgrades.index(decision)].description)
            wait_for_key_press()
            delete()
            upgrade_info(user)

def collect_loot(attacker, loot):
    """sub method from attack() to collect loot of defeated monster"""
    if loot.type == "weapon":
        attacker.weapons.append(loot)
        write_animation(f"\nYou obtained a {loot.name}, a powerful weapon")
        
    elif loot.type == "spell":
        attacker.spells.append(loot)
        write_animation(f"\nYou obtained a {loot.name}, a powerful spell")

    elif loot.type == "armour":
        attacker.armours.append(loot)
        write_animation(f"\nYou obtained a {loot.name}, a powerful armour")

    elif loot.type == "accessory":
        attacker.accessories.append(loot)
        write_animation(f"\nYou obtained a {loot.name}, a powerful accessory")

    elif loot.type == "upgrade":
        attacker.upgrades.append(loot)
        write_animation(f"\nYou obtained a {loot.name}, a powerful upgrade")

    elif loot.type == "item":
        attacker.items.append(loot)
        write_animation(f"\nYou obtained a {loot.name}, an item")

    elif loot.type == "shield":
        attacker.shields.append(loot)
        write_animation(f"\nYou obtained a {loot.name}, a powerful shield")

    sleep(selfsleep)

def end_game():
    global selfend
    global selfroom

    if check_save():
        choice = get_input_animation("\nDo you want to reload the last save?", ["Yes", "No"], None, False)
        if choice == "Yes":
            load_save()

        else:
            selfend = True

    else:
        wait_for_key_press()
        selfend = True

def load_save():
    global selfroom
    global selfcharacter
    global selfrooms
    global selfmap
    temp = setup(True)
    selfroom = temp[0]
    selfcharacter = temp[1]
    selfrooms = temp[2]
    selfmap = temp[3]
    root.after(0,run)

def win(weapon):
    global selfend
    """displays scenario when user wins"""
    hide_hud()
    write_animation(f"\nUsing the almighty {weapon.name}, you struck Dio down, crippling him of all his powers and stopping his evil tyranny over the world")
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
    if selfcharacter.completion == 28:
        write()
        write("Thanks for putting in the effort to 100% the game, hope you enjoyed playing :)")
        sleep(selfsleep)
        write_animation("Thanks for putting in the effort to 100% the game, hope you enjoyed playing :)")
        sleep(selfsleep)
    wait_for_key_press()
    delete()
    write(" _____              _ _ _")
    sleep(0.2)
    write("/  __ \            | (_) |")
    sleep(0.2)
    write("| /  \/_ __ ___  __| |_| |_ ___")
    sleep(0.2)
    write("| |   | '__/ _ \/ _` | | __/ __|")
    sleep(0.2)
    write("| \__/\ | |  __/ (_| | | |_\__ \\")
    sleep(0.2)
    write(" \____/_|  \___|\__,_|_|\__|___/")
    write()
    write_animation("Programmers:")
    write()
    write_animation("Noah Lee")
    write_animation("Ethan Tse")
    write_animation("Brydon Ti")
    write()
    write("Play testers:")
    write()
    write_animation("Ming Cong")
    write_animation("Ling Kai")
    write_animation("Jae Zen")
    write_animation("Vincent Tse")
    write_animation("Yi Heng")
    write_animation("Josiah Lin")
    wait_for_key_press()
    delete()
    write(""" _____              _ _ _       
/  __ \            | (_) |      
| /  \/_ __ ___  __| |_| |_ ___ 
| |   | '__/ _ \/ _` | | __/ __|
| \__/\ | |  __/ (_| | | |_\__ \\
 \____/_|  \___|\__,_|_|\__|___/""")
    write()
    write_animation("Games represented:")
    write()
    write_animation("Hollow Knight")
    write_animation("Minecraft")
    write_animation("Final Fantasy VII")
    write_animation("Persona 5 Royal")
    write_animation("God of War")
    write_animation("Hades")
    write_animation("Risk of Rain 2")
    write_animation("Stray")
    write_animation("Luigi's Mansion 3")
    write_animation("Sonic")
    write_animation("Super Mario Bros")
    write_animation("Octopath Traveler 2")
    write_animation("Nier Automata")
    write_animation("Metroid")
    write_animation("The Legend of Zelda")
    write_animation("Celeste")
    write_animation("Ultrakill")
    write_animation("Valorant")
    write_animation("Shovel Knight")
    write_animation("Elden Ring")
    write_animation("Terraria")
    write_animation("Return of The Obra Dinn")
    write_animation("Yakuza 0")
    write_animation("Undertale")
    write_animation("Astral Chain")
    write_animation("Portal")
    write_animation("Tunic")
    write()
    write_animation("Special thanks to Mr Ng for providing us the opportunity to code this game")
    wait_for_key_press()
    
    selfend = True
    
       
def secret():
    """secret account that gives God like stats by setting name as meow"""
    write_animation("\nWelcome chosen one, the Gods smile upon you and have rained down their blessing")
    wait_for_key_press()
    selfcharacter.health = 999
    selfcharacter.max_health = 999
    selfcharacter.mana = 999
    selfcharacter.max_mana = 999
    selfcharacter.attack = 999
    selfcharacter.defence = 999
    selfcharacter.health_flask = 999
    selfcharacter.mana_flask = 999
    selfcharacter.money = 999
    #selfcharacter.upgrades.append(ShadeCloak())
    #selfcharacter.upgrades.append(Shield())
    selfmap.full_reveal()
    selfcharacter.items.append(DectusMedallionLeft())
    selfcharacter.items.append(DectusMedallionRight())
    selfcharacter.items.append(MementoMortem())
    #selfcharacter.upgrades.append(PortalGun())
    #selfcharacter.upgrades.append(VirtualBoo())
    selfcharacter.items.append(BlackBox())
    selfcharacter.items.append(RustyKey())
    selfcharacter.items.append(RoboticArm())
    selfcharacter.items.append(ScotchWhiskey())
    selfcharacter.shields.append(HylianShield())
    selfactions.insert(-1, "Teleport")

def meow():
    if selfroom.secret == True and selfroom.name == "Walled City 99":
        write("""       
            
   ____ ___  ___  ____ _      __
  / __ `__ \/ _ \/ __ \ | /| / /
 / / / / / /  __/ /_/ / |/ |/ / 
/_/ /_/ /_/\___/\____/|__/|__/  
                               """)
        sleep(selfsleep)
        write_animation("\nYou started communicating with the cat, leading you to discover a hidden passage\n")
        theLastResort = TheLastResort()
        selfroom.back = theLastResort
        theLastResort.forward = selfroom
        selfmap.meow_reveal()
        selfroom.secret = False
    else:
        choice = random.randint(1, 9)
        if choice == 1:
            write("""  
            
  __  __  U _____ u U  ___ u             
U|' \/ '|u\| ___"|/  \/"_ \/__        __ 
\| |\/| |/ |  _|"    | | | |\\\"\      /"/ 
 | |  | |  | |___.-,_| |_| |/\ \ /\ / /\ 
 |_|  |_|  |_____|\_)-\___/U  \ V  V /  U
<<,-,,-.   <<   >>     \\\\  .-,_\ /\ /_,-.
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
( \/ )(  __)/  \ / )( \\
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
[ `.-. .-. |/ /__\\\/ .'`\ \[ \ [ \ [  ] 
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
    wait_for_key_press()
    
def settings():
    global selfend
    """Show and change settings"""
    settings = []
    with open("settings.txt", "r") as f:
        settings = f.readlines()
        settings_dict = {}
        for row in settings:
            key, val = row.split()
            settings_dict[key] = val

    choices = ["Controls", "Music", "Quit", "Finish"]

    if selfroom.enemy == None:
        choices = ["Controls", "Music", "Save", "Quit", "Finish"]

    decision = ""

    while decision != "finish":
        decision = get_input("", choices)

        if decision.lower() == "save":
            save()

        elif decision.lower() == "quit":
            selection = get_input("\nAre you sure you want to quit to the title screen? (Unsaved progress will be lost)", ["Yes", "No"])
            if selection == "Yes":
                selfend = True
                return
        elif decision.lower() == "music":
            new = set_music(settings_dict["Music"])
            settings_dict["Music"] = new

        elif decision.lower() == "finish":
            with open("settings.txt", "w") as f:
                for entry in settings_dict:
                    f.write(entry + " " + settings_dict[entry] + "\n")
            return

        elif decision.lower() == "controls":
            set_controls()
            settings_dict["Up"] = selfup
            settings_dict["Down"] = selfdown
            settings_dict["Enter"] = selfreturn
    
def set_music(current):
    global selfsong
    global selfmusic

    new = get_input("\nMusic: ", ["On", "Off", "Cancel"])
    
    if new.lower() == "cancel":
        return current
    elif new.lower() == "off" and bgm:
        pygame.mixer.music.stop()
        selfsong = None
    elif new.lower() == "on" and bgm and selfsong != selfroom.music:
        pygame.mixer.music.load(f"Music/Room/{selfroom.music}")
        pygame.mixer.music.play(-1, fade_ms=1000)
        selfsong = selfroom.music
        
    selfmusic = new
    return new

def set_controls():
    write(f"Up : {selfup}")
    write(f"Down : {selfdown}")
    write(f"Enter : {selfreturn}")

    choice = get_input("\nWhich control do you want to change?", ["Up", "Down", "Enter", "Finish"], None, False)

    if choice == "Up":
        write("\nPress the key you want to change for scrolling up")
        root.bind("<Key>", change_up)
        root.wait_variable(pause_var)
        pause_var.set("")
        root.unbind("<Key>")
        delete()

    elif choice == "Down":
        write("\nPress the key you want to change for scrolling down")
        root.bind("<Key>", change_down)
        root.wait_variable(pause_var)
        pause_var.set("")
        root.unbind("<Key>")
        delete()

    elif choice  == "Enter":
        write("\nPress the key you want to change for selecting options")
        root.bind("<Key>", change_enter)
        root.wait_variable(pause_var)
        pause_var.set("")
        root.unbind("<Key>")
        delete()        

    elif choice == "Finish":
        return
    
    set_controls()

def change_up(e):
    global selfup
    if e.keysym == selfdown or e.keysym == selfreturn:
        delete()
        write(f"'{e.keysym}' is already binded to another control")
        wait_for_key_press()
    else:
        selfup = e.keysym
    pause_var.set("done")

def change_down(e):
    global selfdown
    if e.keysym == selfup or e.keysym == selfreturn:
        delete()
        write(f"'{e.keysym}' is already binded to another control")
        wait_for_key_press()
    else:
        selfdown = e.keysym
    pause_var.set("done")

def change_enter(e):
    global selfreturn
    if e.keysym == selfup or e.keysym == selfdown:
        delete()
        write(f"'{e.keysym}' is already binded to another control")
        wait_for_key_press()
    else:
        selfreturn = e.keysym
    pause_var.set("done")

def teleport():
    global selfroom
    rooms = []
    for room in selfrooms:
        rooms.append(room.name)
    rooms.append("Cancel")

    choice = get_input("\nWhich room do you want to teleport to?", rooms)

    if choice == "Cancel":
        return
    else:
        room = selfrooms[rooms.index(choice)]
        write(f"\nYou teleported to {room.name}")
        wait_for_key_press()
        selfroom = room

def reapply_tag():
    for tag in text.tag_names():
        text.tag_delete(tag)

    for i, line in enumerate(selftaglines):
        color, start, end = line
        text.tag_add(f"colour{i}", start, end)
        text.tag_config(f"colour{i}", foreground=color)

def display_map(moving = True):
    global selftaglines
    delete()
    if not moving:
        hide_hud()
    """
    Show the map
    """
    legend = """Legend:
┌───┐                                   ┌───*
│   │ = Room has unfinished objectives  │   │ = Fully Cleared Room
└───┘                                   └───┘
    """
    for row in selfmap.map:
        write("".join(row))

    if not moving:
        write(legend)

    if selfroom.name == "Dirtmouth":
        selftaglines = selfmap.dirtmouth_current()
    elif selfroom.name == "Celestial Resort":
        selftaglines = selfmap.celestial_resort_current()
    elif selfroom.name == "The Forge":
        selftaglines = selfmap.forge_current()
    elif selfroom.name == "Miquella's Haligtree":
        selftaglines = selfmap.haligtree_current()
    elif selfroom.name == "Aperture Lab":
        selftaglines = selfmap.aperture_current()
    elif selfroom.name == "Zebes":
        selftaglines = selfmap.zebes_current()
    elif selfroom.name == "Bunker":
        selftaglines = selfmap.bunker_current()
    elif selfroom.name == "Asphodel":
        selftaglines = selfmap.asphodel_current()
    elif selfroom.name == "Kingdom of Ku":
        selftaglines = selfmap.kingdom_ku_current()
    elif selfroom.name == "Greenhill Zone":
        selftaglines = selfmap.greenhill_current()
    elif selfroom.name == "The Hallow":
        selftaglines = selfmap.hallow_current()
    elif selfroom.name == "Commencement":
        selftaglines = selfmap.commencement_current()
    elif selfroom.name == "Midgar":
        selftaglines = selfmap.midgar_current()
    elif selfroom.name == "Hyrule Kingdom":
        selftaglines = selfmap.hyrule_current()
    elif selfroom.name == "The End Dimension":
        selftaglines = selfmap.end_dimension_current()
    elif selfroom.name == "Kamurocho":
        selftaglines = selfmap.kamurocho_current()
    elif selfroom.name == "Tower of Fate":
        selftaglines = selfmap.tower_current()
    elif selfroom.name == "Shores of Nine":
        selftaglines = selfmap.shores_current()
    elif selfroom.name == "Mementos":
        selftaglines = selfmap.mementos_current()
    elif selfroom.name == "Ascent":
        selftaglines = selfmap.ascent_current()
    elif selfroom.name == "The Shrieking Shack":
        selftaglines = selfmap.office_current()
    elif selfroom.name == "6th Circle of Hell":
        selftaglines = selfmap.sixth_circle_current()
    elif selfroom.name == "Snowdin":
        selftaglines = selfmap.snowdin_current()
    elif selfroom.name == "The Sealed Temple":
        selftaglines = selfmap.sealed_temple_current()
    elif selfroom.name == "The Astral Plane":
        selftaglines = selfmap.astral_plane_current()
    elif selfroom.name == "The Obra Dinn":
        selftaglines = selfmap.obradinn_current()
    elif selfroom.name == "The Mushroom Kingdom":
        selftaglines = selfmap.mushroom_current()
    elif selfroom.name == "Walled City 99":
        selftaglines = selfmap.walled_current()
    elif selfroom.name == "The Last Resort":
        selftaglines = selfmap.last_resort_current()
    
    if not moving:
        reapply_tag()
        wait_for_key_press()
        show_hud()

def save():
    global selfsaveroom
    selfsaveroom = selfroom
    selfcharacter.health = selfcharacter.max_health
    selfcharacter.mana = selfcharacter.max_mana
    write()
    write(selfroom.save_message)

    visited_rooms = []
    for room in selfrooms:
        visited_rooms.append(room.get_save_name())

    with open("save.txt", "r") as f:
        out = f.readlines()
        all_rooms  = []
        for i in range(29):
            all_rooms.append([out[35+i*6].strip(), out[37+i*6].split()[1], out[38+i*6].split()[1], out[39+i*6].split()[1]])

    stats = []
    stats.append(["name", selfcharacter.name])
    stats.append(["health", str(selfcharacter.health)])
    stats.append(["max_health", str(selfcharacter.max_health)])

    if len(selfcharacter.spells) == 0:
            stats.append(["spells", "None"])
    else:
        temp = ""
        for spell in selfcharacter.spells:
            temp += spell.get_save_name()
            temp += " "
        stats.append(["spells", temp])

    stats.append(["attack", str(selfcharacter.attack)])
    stats.append(["mana", str(selfcharacter.mana)])
    stats.append(["max_mana", str(selfcharacter.max_mana)])
    stats.append(["defence", str(selfcharacter.defence)])

    if selfcharacter.armour == None:
        stats.append(["armour", "None"])
    else:
        stats.append(["armour", selfcharacter.armour.get_save_name()])

    if len(selfcharacter.armours) == 0:
            stats.append(["armours", "None"])
    else:
        temp = ""
        for armour in selfcharacter.armours:
            temp += armour.get_save_name()
            temp += " "
        stats.append(["armours", temp])

    if selfcharacter.weapon == None:
        stats.append(["weapon", "None"])
    else:
        stats.append(["weapon", selfcharacter.weapon.get_save_name()])

    if len(selfcharacter.weapons) == 0:
            stats.append(["weapons", "None"])
    else:
        temp = ""
        for weapon in selfcharacter.weapons:
            temp += weapon.get_save_name()
            temp += " "
        stats.append(["weapons", temp])

    if selfcharacter.accessory == None:
        stats.append(["accessory", "None"])
    else:
        stats.append(["accessory", selfcharacter.accessory.get_save_name()])

    if len(selfcharacter.accessories) == 0:
            stats.append(["accessories", "None"])
    else:
        temp = ""
        for accessory in selfcharacter.accessories:
            temp += accessory.get_save_name()
            temp += " "
        stats.append(["accessories", temp])
    
    stats.append(["health_flask", str(selfcharacter.health_flask)])
    stats.append(["mana_flask", str(selfcharacter.mana_flask)])

    if len(selfcharacter.items) == 0:
            stats.append(["items", "None"])
    else:
        temp = ""
        for item in selfcharacter.items:
            temp += item.get_save_name()
            temp += " "
        stats.append(["items", temp])

    if len(selfcharacter.upgrades) == 0:
            stats.append(["upgrades", "None"])
    else:
        temp = ""
        for upgrade in selfcharacter.upgrades:
            temp += upgrade.get_save_name()
            temp += " "
        stats.append(["upgrades", temp])

    if selfcharacter.shield == None:
        stats.append(["shield", "None"])
    else:
        stats.append(["shield", selfcharacter.shield.get_save_name()])

    if len(selfcharacter.shields) == 0:
            stats.append(["shields", "None"])
    else:
        temp = ""
        for shield in selfcharacter.shields:
            temp += shield.get_save_name()
            temp += " "
        stats.append(["shields", temp])

    stats.append(["money", str(selfcharacter.money)])

    if selfcharacter.shop:
        stats.append(["shop", "True"])
    else:
        stats.append(["shop", "False"])

    if len(selfcharacter.shop_inventory) == 0:
            stats.append(["shop_inventory", "None"])
    else:
        temp = ""
        for item in selfcharacter.shop_inventory:
            temp += item.get_save_name()
            temp += " "
        stats.append(["shop_inventory", temp])

    if selfcharacter.gamble:
        stats.append(["gamble", "True"])
    else:
        stats.append(["gamble", "False"])

    if selfcharacter.additional_shop:
        stats.append(["additional_shop", "True"])
    else:
        stats.append(["additional_shop", "False"])

    stats.append(["completion", str(selfcharacter.completion)])

    for i in range(len(all_rooms)):

        if all_rooms[i][0] in visited_rooms:

            current_room = selfrooms[visited_rooms.index(all_rooms[i][0])]

            if current_room.enemy == None:
                all_rooms[i][1] = "None"
            else:
                all_rooms[i][1] = current_room.enemy.get_save_name()

            if current_room.loot == None:
                all_rooms[i][2] = "None"
            else:
                all_rooms[i][2] = current_room.loot.get_save_name()
            
            if current_room.secret:
                all_rooms[i][3] = "True"
            else:
                all_rooms[i][3] = "False"

    with open("save.txt", "w") as f:
        f.write("Save True\n\n")
        f.write(f"Room {selfroom.get_save_name()}\n\n")
        f.write(f"Rooms {' '.join(visited_rooms)}\n\n")
        f.write("Character\n\n")
        for stat in stats:
            f.write(f"{stat[0]} {stat[1]}\n")
        f.write("\n")
        for room in all_rooms:
            f.write(f"{room[0]}\n\n")
            f.write(f"enemy {room[1]}\n")
            f.write(f"loot {room[2]}\n")
            f.write(f"secret {room[3]}\n\n")

    wait_for_key_press()

def item():
    items = selfcharacter.get_items()

    if len(items) == 0:
        write("You do not own any items")
        wait_for_key_press()

    else:
        items.append("Cancel")
        choice = get_input("\nWhich item do you want to use?", items)

        if choice == "Cancel":
            return
    
        elif choice == "Memento Mortem" and selfroom.name == "Dirtmouth" and selfroom.secret:
            write("\nYou used the Memento Mortem on the empty vessel, transporting you to the past where you face The Radiance, The source of the infection in Hallownest")
            wait_for_key_press()
            secret_attack(enemy.TheRadiance())

        elif choice == "Black Box" and selfroom.name == "Hyrule Kingdom" and selfroom.secret:
            write("\nYou activated the Black Box, breaking a hole in the ground, Calamity Ganon, a dark, amorphous, and monstrous entity, then crawls out of the hole")
            wait_for_key_press()
            secret_attack(enemy.CalamityGanon())
        
        elif choice == "Rusty Key" and selfroom.name == "The Mushroom Kingdom" and selfroom.secret:
            write("\nYou used the Rusty Key to free the Robot")
            sleep(selfsleep)
            write()
            write("The robot thanks you for saving him and asks you to meet him in The Forge")
            wait_for_key_press()
            selfroom.secret = False
            selfcharacter.shop = True
            selfcharacter.items.pop(items.index(choice))

        elif choice == "Robotic Arm" and selfroom.name == "The Forge" and selfroom.secret and selfroom.secret_message == "You notice that Ox is missing his left arm":
            write("\nYou gave the Robotic Arm to Ox")
            sleep(selfsleep)
            write()
            write("Ox thanks you tremendously as its a perfect fit for him")
            sleep(selfsleep)
            write()
            write("There are new items you can purchase from the store now")
            wait_for_key_press()
            selfcharacter.shop_inventory.append(SmokeBombs())
            selfroom.secret = False
            selfcharacter.items.pop(items.index(choice))

        elif choice == "Scotch Whiskey" and selfroom.name == "Kamurocho" and selfroom.secret:
            write("\nYou gave the drunk man the bottle of Scotch Whiskey")
            sleep(selfsleep)
            write()
            write("The man then led you to an underground Casino")
            wait_for_key_press()
            delete()
            gamble(True)
            selfcharacter.gamble = True
            selfcharacter.items.pop(items.index(choice))
            selfroom.secret = False
            
    
        else:
            write(f"\nYou used {choice} but nothing happened")
            wait_for_key_press()
    inventory(selfcharacter)

def secret_attack(boss):
    secret = encounter.encounter(boss)
    outcome = secret.fight(selfcharacter, root, text)

    if outcome == 1:
        write(f"\n{boss.name} dropped a {boss.loot.name}")
        sleep(selfsleep)
        choice = get_input(f"\nDo you want to pick up {boss.loot.name}?",["Yes","No"],None,False)
        if choice.lower() == "yes":
            collect_loot(selfcharacter, boss.loot)
            sleep(selfsleep)
            write(f"\n{boss.loot.description}")
            wait_for_key_press()
    
        elif choice.lower() == "no":
            write(f"\nYou left {boss.loot.name} on the ground and allowed the resourceful rat to steal it")
            wait_for_key_press()

        selfroom.secret = False

    elif outcome == 2:
        selfroom.encounter.reset()
        end_game()
        
    elif outcome == 3:
        selfroom.encounter.reset()

def shop():
    if selfroom.secret_message == "The Robot has set up a shop in The Forge":
        write_animation("The robot introduces himself as Ox")
        write()
        write_animation("You notice that Ox is missing his left arm")
        selfcharacter.additional_shop = True
        selfroom.secret_message = "You notice that Ox is missing his left arm"
    items = selfcharacter.shop_inventory.copy()

    if len(items) == 0:
        write("You bought out everything in the store")
        wait_for_key_press()
        return

    display = []
    for item in items:
        display.append(f"{item.name} ({item.cost} runes)")
    items.append("Finish")
    display.append("Finish")

    write()
    choice = get_input(f"Which item would you like to purchase? (You have {selfcharacter.money} runes)", items, display, False)

    if choice == "Finish":
        return
    else:
        if selfcharacter.money < choice.cost:
            write(f"You do not have enough runes to buy {choice.name}")
            wait_for_key_press()
        else:
            write(f"You bought {choice.name}, a {choice.type}")
            sleep(selfsleep)
            write()
            write(choice.description)
            wait_for_key_press()
            if choice.type == "item":
                selfcharacter.items.append(choice)
            elif choice.type == "upgrade":
                selfcharacter.upgrades.append(choice)
            selfcharacter.money -= choice.cost
            selfcharacter.shop_inventory.pop(items.index(choice))
        delete()
        shop()

def gamble(new=False):
    if new:
        write_animation("You step into a vibrant and bustling establishment of lavish and extravagant design, with neon lights and flashy signage")
    else:
        write("You step into a vibrant and bustling establishment of lavish and extravagant design, with neon lights and flashy signage")

    advance = False
    while not advance:
        if new:
            choice = get_input_animation(f"Which game would you like to play? (You have {selfcharacter.money} runes)", ["Jan Ken Pon", "Blackjack", "Slots", "Finish"], None, False)
        else:
            choice = get_input(f"Which game would you like to play? (You have {selfcharacter.money} runes)", ["Jan Ken Pon", "Blackjack", "Slots", "Finish"], None, False)
    
        if choice == "Finish":
            advance = True
        elif choice == "Jan Ken Pon":
            if selfcharacter.money == 0:
                write("Sorry you do not have any runes to gamble")
                delete()
            else:
                games.JanKenPon(selfcharacter, root, text).play()

        elif choice == "Blackjack":
            if selfcharacter.money == 0:
                write("Sorry you do not have any runes to gamble")
                delete()
            else:
                games.Blackjack(selfcharacter, root, text).play()

        elif choice == "Slots":
            if selfcharacter.money == 0:
                write("Sorry you do not have any runes to gamble")
                delete()
            else:
                games.Slots(selfcharacter, root, text).play()

def logo():
    return """  
  _____            _                 _ _   _ 
 |  __ \          | |               | | | (_)
 | |__) |___  __ _| |_ __ ___  _   _| | |_ _   ／l、 
 |  _  // _ \/ _` | | '_ ` _ \| | | | | __| | （｡､ ｡ ７ 
 | | \ \  __/ (_| | | | | | | | |_| | | |_| |   l  ~ヽ 
 |_|  \_\___|\__,_|_|_| |_| |_|\__,_|_|\__|_|   じしf_,)ノ  
                                             
                                             """

def check_save():
    with open("save.txt", "r") as f:
        if f.readline().split()[1] == "True":
            return True
        else:
            return False

def title():
    global selfroom
    global selfcharacter
    global selfrooms
    global selfmap
    hide_hud()
    if bgm and selfmusic == "On":
        pygame.mixer.music.load(f"Music/Title.mp3")
        pygame.mixer.music.play(-1)
    delete()
    write(logo())
    wait_for_key_press()
    if check_save():
        choice = ["Continue Game", "New Game", "Exit"]
    else:
        choice = ["New Game", "Exit"]
    
    while True:
        decision = get_input(logo(), choice, None, False)
        if decision == "New Game" and "Continue Game" in choice:
            selection = get_input(f"{logo()}\nAre you sure you want to overwrite your save file?", ["Yes", "No"])
            if selection == "Yes":
                break

        elif decision == "Exit":
            selection = get_input(f"{logo()}\nAre you sure you want to exit the game?", ["Yes", "No"])
            if selection == "Yes":
                break
        
        else:
            break

    if bgm and selfmusic == "On":
        pygame.mixer.music.fadeout(100)
    if decision == "New Game":
        temp = setup()
        selfroom = temp[0]
        selfcharacter = temp[1]
        selfrooms = temp[2]
        selfmap = temp[3]
        root.after(0,intro)
    elif decision == "Continue Game":
        load_save()
        show_hud()
    else:
        if bgm and selfmusic == "On":
            pygame.mixer.music.stop()
        root.destroy()
                
if __name__ == "__main__":
    window_width = 1000
    text_width = 750
    window_height = 750
    root = tk.Tk()
    pause_var = tk.StringVar()
    pointer = tk.IntVar()
    sleepCount = tk.IntVar()
    root.geometry(f'{window_width}x{window_height}')
    root.configure(bg='black')
    frame=tk.Frame(root, width=window_width, height=window_height, background = "black")
    frame.pack()
    text = tk.Text(frame, background = "black", foreground = "white", borderwidth=0, wrap = tk.WORD, highlightthickness=0)
    hud = tk.Text(frame,  background = "black", foreground = "white", borderwidth=0, highlightthickness=0)
    if platform.system() == "Windows":
        windowsFont = ("Meslo LG S", 9, "normal")
        text.config(font = windowsFont)
        hud.config(font = windowsFont)
    text.place(x = 0, y= 0, height = window_height, width = window_width)
    hud.place(x = text_width+40, y = 0, height = window_height, width = window_width-(text_width+40))
    text.focus_set()
    root.after(0, title)
    root.mainloop()
