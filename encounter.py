#import builtins
import random
import tkinter as tk

bgm = True
try:
    import pygame
except ModuleNotFoundError:
    bgm = False

#import local files
import Content.item as item
import Content.enemy as e

class encounter:
    """
    Parent class for fights
    """

    def __init__(self, enemy: "Enemy"):
        self.initenemy = enemy
        self.enemies = [enemy]
        self.dead = []
        self.line = 1
        self.turns = 1
        self.tips = ["Remember to restore your health and mana before every fight",
                    "Other rooms may have useful drops that could make this fight easier"]
        self.taglines = []

    def hide_hud(self, fullscreen=True):
        w = self.window_width if fullscreen else self.text_width
        self.text.place(x=0, y=0, height=self.window_height, width=w)
        self.hud['state'] = 'normal'
        self.hud.lower()
        self.hud.delete("1.0", tk.END)
        self.hud['state'] = 'disabled'

    def show_hud(self):
        self.text.place(x=0, y=0, height=self.window_height, width=self.text_width)
        self.update_hud(self.player)

    def update_hud(self, user):

        self.hud['state'] = 'normal'
        self.hud.delete("1.0", tk.END)

        self.hud.tag_add('default', '1.0', tk.END)
        self.hud.tag_config('default', foreground="#999594")
        self.hud.tag_add('title', '1.0', tk.END)
        self.hud.tag_config('title', foreground="#c9c0bf")
        self.hud.tag_add('red', '1.0', tk.END)
        self.hud.tag_config('red', foreground="red")
        self.hud.tag_add('blue', '1.0', tk.END)
        self.hud.tag_config('blue', foreground="#68c2f5")
        self.hud.tag_add('green', '1.0', tk.END)
        self.hud.tag_config('green', foreground="#67f55b")
        self.hud.tag_add('gold', '1.0', tk.END)
        self.hud.tag_config('gold', foreground="#d9a002")
        self.hud.tag_add('white', '1.0', tk.END)
        self.hud.tag_config('white', foreground="white")
        self.hud.tag_add('room', '1.0', tk.END)
        self.hud.tag_config('room', foreground="white")
        self.hud.tag_add('grey', '1.0', tk.END)
        self.hud.tag_config('room', foreground="grey")

        self.hud.insert('1.0', f"\n{self.room}\n", ('room',))
        self.hud.insert(tk.END, f"------------------\n\n", ('title',))

        self.hud.insert(tk.END, "Attributes\n", ('title',))
        self.hud.insert(tk.END, "\nHealth: ", ('default',))
        self.hud.insert(tk.END, f"{user.health} / {user.max_health} ", ('green',))
        self.hud.insert(tk.END, "\nMana: ", ('default',))
        self.hud.insert(tk.END, f"{user.mana} / {user.max_mana}", ('blue',))
        self.hud.insert(tk.END, "\nDefence: ", ('default',))
        self.hud.insert(tk.END, f"{user.defence}", ('blue',))
        self.hud.insert(tk.END, "\nStrength: ", ('default',))
        self.hud.insert(tk.END, f"{user.attack}", ('red',))
        self.hud.insert(tk.END, "\nRunes: ", ('default',))
        self.hud.insert(tk.END, f"{user.money}", ('gold',))
        self.hud.insert(tk.END, "\nCompletion: ", ('default',))
        self.hud.insert(tk.END, f"{int((self.completion / 28) * 100)}%", ('white',))
        self.hud.insert(tk.END, f"\n------------------\n\n", ('title',))
        self.hud.insert(tk.END, "Equipment\n", ('title',))
        self.hud.insert(tk.END, "\nArmour: ", ('default',))
        self.hud.insert(tk.END, f"{user.armour.name if not user.armour is None else 'Empty'}", ('white',))
        self.hud.insert(tk.END, "\nWeapon: ", ('default',))
        self.hud.insert(tk.END, f"{user.weapon.name if not user.weapon is None else 'Empty'}", ('white',))
        self.hud.insert(tk.END, "\nAccessory: ", ('default',))
        self.hud.insert(tk.END, f"{user.accessory.name if not user.accessory is None else 'Empty'}", ('white',))
        self.hud.insert(tk.END, "\nShield: ", ('default',))
        self.hud.insert(tk.END, f"{user.shield.name if not user.shield is None else 'Empty'}", ('white',))
        self.hud.insert(tk.END, f"\n\nTurn {self.turns}")
        self.hud.insert(tk.END, "\n\nEnemies:", ('white',))
        for enemy in self.enemies:
            self.hud.insert(tk.END, f"\n{enemy.name} ({enemy.health} hp)", ('red',))
        for die in self.dead:
            self.hud.insert(tk.END, f"\n{die.name} ({die.health} hp)", ('grey',))
        self.hud['state'] = 'disabled'

    def reapply_tag(self):
        for tag in self.text.tag_names():
            self.text.tag_delete(tag)

        for i, line in enumerate(self.taglines):
            color, start, end = line
            self.text.tag_add(f"colour{i}", start, end)
            self.text.tag_config(f"colour{i}", foreground=color)
        
    def show(self, prompt, options, deletebefore):
        data = self.text.get("1.0",'end-1c')
        self.delete(True)
        keep = ""
        if not deletebefore:
            keep = data.split(prompt)[0]
            
        """main action for user to get the list of possible actions"""
        # Displays the list of actions the user can do
        p = self.pointer.get()
        self.write(keep+prompt+"\n")
        for i, e in enumerate(options):
            arrow = " "
            if p == i: arrow = ">"
            self.write(f"{arrow} {e}")
        self.reapply_tag()

    def show_animation(self, prompt, options, deletebefore):
        data = self.text.get("1.0",'end-1c')
        self.delete(True)
        keep = ""
        if not deletebefore:
            keep = data.split(prompt)[0]
            
        """main action for user to get the list of possible actions"""
        # Displays the list of actions the user can do
        p = self.pointer.get()
        self.write(keep, False)
        self.write_animation(prompt+"\n")
        for i, e in enumerate(options):
            arrow = " "
            if p == i: arrow = ">"
            self.write(f"{arrow} {e}")
        self.reapply_tag()
        
    def up_action(self, prompt, options, delete):
        p = self.pointer.get()
        if p != 0:
            self.pointer.set(p-1)
        else:
            self.pointer.set(len(options)-1)
    
        self.show(prompt, options, delete)
    
    def down_action(self, prompt, options, delete):
        p = self.pointer.get()
        if p != len(options)-1:
            self.pointer.set(p+1)
        else:
            self.pointer.set(0)
    
        self.show(prompt, options, delete)
    
    def get_input(self, prompt, options, displayoptions = None, deletebefore = True, animation = False):
        """sub action for run() that prompts user for a main action"""
        if displayoptions is None:
            displayoptions = options
        if animation:
            self.show_animation(prompt, displayoptions, deletebefore)
        else:
            self.show(prompt, displayoptions, deletebefore)
        self.root.bind(f'<{self.enter}>', lambda x: self.pause_var.set("done"))
        self.root.bind(f"<{self.up}>", lambda e: self.up_action(prompt, displayoptions, deletebefore))
        self.root.bind(f"<{self.down}>", lambda e: self.down_action(prompt, displayoptions, deletebefore))
        self.root.wait_variable(self.pause_var)
        self.root.unbind(f'<{self.enter}>')
        self.root.unbind(f"<{self.up}>")
        self.root.unbind(f"<{self.down}>")
        self.pause_var.set("")
        decision = options[self.pointer.get()]
        self.pointer.set(0)
        self.delete()
        return decision
    

    def reset(self):
        """
        resets the enemies when the player runs away
        """
        self.initenemy.__init__()
        og = self.initenemy
        self.__init__(og)

    def write(self, txt="", newline = True):
        """
        writes txt to the text field
        
        the colors rely on the line tracker which only increments by 1
        for each thing you write pls pls pls do not use newline characters
        """
        self.text['state'] = 'normal'
        if newline:
            self.text.insert(tk.END, txt+"\n")
        else:
            self.text.insert(tk.END, txt)
        self.text['state'] = 'disabled'
        self.line += 1
        self.reapply_tag()

    def write_animation(self, txt="", newline=True):
        global time
        def skip(e):
            global time
            time = 0
        time = 0.05
        self.root.bind(f'<{self.enter}>', skip)
        for i in txt:
            self.text['state'] = 'normal'
            self.text.insert(tk.END, i)
            self.text['state'] = 'disabled'
            self.delay(time)
        self.root.unbind(f'<{self.enter}>')
        if newline:
            self.write()

    def write_color(self, txt, color):
        """
        writes red to the text field in red

        the colors rely on the line tracker which only increments by 1
        for each thing you write pls pls pls do not use newline characters
        """
        self.text['state'] = 'normal'
        self.text.insert(tk.END, txt+"\n")

        self.taglines.append([color, f"{self.line}.0", f"{self.line}.end"])
        self.text['state'] = 'disabled'
        self.line += 1

    def delete(self, keeptag=False):
        """
        clears the text field
        """
        self.text['state'] = 'normal'
        self.text.delete("1.0", tk.END)
        self.text['state'] = 'disabled'
        self.line = 1

        #deleting tags
        if not keeptag:
            self.taglines = []
            for tag in self.text.tag_names():
                self.text.tag_delete(tag)

    def delay(self, sleep):
        """
        stops execution for self.sleep seconds
        """
        if sleep == 0:
            pass
        else:
            self.root.after(int(sleep*1000), lambda: self.pause.set(self.pause.get()+1))
            self.root.wait_variable(self.pause)

    def fight(self, player: "character", root: "tk.Tk()", text: "tk.Text()", hud: "tk.Text()", room: str, dim: list) -> int:
        """
        main loop for the encounter, return 1 if player wins, 2 if player dies, 3 if player flees
        'player' is the player character
        'root' is the tk window
        'text' is the text field to write messages to
        'hud' is the text field to display the hud
        'room' is the name of the current room
        'dim' is a list containing the window width, height, and the text width
        """

        self.player = player
        self.completion = player.completion
        self.root = root
        self.text = text
        self.hud = hud
        self.room = room
        self.pause = tk.IntVar()
        self.pointer = tk.IntVar()
        self.pause_var = tk.StringVar()
        self.window_width = dim[0]
        self.window_height = dim[1]
        self.text_width = dim[2]
        with open("settings.txt", "r") as f:
            out = f.readlines()
            out = [x.split()[1] for x in out]
        self.sleep = int(out[0])
        self.music = out[1]
        self.up = out[2]
        self.down = out[3]
        self.enter = out[4]
        #for the variable 'state', 0 means the fight is ongoing, 1 means the player wins, 2 means the player loses
        self.delete()

        if bgm and self.music == "On":
            pygame.mixer.music.load(f"Music/Enemy/{self.enemies[0].music}")
            pygame.mixer.music.play(-1, fade_ms=100)

        self.show_hud()

        state = 0
        data = self.text.get("1.0",'end-1c')
        while state == 0:
            
            advance = False
            count = 0
            while not advance:

                self.delete(True)
                self.write(data, False)

                if count == 0:
                    decision = self.get_choice(True)
                else:
                    decision = self.get_choice(False)

                if decision.lower() == "weapon":
                    advance = self.attack()

                elif decision.lower() == "spell":
                    advance = self.spell(data)

                elif decision.lower() == "flask":
                    advance = self.flask(data)

                elif decision.lower() == "defend":
                    self.write(f"You raise up your {self.player.shield.name}")
                    advance = True

                elif decision.lower() == "escape":
                    self.reset()
                    self.delete()
                    self.write("You put on the shade cloak and dashed away from the enemy")
                    self.delay(self.sleep)
                    if bgm and self.music == "On":
                        pygame.mixer.music.fadeout(100)
                    return 3
                count += 1

            self.show_hud()

            state = self.over()
            if state != 0:
                break

            self.write("")
            self.write(f"{'-'*50}")
            
            self.enemy_turn(decision)

            self.write("")
            self.write(f"{'-'*50}")

            data = self.text.get("1.0",'end-1c')
            state = self.over()
            self.turns += 1
            

            self.show_hud()

        if state == 1:
            if bgm and self.music == "On":
                pygame.mixer.music.fadeout(100)
            self.wait_for_key_press()
            return 1

        elif state == 2:
            self.wait_for_key_press()
            self.end_game()
            self.write("")
            
            self.write_animation(random.choice(self.tips))

            if bgm and self.music == "On":
                pygame.mixer.music.fadeout(100)
            return 2
    
    def get_choice(self, new) -> str:
        """
        get choice of action from user
        """

        choices = ["Weapon", "Spell", "Flask"]

        if self.player.shield != None:
            choices.append("Defend")

        if "Shade Cloak" in self.player.get_upgrades():
            choices.append("Escape")

        self.write("")
        if new:
            return self.get_input("What do you want to use?", choices, None, False, True)
        else:
            return self.get_input("What do you want to use?", choices, None, False, False)

    def enemy_turn(self, player_choice: str) -> None:
        """
        let enemies attack
        """

        #enemies take turns in random order
        enemies = self.enemies.copy()
        random.shuffle(enemies)
        
        for enemy in enemies:

            #negate damage if player is shielding
            damage = max(1, enemy.attack - self.player.defence)
            if player_choice.lower() == "defend":
                damage = int((self.player.shield.negation/100)*(damage))
                
                
            self.player.health = self.player.health - damage
            self.write("")
            self.write_animation(f"{enemy.name} used {enemy.move}, dealing {damage} damage to {self.player.name}")
            self.delay(self.sleep)
            if self.player.health <= 0:
                break

    def target(self) -> "Enemy":
        """
        let player choose a target for their attack/spell
        returns enemy object to be attacked, or none if cancelled
        """

        if len(self.enemies) == 1:
            self.delete()
            return self.enemies[0]

        choices = self.enemies.copy()
        display_options = [enemy.name for enemy in choices]
        choices.append(None)
        display_options.append("Cancel")

        return self.get_input("Which enemy do you want to attack?", choices, display_options, False) 

    def damage(self, weapon: "Weapon/Spell", target: "enemy") -> None:
        """
        deal damage to target using the weapon
        """

        #calculate damage dealt
        damage = max(1, weapon.attack + self.player.attack - target.defence)
        target.health = target.health - damage

        #check if enemy is dead
        if target.health > 0:
            self.write("")
            self.write_animation(f"{self.player.name}{weapon.move}, dealing {damage} damage to {target.name}")
            self.delay(self.sleep)
        else:
            self.write("")
            self.write_animation(f"{self.player.name}{weapon.win_front}{target.name}{weapon.win_back}")
            self.enemies.remove(target)
            target.health = 0
            self.dead.append(target)
            self.delay(self.sleep)

    def damage_all(self, weapon: "Weapon/Spell") -> None:
        """
        deal damage to all enemies using the weapon
        """
        self.write(f"{self.player.name}{weapon.move}, dealing damage to all enemies")
        new = []
        #loop through enemies
        for enemy in self.enemies:
            #calculate damage dealt
            damage = max(1, weapon.attack + self.player.attack - enemy.defence)
            enemy.health = enemy.health - damage

            #check if enemy is dead
            if enemy.health > 0:
                self.write("")
                self.write(f"{enemy.name} took {damage} damage")
                self.delay(self.sleep)
                new.append(enemy)
            else:
                self.write("")
                self.write(f"{weapon.win_front}{enemy.name}{weapon.win_back}")
                enemy.health = 0
                self.dead.append(enemy)
                self.delay

        self.enemies = new

    def attack(self) -> bool:
        """
        damages enemy using weapon
        return True if turn passes, return False if cancelled action
        """

        weapon = self.player.weapon
        
        if not weapon.aoe:
            target = self.target()
            
            if target == None:
                return False
                
            self.damage(weapon, target)
            
        else:
            self.damage_all(weapon)

        return True

    def spell(self, data) -> bool:
        """
        deducts mana from player for using a spell
        damages enemy using spell
        return True if turn passes, return False if cancelled action
        """

            
        spells = self.player.spells.copy()
        spell_display = []
        for spell in spells:
            spell_display.append(f"{spell.name} ({spell.cost} mana)")
        spells.append("Cancel")
        spell_display.append("Cancel")
        
        valid = False

        while not valid:
            self.write(data)
            choice = self.get_input("Which spell would you like to cast?", spells, spell_display, False)

            if choice == "Cancel":
                return False

            elif choice.cost > self.player.mana:
                self.write("")
                self.write(f"You do not have enough mana to cast {choice.name}")

            else:
                valid = True

        if not choice.aoe:

            target = self.target()
            if target == None:
                return False
        
            self.player.mana = self.player.mana - choice.cost
            self.write("")
            self.write(f"You used up {choice.cost} mana points")

            self.damage(choice, target)

        else:

            self.player.mana = self.player.mana - choice.cost
            self.write("")
            self.write(f"You used up {choice.cost} mana points")

            self.damage_all(choice)

        return True

    def flask(self, data) -> bool:
        """
        let player choose a flask to use
        return True if turn passes, return False if cancelled action
        """

        user = self.player
        health, mana = item.FlaskOfCrimsonTears(), item.FlaskOfCeruleanTears()

        flasks = [health, mana, "Cancel"]
        display = [f"Flask of Crimson Tears (restores {health.health} health)", f"Flask of Cerulean Tears (restores {mana.mana} mana)", "Cancel"]
        
        valid = False

        while not valid:

            self.write(data)

            choice = self.get_input("Which Flask would you like to drink?", flasks, display, False)

            if choice == "Cancel":
                return False

            elif choice == health:
                if user.health_flask <= 0:
                    self.write("You ran out of Flask of Crimson Tears")

                elif user.health == user.max_health:
                    self.write("You do not need to drink a Flask of Crimson Tears")

                else:
                    self.health_flask()
                    return True
                    

            elif choice == mana:
                if user.mana_flask <= 0:
                    self.write("You ran out of Flask of Cerulean Tears")

                elif user.mana == user.max_mana:
                    self.write("You do not need to drink a Flask of Cerulean Tears")

                else:
                    self.mana_flask()
                    return True
    
    def health_flask(self) -> None:
        """
        remove one health flask from player
        restore hp to player up to their maximum hp
        """
        #remove flask
        self.player.health_flask = self.player.health_flask - 1

        #heal player
        healing = min(self.player.max_health - self.player.health, item.FlaskOfCrimsonTears().health)
        self.player.health = self.player.health + healing
        self.write("")
        self.write(f"You drank a Flask of Crimson Tears and gained {healing} health")
        self.delay(self.sleep)

    def mana_flask(self) -> None:
        """
        remove one mana flask from player
        restore mana to player up to their maximum mana
        """
        #remove flask
        self.player.mana_flask = self.player.mana_flask - 1

        #restore player mana
        mana = min(self.player.max_mana - self.player.mana, item.FlaskOfCeruleanTears().mana)
        self.player.mana = self.player.mana + mana
        self.write("")
        self.write(f"You drank a Flask of Cerulean Tears and gained {mana} mana")
        self.delay(self.sleep)

    def over(self):
        """
        determines whether the fight should continue and outcome of fight
        return 0 for continue, 1 for player win, 2 for player loss
        """
        player = self.player
        enemies = self.enemies
        
        if player.health <= 0:
            return 2
        
        elif sum([enemy.health for enemy in enemies]) <= 0:
            return 1
        
        else:
            return 0
        
    def end_game(self) -> None:

        self.delete()

        def short_del():
            pause = tk.StringVar()
            self.root.after(100, lambda: pause.set("go"))
            self.root.wait_variable(pause)
        
        """displays scenario when user dies"""
        self.write("__   _______ _   _  ______ _____ ___________")
        short_del()
        self.write("\ \ / /  _  | | | | |  _  \_   _|  ___|  _  \\")
        short_del()
        self.write(" \ V /| | | | | | | | | | | | | | |__ | | | |")
        short_del()
        self.write("  \ / | | | | | | | | | | | | | |  __|| | | |")
        short_del()
        self.write("  | | \ \_/ / |_| | | |/ / _| |_| |___| |/ /")
        short_del()
        self.write("  \_/  \___/ \___/  |___/  \___/\____/|___/ ")

        self.update_hud(self.player)

    def wait_for_key_press(self):
        pause_var = tk.StringVar()
        self.write("\nPress any key to continue")
        self.root.bind('<Key>', lambda x: pause_var.set("done"))
        self.root.wait_variable(pause_var)
        self.root.unbind('<Key>')
        pause_var.set("")

class voldemort_fight(encounter):
    """
    an encounter that inherits from the encounter class
    """
    def __init__(self, enemy: "Enemy"):
        super().__init__(enemy)
        self.phases = [e.Dio()]
        self.transfer = 0

    def damage(self, weapon: "Weapon/Spell", target: "enemy") -> None:
        """
        deal damage to target using the weapon

        changing this method so that voldemort can revive himself after phase 1
        """
        #calculate damage dealt
        damage = weapon.attack + self.player.attack - target.defence
        target.health = target.health - damage

        #check if enemy is dead
        if target.health > 0:
            self.write("")
            self.write(f"{self.player.name}{weapon.move}, dealing {damage} damage to {target.name}")
            self.delay(self.sleep)
        else:
            #check if enemy can revive
            if len(self.phases) == 1:
                self.phase_transfer()
            else:
                self.enemies.remove(target)
                target.health = 0

    def phase_transfer(self):
        """
        Intermission for phase change
        """
        self.delete()
        self.write("insert phase transition")
        self.enemies[0] = self.phases[0]
        self.phases.remove(self.phases[0])
        self.transfer = 1
        self.delay(self.sleep)

    def enemy_turn(self, player_choice: str) -> None:
        """
        let enemies attack

        changing this method so that phase 2 doesn't take a turn immediately after reviving
        """

        if self.transfer == 1:
            self.transfer = 0
            return
        
        #enemies take turns in random order
        enemies = self.enemies
        random.shuffle(enemies)
        
        for enemy in enemies:

            # negate damage if player is shielding
            damage = max(1, enemy.attack - self.player.defence)
            if player_choice.lower() == "defend":
                damage = int((self.player.shield.negation / 100) * (damage))

            self.player.health = self.player.health - damage
            self.write("")
            self.write(f"{enemy.name} used {enemy.move}, dealing {damage} damage to {self.player.name}")
            self.delay(self.sleep)
            if self.player.health <= 0:
                break

class gabriel_fight(encounter):
    """
    an encounter that inherits from the encounter class
    """

    def __init__(self, enemy: "Enemy"):
        super().__init__(enemy)
        self.timer = 3
        self.spinning_blades = 0
        self.melee = ["buster sword", "master sword", "virtuous treaty",
                      "zenith", "rgx butterfly knife", "wand", "toy knife"]
        self.enemy = self.enemies[0]
        self.spin_warning = 0
        self.tips = ["Gabriel's Spinning Blades make close range attacks risky. Try engaging him at a distance with spells.",
                    "Gabriel doesn't activate spinning blades when he's winding up to use Sword Throw."]

    def enemy_turn(self, player_choice: str) -> None:
        """
        enemy turn

        changing this method to implement gabriel's fight mechanics
        """
        enemy = self.enemy
        if self.timer > 0:
            damage = max(1, enemy.attack - self.player.defence)
            if player_choice.lower() == "defend":
                damage = int((self.player.shield.negation/100)*(damage))

            self.player.health = self.player.health - damage
            self.write("")
            self.write_animation(f"Gabriel used light combo, dealing {damage} damage to {self.player.name}")
            self.delay(self.sleep)

        if self.timer > 1:
            enemy.defence = 10
            self.spinning_blades = 1
            self.write_animation(f"Gabriel used spinning blades, increasing his defence by 10 for one turn")
            self.delay(self.sleep)

        if self.timer == 1:
            enemy.defence = 0
            self.spinning_blades = 0

        if self.timer == 0:
            self.spinning_blades = 0
            self.timer = 4
            
            if player_choice == "Weapon" and self.player.weapon.name.lower() in self.melee:
                self.write("")
                self.write_animation("Gabriel used his special move, Sword Throw")
                self.delay(self.sleep)
                self.write("")
                self.write_animation(f"As you swung the {self.player.weapon.name}, you +PARRIED Gabriel's Sword Throw")
                enemy.health = enemy.health - 100
                if enemy.health <= 0:
                    self.write_animation("The Sword pierces Gabriel's armor and explodes, vanquishing the angel")
                else:
                    self.write_animation("It rockets back towards Gabriel, exploding for 100 damage")

            else:
                damage = max(1, 60 - self.player.defence)
                if player_choice.lower() == "defend":
                    damage = int((self.player.shield.negation/100)*(damage))
                             
                self.player.health = self.player.health - damage
                self.write("")
                self.write_animation(f"Gabriel used his special move, Sword Throw, dealing {damage} damage to {self.player.name}")
                self.delay(self.sleep)
                
        self.timer = self.timer - 1

        if self.timer == 0:
            self.write("")
            self.write("Gabriel is preparing something")

    def damage(self, weapon: "Weapon/Spell", target: "enemy") -> None:
        """
        deal damage to target using the weapon

        changing this method so that executing melee attacks while spinning blades is active deals damage to the player
        """
        #calculate damage dealt
        damage = max(1, weapon.attack + self.player.attack - target.defence)
        target.health = target.health - damage

        #check if enemy is dead
        if target.health > 0:
            self.write("")
            self.write_animation(f"{self.player.name}{weapon.move}, dealing {damage} damage to {target.name}")
            self.delay(self.sleep)
            
        else:
            self.write("")
            self.write_animation(f"{self.player.name}{weapon.win_front}{target.name}{weapon.win_back}")
            self.enemies.remove(target)
            target.health = 0
            self.dead.append(target)
            self.delay(self.sleep)

        if weapon.name.lower() in self.melee and self.spinning_blades == 1:
            damage = max(1, self.enemy.attack - self.player.defence)
            self.player.health = self.player.health - damage
            self.write("")
            self.write_animation(f"Gabriel's spinning blades hit you as you attacked, dealing {damage} damage to you")
            if self.spin_warning == 0:
                self.write_animation("You would do well to keep your distance while this ability is active")
                self.spin_warning = 1


class glados_fight(encounter):
    """
    an encounter that inherits from the encounter class
    """

    def __init__(self, enemy: "Enemy"):
        super().__init__(enemy)
        
        self.intro_trigger = 0
        
        self.gas_state = 1

        self.shield = True

        self.stun = 0
        
        self.cores = 0
        self.gauge = 0
        self.transfer = False

        self.turret_cooldown = 0
        self.turret_times = 0

        self.rocket_cooldown = 1
        self.rocket_state = 0

        self.tips = ["Damage dealt to turrets is dealt to GLaDOS as well, but is still subject to GLaDOS's damage reduction. Generally, don't attack GLaDOS while the shield is up.",
                     "After taking a certain amount of damage, GLaDOS will drop a core. Do it enough times and maybe something will happen.",
                     "Rocket Turrets deal a lot of damage, but they take a long time to arm. Destroy them before they can fire.",
                     "Every third time GLaDOS deploys sentry turrets, she will fail and stun herself, deactivating her shields",
                     "Make the most out of AOE attacks by maximising the number of enemies on the field",
                     "GLaDOS will use a powerful attack when she recovers from being stunned. Make sure you can tank it.",
                     "After a certain number of turns, the neurotoxins will immediately kill you. Every turn counts.",
                     "Devs personally recommend the Dragon Amulet for this fight."]


    def intro(self) -> None:
        self.write("")
        self.write_animation("GLaDOS starts filling the room with deadly neurotoxins")
        self.delay(self.sleep)
        self.write_animation("You will take 5 damage every turn, damage is not affected by defence")
        self.delay(self.sleep)
        self.write("")
        self.write_animation("GLaDOS activates bomb shields, reducing her incoming damage by 90%")

    def fight(self, player: "character", root: "tk.Tk()", text: "tk.Text()", hud: "tk.Text()", room: str,
              dim: list) -> int:
        """
        main loop for the encounter, return 1 if player wins, 2 if player dies, 3 if player flees
        'player' is the player character
        'root' is the tk window
        'text' is the text field to write messages to
        'hud' is the text field to display the hud
        'room' is the name of the current room
        'dim' is a list containing the window width, height, and the text width
        """

        self.player = player
        self.completion = player.completion
        self.root = root
        self.text = text
        self.hud = hud
        self.room = room
        self.pause = tk.IntVar()
        self.pointer = tk.IntVar()
        self.pause_var = tk.StringVar()
        self.window_width = dim[0]
        self.window_height = dim[1]
        self.text_width = dim[2]
        with open("settings.txt", "r") as f:
            out = f.readlines()
            out = [x.split()[1] for x in out]
        self.sleep = int(out[0])
        self.music = out[1]
        self.up = out[2]
        self.down = out[3]
        self.enter = out[4]
        #for the variable 'state', 0 means the fight is ongoing, 1 means the player wins, 2 means the player loses
        self.delete()

        if bgm and self.music == "On":
            pygame.mixer.music.load(f"Music/Enemy/{self.enemies[0].music}")
            pygame.mixer.music.play(-1, fade_ms=100)

        state = 0

        if self.intro_trigger == 0:
            self.intro()
            self.intro_trigger = 1

        data = self.text.get("1.0", 'end-1c')
        while state == 0:

            #display state of player and enemies
            self.show_hud()

            if self.turns == 25:
                self.write("")
                self.write_animation("The neurotoxin concentration is getting dangerously high")
                self.delay(self.sleep)
                self.write_animation("Damage per turn increased to 10")
                self.gas_state = 2

            if self.turns == 36:
                self.gas_state = 3

            self.core_corruption()
            
            data = self.text.get("1.0",'end-1c')

            advance = False
            count = 0
            while not advance:

                self.delete(True)
                self.write(data, False)
                if count == 0:
                    decision = self.get_choice(True)
                else:
                    decision = self.get_choice(False)

                if decision.lower() == "weapon":
                    advance = self.attack()

                elif decision.lower() == "spell":
                    advance = self.spell(data)

                elif decision.lower() == "flask":
                    advance = self.flask(data)

                elif decision.lower() == "defend":
                    self.write_animation(f"You raise up your {self.player.shield.name}")
                    self.delay(self.sleep)
                    advance = True

                elif decision.lower() == "escape":
                    self.reset()
                    self.delete()
                    self.write_animation("You put on the shade cloak and dashed away from the enemy")
                    self.delay(self.sleep)
                    if bgm and self.music == "On":
                        pygame.mixer.music.fadeout(100)
                    return 3

                elif decision.lower() == "core transfer":
                    if self.stun == 0:
                        self.write("")
                        self.write_animation("You grab one of the cores and try to reach the core receptacle,")
                        self.write_animation("but GLaDOS raises the floor panels, blocking your path")
                        self.delay(self.sleep)
                    else:
                        self.core_transfer()
                    advance = True
                
                count += 1

            self.check_gauge()

            state = self.over()
            if state != 0:
                break

            self.write("")
            self.write(f"{'-'*50}")
            
            self.enemy_turn(decision)

            self.write("")
            self.write(f"{'-'*50}")

            data = self.text.get("1.0", 'end-1c')
            state = self.over()

            self.rocket_cooldown -= 1
            self.turret_cooldown -= 1
            self.turns += 1

        if state == 1:
            if bgm and self.music == "On":
                pygame.mixer.music.fadeout(100)
            return 1

        elif state == 2:
            self.end_game()
            self.write("")
            self.write(random.choice(self.tips))
            self.wait_for_key_press()
            if bgm and self.music == "On":
                pygame.mixer.music.fadeout(100)
            return 2

    def enemy_turn(self, player_choice: str) -> None:
        """
        let enemies attack

        changing method to implement glados fight mechanics
        """
        #neurotoxins hit first

        self.write("")
        
        if self.gas_state == 1:
            
            self.write_animation("You take 5 damage from the neurotoxins")
            self.delay(self.sleep)
            self.player.health -= 5

        elif self.gas_state == 2:
            
            self.write_animation("You take 10 damage from the neurotoxins")
            self.delay(self.sleep)
            self.player.health -= 10

        elif self.gas_state == 3:
            
            self.write_animation("The neurotoxins have liquefied your brain matter")
            self.delay(self.sleep)
            self.player.health = 0

        if self.player.health <= 0:
            
            return None

        #glados turn if player is not dead

        if self.stun <= 0:

            if self.turret_cooldown <= 0:

                if self.turret_times == 2:
                    self.stunned()
                    self.turret_times = 0
                    
                else:
                    self.turrets()

            if self.rocket_cooldown <= 0:
                self.rocket()
        else:

            self.stun -= 1
            
            if self.stun == 0:
                self.wake(player_choice)

            else:
                self.write("")
                self.write_animation("GLaDOS twitches erratically. Looks like she's still out of it")
            
            
        #all other enemies take turns in random order
        enemies = self.enemies[1:]
        random.shuffle(enemies)
        
        for enemy in enemies:

            #if rocket sentry, wait for rocket to arm before attacking
            if enemy.name == "Rocket Sentry":
                if self.rocket_state == 3:
                    self.rocket_state = 2
                    continue
                elif self.rocket_state == 2:
                    out = enemy
                    self.rocket_state = 1

            #negate damage if player is shielding
            damage = max(1, enemy.attack - self.player.defence)
            if player_choice.lower() == "defend":
                damage = int((self.player.shield.negation/100)*(damage))
                
            self.player.health = self.player.health - damage
            self.write("")
            self.write_animation(f"{enemy.name} used {enemy.move}, dealing {damage} damage to {self.player.name}")
            self.delay(self.sleep)
            
            if self.player.health <= 0:
                return None

        if self.rocket_state == 1:
            self.enemies.remove(out)
            self.write("")
            self.write_animation(f"The Rocket Sentry retreats into the floor")
            self.rocket_state = 0
                
    def damage(self, weapon: "Weapon/Spell", target: "enemy") -> None:
        """
        deal damage to target using the weapon

        changing this method such that all damage dealt is dealt to glados as well
        changing this method such that rocket sentries reset state when killed
        changing this method to not record dead enemies to avoid flooding the window
        """

        #calculate damage dealt
        damage = max(1, weapon.attack + self.player.attack - target.defence)
        
        if target.name == "GLaDOS":
            damage = self.glados_damage(damage)
            self.add_gauge(damage)
        
        target.health = target.health - damage
        
        #check if enemy is dead
        if target.health > 0:
            self.write("")
            self.write_animation(f"{self.player.name}{weapon.move}, dealing {damage} damage to {target.name}")
            self.delay(self.sleep)
        else:
            
            if target.name == "Rocket Sentry":
                self.rocket_state = 2

            self.write("")
            self.write_animation(f"{self.player.name}{weapon.win_front}{target.name}{weapon.win_back}")
            self.enemies.remove(target)
            target.health = 0
            self.delay(self.sleep)

        if target.name != "GLaDOS":
            additional = self.glados_damage(damage)
            self.initenemy.health = self.initenemy.health - additional
            self.add_gauge(additional)
            self.write("")
            self.write_animation(f"GLaDOS took {additional} damage")

    def damage_all(self, weapon: "Weapon/Spell") -> None:
        """
        deal damage to all enemies using the weapon

        changing this method such that all damage is dealt to glados as well
        changing this method such that rocket sentries reset state when killed
        changing this method to not record turrets under dead enemies to avoid flooding the window
        """
        self.write(f"{self.player.name}{weapon.move}, dealing damage to all enemies")
        new = []
        total = 0
        #loop through enemies
        for enemy in self.enemies:
            #calculate damage dealt
            damage = max(1, weapon.attack + self.player.attack - enemy.defence)

            if enemy.name == "GLaDOS":
                damage = self.glados_damage(damage)
                self.add_gauge(damage)
                
            else:
                total += damage

            enemy.health = enemy.health - damage

            #check if enemy is dead
            if enemy.health > 0:
                self.write("")
                self.write_animation(f"{enemy.name} took {damage} damage")
                self.delay(self.sleep)
                new.append(enemy)
            else:

                if enemy.name == "Rocket Sentry":
                    self.rocket_state = 0
                
                self.write("")
                self.write_animation(f"{weapon.win_front}{enemy.name}{weapon.win_back}")
                enemy.health = 0
                self.delay

        self.enemies = new

        if total != 0:
            additional = self.glados_damage(total)
            self.initenemy.health = self.initenemy.health - additional
            self.add_gauge(additional)
            self.write("")
            self.write_animation(f"GLaDOS took an additional {additional} damage")

    def glados_damage(self, damage) -> int:
        """
        reduce damage if shield is active
        return damage as int
        """

        if self.shield == True:
            damage = max(1, int(damage * 0.1))

        return damage

    def add_gauge(self, damage) -> None:
        """
        adds damage to self.gauge
        """
        self.gauge = self.gauge + damage

    def check_gauge(self) -> None:
        """
        triggers self.core_drop() when self.gauge is higher than 400
        resets self.gauge to 0
        """
        if self.gauge > 400:
            if self.cores < 4:
                self.core_drop()
                self.gauge = 0

    def get_choice(self, new) -> str:
        """
        get choice of action from user

        changing this method to let player perform core transfer once conditions are fulfilled
        """

        choices = ["Weapon", "Spell", "Flask"]

        if self.player.shield != None:
            choices.append("Defend")

        if "Shade Cloak" in self.player.get_upgrades():
            choices.append("Escape")

        if self.transfer:
            choices.append("Core Transfer")

        self.write("")
        if new:
            return self.get_input("What do you want to use?", choices, None, False, True)
        else:
            return self.get_input("What do you want to use?", choices, None, False)
    
    def core_drop(self) -> None:
        """
        drop a core from glados mainframe
        if 4 cores have dropped, allow player to initiate core transfer
        """
        self.write("")
        self.write_animation("A white, spherical object screams as it falls from GLaDOS's body, landing with a resounding thump")
        self.delay(self.sleep)
        self.cores += 1
        if self.cores == 4:
            self.write("")
            self.write_animation('A voice announces over the speakers: "WARNING! CORE CORRUPTION AT 100 PERCENT"')
            self.write_animation('"MANUAL CORE REPLACEMENT REQUIRED"')
            self.write("")
            self.write_animation("A core receptacle rises up out of the floor")
            self.transfer = True
    
    def core_transfer(self) -> None:
        """
        kills glados
        """
        for enemy in self.enemies:
            enemy.health = 0

        self.write_animation("You grabbed a core and shoved it into the receptacle")
        self.write_animation("GLaDOS wakes up and tries to resist the transfer")
        self.write_animation("In her desperation, she blows up her mainframe, destroying herself")
        self.wait_for_key_press()

    def core_corruption(self) -> None:
        """
        outputs a message based on number of cores dropped
        """
        if self.cores == 0:
            return
        elif self.cores == 1:
            self.write("")
            self.write_animation('A voice announces over the speakers: "WARNING! CORE CORRUPTION AT 29 PERCENT"')
        elif self.cores == 2:
            self.write("")
            self.write_animation('A voice announces over the speakers: "WARNING! CORE CORRUPTION AT 58 PERCENT"')
        elif self.cores == 3:
            self.write("")
            self.write_animation('A voice announces over the speakers: "WARNING! CORE CORRUPTION AT 85 PERCENT"')
        elif self.cores > 3:
            self.write("")
            self.write_animation('A voice announces over the speakers: "WARNING! CORE CORRUPTION AT 100 PERCENT"')
            self.write_animation('"MANUAL CORE REPLACEMENT REQUIRED"')

    def stunned(self) -> None:

        self.write("")
        self.write_animation("GLaDOS tries to deploy more turrets, but the pipe network jams")
        self.delay(self.sleep)
        self.write_animation("There is an explosion overhead, bombarding GLaDOS with debris, stunning her")
        self.delay(self.sleep)
        self.write("")
        self.write_animation("GLaDOS's shields have been deactivated")

        self.shield = False
        self.stun = 2

    def rocket(self) -> None:

        self.enemies.append(e.Glados_Rocket())
        self.write("")
        self.write_animation("A Rocket Turret rises up out of the ground")
        self.delay(self.sleep)
        self.write_animation("It locks on to you and begins arming a rocket")
        self.delay(self.sleep)
        self.rocket_state = 3
        self.rocket_cooldown = 4

    def turrets(self) -> None:
        
        self.enemies.append(e.Glados_Turret())
        self.enemies.append(e.Glados_Turret())
        self.write("")
        self.write_animation("Sentry Turrets drop down from the pipe network above")
        self.delay(self.sleep)
        self.turret_times += 1
        self.turret_cooldown = 2

    def wake(self, player_choice) -> None:

        self.write_animation("GLaDOS has recovered, and she looks pissed")
        self.delay(self.sleep)
        self.write("")
        self.write_animation("GLaDOS's bomb shields are active again")
        self.delay(self.sleep)
        self.write_animation("GLaDOS used Thermal Discouragement Beams, dealing 60 damage to everyone")
        self.delay(self.sleep)

        self.shield = True
        self.enemies = [self.initenemy]
        
        damage = max(1, 60 - self.player.defence)
        if player_choice.lower() == "defend":
            damage = int((self.player.shield.negation/100)*(damage))

        self.player.health = self.player.health - damage

        self.write("")
        self.write_animation(f"You took {damage} damage")

    def over(self):
        """
        determines whether the fight should continue and outcome of fight
        return 0 for continue, 1 for player win, 2 for player loss
        """
        player = self.player
        
        if player.health <= 0:
            return 2
        
        elif self.initenemy.health <= 0:
            return 1
        
        else:
            return 0
        
class hollow_knight_encounter(encounter):

    def __init__(self, enemy):
        super().__init__(enemy)

        self.timer = 4

        self.enemy = self.enemies[0]

        self.tips = ["The Hollow Knight will retaliate if you use a weapon when he is defending", "The Hollow Knight will catch you off guard if you use a spell when he charges at you"]

    def enemy_turn(self, player_choice: str) -> None:
        """
        let enemies attack
        """

        enemy = self.enemy

        if self.timer == 4 or self.timer == 2:

            damage = max(1, enemy.attack - self.player.defence)
            if player_choice.lower() == "defend":
                damage = int((self.player.shield.negation/100)*(damage))
                
            self.player.health = self.player.health - damage
            self.write("")
            self.write_animation(f"The Hollow Knight swung his nail at you dealing {damage} damage to {self.player.name}")
            self.delay(self.sleep)

            if self.timer == 4:
                self.write("")
                self.write_animation("The Hollow Knight takes a defensive stance with his nail")

            if self.timer == 2:
                self.write("")
                self.write_animation("The Hollow Knight is getting ready to unleash a powerful attack")

            self.timer -= 1
        
        elif self.timer == 3:
            
            if player_choice.lower() == "weapon":
                damage = max(1, (enemy.attack * 3) - self.player.defence)
                if player_choice.lower() == "defend":
                    damage = int((self.player.shield.negation/100)*(damage))

                self.player.health = self.player.health - damage

                self.write("")
                self.write_animation(f"The Hollow Knight parried your attack and retaliated with a triple slash dealing {damage} damage to {self.player.name}")
            
            else:

                self.write("")
                self.write_animation("The Hollow Knight lowered his nail")
            
            self.timer -= 1

        else:

            if player_choice.lower() == "spell":
                damage = max(1, (enemy.attack * 2) - self.player.defence)
                if player_choice.lower() == "defend":
                    damage = int((self.player.shield.negation/100)*(damage))

                self.player.health = self.player.health - damage

                self.write("")
                self.write_animation(f"The Hollow Knight lunged towards you catching you off guard after casting your spell")
                self.write("")
                self.write_animation(f"The Hollow Knight's nail stabbed you directly, dealing {damage} damage to {self.player.name}")
            
            else:
                damage = max(1, int((enemy.attack * 0.5) - self.player.defence))
                if player_choice.lower() == "defend":
                    damage = int((self.player.shield.negation/100)*(damage))

                self.player.health = self.player.health - damage

                self.write("")
                self.write_animation(f"The Hollow Knight lunged towards you but you managed to react fast enough")
                self.write("")
                self.write_animation(f"The Hollow Knight's nail only grazed you, dealing {damage} damage to {self.player.name}")
                

            self.timer = 4

class ender_dragon_encounter(encounter):

    def __init__(self, enemy):
        super().__init__(enemy)

        self.enemies += [e.Ender_Crystal] * 3

    def enemy_turn(self, player_choice: str) -> None:
        """
        let enemies attack
        """

        #enemies take turns in random order
        enemies = self.enemies.copy()
        random.shuffle(enemies)
        
        for enemy in enemies:

            #negate damage if player is shielding
            damage = max(1, enemy.attack - self.player.defence)
            if player_choice.lower() == "defend":
                damage = int((self.player.shield.negation/100)*(damage))
                
                
            self.player.health = self.player.health - damage
            self.write("")
            self.write_animation(f"{enemy.name} used {enemy.move}, dealing {damage} damage to {self.player.name}")
            self.delay(self.sleep)
            if self.player.health <= 0:
                break
                
class ganondorf_encounter(encounter):

    def __init__(self, enemy):
        super().__init__(enemy)

        self.timer = 4

        self.enemy = self.enemies[0]

        self.tips = ["After charging at you, Ganondorf will slam the ground", "Use your shield to block charge attacks", "Ganodorf can remove your shield with his slam"]
        self.shield_state = True

    def enemy_turn(self, player_choice: str) -> None:
        """
        let enemies attack
        """

        enemy = self.enemy
        
        if self.timer == 3:

            damage = max(1, enemy.attack - self.player.defence)
            if player_choice.lower() == "defend" and self.shield_state:
                damage = int((self.player.shield.negation/100)*(damage))
                
            self.player.health = self.player.health - damage
            self.write("")
            self.write_animation(f"Ganondorf swings at you, dealing {damage} damage to {self.player.name}")
            self.delay(self.sleep)
            self.write_animation("Ganondorf is preparing to charge")

           
        
        elif self.timer == 2:
            
            if player_choice.lower() == "weapon" or player_choice.lower() == "spell":
                damage = max(1, (enemy.attack * 3) - self.player.defence)
                self.player.health = self.player.health - damage

                self.write("")
                self.write_animation(f"Ganondorf interrupted your attack and charged, dealing {damage} damage to {self.player.name}")
            elif player_choice.lower() == "defend":
                if self.shield_state:
                    damage = 0
                    self.write("")
                    self.write_animation("Ganondorf's charge was stopped by your shield")
                else:
                    damage = max(1, (enemy.attack - self.player.defence)/1.5)
                    self.write("")
                    self.write_animation("Without a shield you were forced to dodge,")
        else:
            damage = max(1, round((enemy.attack - self.player.defence)*1.5))
            self.player.health = self.player.health - damage
            self.write("")
            if player_choice.lower() == "spell":
                lower_bound = 2.5
                upper_bound = 1.5
                damage = max(1, random.randint(round(damage/lower_bound), round(damage/upper_bound)))
            else:
                self.write_animation(f"Ganondorf slams the ground in front of you, dealing {damage} damage to {self.player.name}")
            if player_choice.lower() == "defend":
                self.write_animation(f"You tried to block the attack but the shield was knocked out of your hands")
                self.shield_state = False
        self.timer -= 1
