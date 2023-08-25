#File containing the code for the game
from data import *
import random

NORTH = "NORTH"
SOUTH = "SOUTH"
EAST = "EAST"
WEST = "WEST"


class MUDGame:
    """This class encapsulates data for the main game implementation."""
    def __init__(self):
        self.gameover = False # default
        self.won = False # default
        self.maze = Labyrinth()
        self.maze.generate()
        self.steve = Steve()
        self.steve_path = []
        self.boss = Boss()


    
    def introduce(self): 
        """
        Starting interface of the game
        """
        username = input('Enter your username: ')
        while username is None:
            username = input('Enter your username: ')
        print(f'{username}, OH NO YOU ARE TRAPPED! \nYou will go through a series of rooms that may give you items or have ANGRY creatures wanting you DEAD :P \nKill them all, especially the boss to escape! \nGOOD LUCK ;D')

    def game_is_over(self) -> bool:
        """
        Returns True if either Steve or Boss is dead.
        """
        if self.steve.isdead() or self.boss.isdead(): # other conditions
            return True

    def show_status(self) -> None:
        """
        Print status of Steve.
        """
        print(self.steve)

    def show_options(self, sit: str) -> None:
        """
        Print menu of options provided to users according to different situation.
        """
        if sit == 'creature':
            menu = "1. Attack \n2. Retreat"
        elif sit == 'item':
            menu = '1. Pick Up \n2. Do not pick up'
        elif sit == 'restart':
            menu = '1. Yes \n2. No'
        elif sit == 'battle':
            menu = '1. Attack \n2. Heal'
        print(menu)

    def prompt_player(self) -> int:
        """
        Prompt player to choose option 1 or 2.
        Returns 1 or 2.
        """
        opt = input('Please choose option 1 or 2: ')
        while not self.isvalid(opt):
            print('Please enter a valid number(1/2).')
            opt = input('Please choose option 1 or 2: ')
        return opt


    def isvalid(self, opt) -> bool:
        """
        Validate player's choice when given 2 options.
        Returns a Boolean value.
        """
        if opt in '12':
            if len(opt) == 1:
                return True
        return False

    def battle(self) -> None:
        """
        Battle between Steve and creatures.
        Each takes a turn to deal damage or heal.
        Only boss and steve are able to heal themselves.
        Battle continues until one dies.
        """
        x, y = self.maze.get_current_pos()
        room = self.maze.lab[x][y]
        creature = room.get_creature()
        print(f"You have encountered the {creature.get_name()}!")
        while not self.steve.isdead() or creature.isdead():
            print(self.steve) # show HP
            if len(self.steve.inventory) == 0:
                print(f'You have no heal items! \nAttack the {creature.get_name()}.')
                damage = self.steve.get_attack()
                creature.take_damage(damage)
                print(f"{creature.get_name()} now has {creature.get_health()} HP")
            else:
                self.show_options('battle')
                battle_option = self.prompt_player()
                if battle_option == 1:
                    #attack
                    damage = self.steve.get_attack()
                    creature.take_damage(damage)
                    print(f"{creature.get_name()} now has {creature.get_health()} HP")
                elif battle_option == 2:
                    #heal
                    heal_option = None
                    n = 0
                    while not self.isvalid_heal(heal_option): 
                        self.steve.display_inventory()
                        if n > 1:
                            self.invalid_opt()
                        heal_option = input('Please choose a food item: ')
                        self.isvalid_heal(heal_option)
                    heal_option = int(heal_option) - 1
                    self.steve.eat(heal_option)
                    print('Healed!')
            #Steve endturn 
            damage = creature.random_move()
            self.steve.take_damage(damage)
            if damage == 0:
                print(f"The {creature.name} has healed itself.")
            else:
                print(f"The {creature.name} has dealt {damage} damage on you.")
        

    def isvalid_heal(self, heal_option):
        """
        Validate player's option when choosing food items from inventory.
        Used for battle()
        """
        range_of_option = len(self.steve.inventory) + 1
        valid_opt = []
        for i in range(1, range_of_option):
            valid_opt.append(str(i))
        if heal_option in valid_opt:
            return True
        return False
        

    def creature_encountered(self):
        """
        Returns True when creature is found in the room.
        """
        x, y = self.maze.get_current_pos()
        room = self.maze.lab[x][y]
        if room.get_creature() is None:
            return False
        return True

    def item_found(self):
        """
        Returns True if item is found in the room.
        """
        x, y = self.maze.get_current_pos()
        room = self.maze.lab[x][y]
        if room.get_item() is None:
            return False
        return True

    def show_winscreen(self):
        """
        Shows winscreen when Boss dies.
        """
        print('Congratulations! \nYou have escaped!')

    def show_losescreen(self):
        """
        Show losescreen when Steve dies."""
        print("YOU DIED...")
        print(f"Score: {random.randint(0, 10000)}")

    def movesteve(self):
        """
        Move Steve to another room when no item or creatures left in the current room.
        """
        current_location = self.maze.get_current_pos()
        opt_dir = {'1':NORTH, '2':SOUTH, '3':EAST, '4':WEST}
        available_dir = []
        dir_provided = ''
        for dir in opt_dir.values():
            if self.maze.can_move_here(current_location, dir):
                available_dir.append(dir)
        for i in range(len(available_dir)):
            dir_provided = dir_provided + str(i+1) + '. ' + available_dir[i] + ' '
        validity = False
        n = 0
        while validity == False:
            n += 1
            if n > 1:
                self.invalid_opt()
            print('Where are you going next? ' + dir_provided )
            choice = input('Next location: ')
            no_of_choice = len(available_dir)
            valid_choice = ''
            for i in range(no_of_choice):
                valid_choice += str(i + 1)
            if choice in valid_choice:
                if len(choice) == 1:
                    validity = True
        choice = int(choice)
        self.maze.move_steve(available_dir[choice - 1])

    def moveboss(self):
        """
        Move boss to another room.
        """
        self.maze.move_boss()

    def invalid_opt(self):
        """
        Show error message.
        """
        print('Please enter a valid option.')
    
    def run(self):
        """
- initiating the game
- interaction between steve and creatures --> what kind of creature, what kind of battle do you want
- how the turns work --> when to move steve, when to move the monster
- winscreen
- losescreen + lose conditions
- 
        """
        self.introduce()
        while not self.game_is_over():
            self.steve_path.append(self.maze.get_current_pos)
            self.show_status()
            # show status: direction, hp, lvl, inventory
            if self.creature_encountered():
                self.show_options('creature')
                # show player action options
                option = self.prompt_player()
                # prompt player to take actions
                if option == '1':
                    self.battle()
                    if self.game_is_over():
                        continue
                else:
                    odds = random.randint(1, 100)
                    if odds <= 40:
                        self.maze.try_move_steve(self.steve_path[-2])
                        continue
                    else:
                        print("Too late to escape!")
                        self.battle()
                        if self.game_is_over():
                            continue
            if self.item_found():
                x, y = self.maze.get_current_pos()
                room = self.maze.lab[x][y]
                item = room.get_item()
                self.show_options('item')
                item_choice = self.prompt_player()
                if item_choice == 1:
                    self.steve._add_item_to_inv(item)
            self.movesteve()
            if random.randint(1, 100) <= 30:
                self.moveboss() 
                # update
        if self.steve.isdead():
            self.show_losescreen()
        else:
            self.show_winscreen()

            
            