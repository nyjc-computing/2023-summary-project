#this file is for testing fights and not used in the main game

import Content.character as character
import encounter
import Content.enemy as enemy
import tkinter as tk
import platform
from Content.armour import *
from Content.weapon import *
from Content.accessory import *
from Content.spell import *
from Content.shield import *

window_width = 1000
text_width = 700
window_height = 700
root = tk.Tk()
pause_var = tk.StringVar()
pointer = tk.IntVar()
sleepCount = tk.IntVar()
root.geometry(f'{window_width}x{window_height}')
root.configure(bg='black')
windowsFont = ("Meslo LG S", 9, "normal")
frame=tk.Frame(root, width=window_width, height=window_height, background = "black")
frame.pack()
text = tk.Text(frame, background = "black", foreground = "white", borderwidth=0, wrap = tk.WORD, highlightthickness=0)
hud = tk.Text(frame,  background = "black", foreground = "white", borderwidth=0, highlightthickness=0)
if platform.system() == "Windows":
    text.config(font = windowsFont)
    hud.config(font = windowsFont)
text.place(x = 0, y= 0, height = window_height, width = 580)
hud.place(x = text_width+40, y = 0, height = window_height, width = window_width-(text_width+40))
text.focus_set()

bgm = True
try:
    import pygame
    pygame.mixer.init()
except ModuleNotFoundError:
    bgm = False
    
def equip_armour(user, armour):
    # Adds the defence of the new armour
    user.defence = user.defence + armour.defence
    user.armour = armour

def equip_accessory(user, accessory):
    # Adds the stat boost from the new accessory
    user.health += accessory.health_boost
    user.max_health += accessory.health_boost
    user.attack += accessory.attack_boost
    user.mana += accessory.mana_boost
    user.max_mana += accessory.mana_boost
    user.defence += accessory.defence_boost
    user.accessory = accessory

player = character.Character()
player.name = "awpik"
player.health = 100
player.max_health = 100
player.mana = 100
player.max_mana = 100
player.attack = 0

player.armours.append(OrnatePlate())
player.weapons.append(Zenith())
player.accessories.append(GoldenFeather())
player.spells.append(WingardiumLeviosa())
player.spells.append(VengefulSpirit())
player.spells.append(Megidolaon())
player.spells.append(GlintstoneCometshard())
player.spells.append(WillOTheWisp())

player.weapon = Zenith()

armour = OrnatePlate()
equip_armour(player, armour)

accessory = DragonAmulet()
equip_accessory(player, accessory)

shield = HylianShield()
player.shield = shield

player.health_flask = 20
player.mana_flask = 20

fight = encounter.glados_fight(enemy.Glados())

fight.fight(player, root, text, hud, "penisland", [window_width, window_height, text_width])
