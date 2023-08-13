#File for data designer

import json
import random

NORTH = "NORTH"
SOUTH = "SOUTH"
WEST = "WEST"
EAST = "EAST"
# NOVICE = "NOVICE"
# JOURNEYMAN = "JOURNEYMAN"
# MASTER = "MASTER"
STARTROOM = "STARTROOM"


CREATURE = "CREATURE"


labsize = 10 # cannot be too small!!
class Labyrinth:
    """
    -- ATTRIBUTES --
    - lab: list[list[Room]]
    - difficulty_level
    - boss_pos: list[int]
    - steve_pos: list[int]

    -- METHODS
    + generate(self) -> None
    - generate_place_steve_boss() -> None:
    - generate_cmaze(startroom_pos: list) -> None:
    - generate_link_rooms(room1coords: list, room2coords: list) -> None:
    - generate_rooms_connected() -> bool:
    + move_boss(self) -> None:
    + can_move_here(self, coords: list(int), direction):
    + steve_useitem(self, item: Item) -> None
    + monster_roar(self) -> None
    
    """
    def __init__(self):
        self.lab = [[None] * labsize] * labsize
        self.difficulty_level = None
        self.boss_pos = [-1, -1] # Decided upon generation
        self.steve_pos = [-1, -1] # Decided upon generation

    def generate(self) -> None:
        """Generates the maze by:
        1. Filling in empty rooms in the empty maze
        2. Chooses (somewhat) randomly which room is the startroom room where Steve is placed
        3. Places the boss room opposite to startroom
        4. Makes the rooms connected like a maze structure
        5. Fills in the rooms with random contents (creatures and items)
        
        6. (Unimplemented functionality) Takes in a difficulty level and sets the game accordingly
        
        Requires the use of helper methods, namely:
        _generate_place_steve_boss()
        _generate_maze()
        _generate_count_unconnected_rooms()
        _generate_link_rooms()
        """
        raise NotImplementedError
        # self.difficulty_level = difficulty_level
        # put in empty rooms
        for x in range(labsize):
            for y in range(labsize):
                self.lab[x][y] = Room(x, y)
        self._generate_place_steve_boss()
        self._generate_maze()
        # give the rooms contents

    def _generate_place_steve_boss(self) -> None:
        """One of many helper methods of the generate() method.

        Chooses a startroom somewhat randomly, places Steve there,
        and places the boss in a room opposite of startroom

        How startroom is chosen:
        - The possible rooms to be picked are rooms nearer to the perimeter than the center.
        - e.g. If the labyrinth is 10 by 10 rooms, the middle 6 by 6 rooms cannot be chosen as startroom. the surrounding 64 rooms can be chosen as rooms.
        - Of the 64 rooms nearing the far sides of the labyrinth, one room is chosen at random.
        - This means that labsize cannot be too small, or the generation may break. ie labsize cannot be less than 4.

        How bossroom is chosen:
        - e.g. labsize is set to 10 and startroom coords are [1, 7]
        - bossroom is at the opposite of the labyrinth at [8, 2]

        Startroom will be remembered throughout the game, the starting position of the boss will not be remembered. 
        """
        # choose position of Start room randomly
        n = labsize // 4
        n = random.randint(-n, n - 1)
        m = random.randint(0, labsize - 1)
        mylist = [n, m]
        random.shuffle(mylist)
        steve_x, steve_y = mylist
        self.lab[steve_x][steve_y].settype_startroom()
        self.steve_pos = mylist
        # choose position of Monster room opposite to where steve is
        boss_x = labsize - 1 - steve_x
        boss_y = labsize - 1 - steve_y
        if (boss_x, boss_y) == (steve_x, steve_y): # if they happen to be placed in the same room
            raise ValueError("Steve and the Boss have been put at the same location!")
        self.lab[boss_x][boss_y].boss_enters()    

    def _generate_maze(self, startroom_pos: list[int]) -> None:
        # link up a large number of rooms
        self._generate_recursive_linking(startroom_pos)
        unconnected = self._generate_count_unconnected_rooms()
        while unconnected != 0:
            for x in range(labsize):
                for y in range(labsize):
                    room = self.lab[x][y]
                    if not room.is_connected_tostart():
                        self._generate_force_connect([x, y])
            unconnected = self._generate_count_unconnected_rooms()

    def _generate_force_connect(roomcoords: list[int]) -> None:
        """links holes in connectivity of maze to as many adjacent rooms as possible"""
        dirlist = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        random.shuffle(dirlist)
        for i in range(4):
            neighbourcoords = [roomcoords[0] + dirlist[i][0], roomcoords[1] + roomcoords[i][1]]
            possible = True
            posscoords = [i for i in labsize]
            for t in neighbourcoords:
                if t not in posscoords:
                    possible = False
            if possible:
                _generate_link_rooms(roomcoords, neighbourcoords)
                
            
    def _generate_recursive_linking(self, thisroomcoords: list[int]) -> None:
        """
        Attempts to link a large number of rooms, recursively
        Rules for whether a neighbour room is linkable:
        0. The room exists.
        1. The room is not already linked.

        thisroom will make an attempt to link to linkable neighbour rooms.
        The success of the attempt is based on chance.
        This chance can be changed, but is hardcoded.
        This chance should be quite high above 25%; the lower the odds, the more holes in connectivity, the more cleanup linking has to be done.
        
        """
        # current room should already be connected
        x, y = thisroomcoords
        thisroom = self.lab[x][y] # object thisroom object
        if not thisroom.is_connected_tostart():
            raise ValueError("Room that is trying to (recursively) link to others is not yet connected, should not happen.")
        dirlist = [[0, 1], [0, -1], [1, 0], [-1, 0]] # corresponding to N, S, E, W
        neighbours_statuses = thisroom.get_neighbours_statuses()
        # iteration through N, S, E, W:
        # checking whether they are linkable by rules
        # if linkable, there is a chance of linking
        for i in range(4):
            if _generate_linkable_by_recursive(neighbours_statuses[i]):
                odds = random.randint(1, 100)
                if odds <= 50: # 50% chance of linking; 
                    neighbourcoords = [x + dirlist[i][0], y + dirlist[i][1]]
                    self._generate_link_rooms(thisroomcoords, neighbourcoords)
                    self._generate_recursive_linking(neighbourcoords) # recursion call
        # base case should be inherently built into this loop:
        # Recursion branch ends at a room where
        # 1. All adjacent rooms are not linkable
        # 2. By chance, the labyrinth chooses not to link this room to any other room.

    def _generate_linkable_by_recursive(self, room_status: dict) -> bool:
        if room_status is None:
            return False
        x, y = room_status["coords"]
        room_object = self.lab[x][y]
        if room_object.is_connected_to_start():
            return False
        return True
                     
    
    def _generate_link_rooms(self, room1coords: list[int], room2coords: list[int]) -> None:
        # validation
        posscoords = [i for i in range(labsize)]
        x1, y1, x2, y2 = room1coords + room2coords
        numbers = room1coords + room2coords
        for i in numbers:
            if i not in posscoords:
                raise IndexError("_generate_link_rooms(): a room passed in has coords outside of labyrinth. Cannot be linked.")
        if x1 == x2 and y1 == y2:
            raise IndexError("_generate_link_rooms(): the same room is passed twice, cannot be linked.")
        if not ((x1 == x2 and abs(y1 - y2) == 1) or (abs(x1 - x2) == 1 and y1 == y2)):
            raise IndexError("_generate_link_rooms(): non adjacent rooms are passed, cannot be linked.")
        # linking rooms
        room1 = self.lab[x1][y1]
        room2 = self.lab[x2][y2]
        if room1.is_connected_tostart() or room2.is_connected_tostart():
            room1.set_connected_True()
            room2.set_connected_True()
        if not room1.is_connected_tostart() and not room2.is_connected_tostart():
            # every linking must happen between rooms of which 1 MUST be connected.
            return None # no linking done if both are unconnected.
        if x1 == x2 and y1 < y2:
                room1.set_access_True(NORTH)
                room2.set_access_True(SOUTH)
        elif x1 == x2 and y1 > y2:
                room1.set_access_True(SOUTH)
                room2.set_access_True(NORTH)
        elif x1 < x2 and y1 == y2:
                room1.set_access_True(EAST)
                room2.set_access_True(WEST)
        elif x1 > x2 and y1 == y2:
                room1.set_access_True(WEST)
                room2.set_access_True(EAST)
            
    
    def _generate_count_unconnected_rooms(self) -> int:
        """
        One of many helper methods of the generate() method.
        
        Linearly search the rooms to check whether the rooms are connected to the startroom.
        Returns the number of rooms that are not connected.
        
        """
        number_of_unconnected = 0
        for column in self.lab:
            for room in column:
                # room is an instance of the Room class
                if not room.is_connected_tostart():
                    number_of_unconnected += 1 # counter
        return number_of_unconnected

    def move_boss(self) -> None:
        dirlist = [NORTH, SOUTH, EAST, WEST]
        random.shuffle(dirlist)
        for randomdir in dirlist:
            if  _can_move_here(boss_pos, randomdir):



                return None
                
    def move_steve(self, direction) -> bool:
        if _can_move_here(self.steve_pos):
            if direction == NORTH:
                return None
            if direction ==  SOUTH:
                return None
            if direction == EAST:
                return None
            if direction == WEST:
                return None        

    def _can_move_here(self, coords: list(int), direction):
        x, y = coords
        if x < 0 or x >= labsize or y < 0 or y >= labsize: # this should not happen at all
            raise IndexError("entity is not inside of maze")
        raise NotImplementedError
        if direction == NORTH:
            return False

    def _steve_useitem(self, item: Item) -> None:
        raise NotImplementedError

    def _monster_roar(self):
        raise NotImplementedError



class Room:
    """
    -- ATTRIBUTES --
    + coords: list[int]
    + type: dict
    + connected: bool
    + mynorth: dict
    + mysouth: dict
    + myeast: dict
    + mywest: dict

    
    -- METHODS --
    + settype_startroom(self) -> None
    + steve_leaves(self) -> None
    + steve_enters -> None
    + steve_leaves -> None
    + steve_enters -> None

    
    """
    def __init__(self, x: int, y: int):
        self.coords = [x, y]
        self.type = {"startroom?": False, "steve?": False, "creature": None, "item": None, "boss?": False}
        self.connected = False
        # setting mynorth, mysouth, myeast, mywest status attributes where possible
        if y + 1 >= labsize:
            self.mynorth = None
        else:
            self.mynorth = {"coords": [x, y + 1], "access": False}
        if y <= 0:
            self.mysouth = None
        else:
            self.mysouth = {"coords": [x, y - 1], "access": False}
        if x + 1 >= labsize:
            self.myeast = None
        else:
            self.myeast = {"coords": [x + 1, y], "access": False}
        if x <= 0:
            self.mywest = None
        else:
            self.mywest = {"coords": [x - 1, y], "access": False}

    def settype_startroom(self) -> None:
        self.type["startroom?"] = True
        self.type["steve?"] = True
        self.connected = True

    def steve_leaves(self) -> None:
        self.type["steve?"] = False

    def steve_enters(self) -> None:
        self.type["steve?"] = True

    def boss_leaves(self) -> None:
        self.type["boss?"] = False
            
    def boss_enters(self) -> None:
        self.type["boss?"] = True

    def set_connected_True(self) -> None:
        self.connected = True

    def set_access_True(direction) -> None:
        if direction == NORTH:
            if self.mynorth is None:
                raise ValueError(f'Room {self.coords} has no room to the north of it, access cannot be set.')
            self.mynorth["access"] = True
        elif direction == SOUTH:
            if self.mysouth is None:
                raise ValueError(f'Room {self.coords} has no room to the south of it, access cannot be set.')
            self.mysouth["access"] = True
        elif direction == EAST:
            if self.myeast is None:
                raise ValueError(f'Room {self.coords} has no room to the east of it, access cannot be set.')
            self.myeast["access"] = True
        elif direction == WEST:
            if self.mywest is None:
                raise ValueError(f'Room {self.coords} has no room to the west of it, access cannot be set.')
            self.mywest["access"] = True
        else:
            raise ValueError(f'Room {self.coords} set_access_True() had argument passed that is not a direction value.')

    def is_connected_tostartroom():
        return self.connected

    def get_neighbours_statuses():
        return [self.mynorth, self.mysouth, self.myeast, self.mywest]

class Item:
    """
    -- ATTRIBUTES --

    + self.info: dict
    
    -- METHODS --
    """
    def __init__(self):
        self.info = {}
        for i in ["name", "item type", "description"]:
            self.info[i] = None

    def __repr__(self) -> str:
        outputstr = ''
        for key, value in self.info.items():
            outputstr += key.capitalize() + ": " + value
        return outputstr

    def __str__(self) -> str:
        outputstr = ''
        for key, value in self.info.items():
            outputstr += key.capitalize() + ": " + value
        return outputstr

    def set_nametypedesc(self, name: str, type: str, desc: str) -> None:
        self.info["name"] = name
        self.info["type"] = type
        self.info["description"] = desc


DEFAULT_HITPOINTS = 20
class Steve:
    """
    -- ATTRIBUTES --
    
    -- METHODS --
    """
    def __init__(self, n: int):
        self._inventory = [] # list of dict
        # each dict in self.inventory describes an item, as well as the number of it in the inventory.
        # e.g. {"item": Health_Potion, "number": 2}
        # There should NOT be duplicate dicts in self.inventory e.g. 2 different dicts in self.inventory with "item" being Health_Potions
        self.inv_slots_num = n
        self.armour = {}
        for slot in ["helmet", "chestplate", "leggings", "boots"]:
            self.armour[i] = None
        self.health = DEFAULT_HITPOINTS

    def __repr__(self):
        return f"Steve has {self.heatlh} HP."

    def _display_inventory(self) -> None:
        raise NotImplementedError

    def _add_item_to_inv(new_item: Item, num: int) -> None:
        for index, dict_ in enumerate(self._inventory): # Linear search through inventory
            if str(new_item) == str(dict_["item"]): # new_item is already in the inventory
                self._inventory[index]["number"] += num
                return None
        # If exit loop, inventory does not have any of new_item
        # create a dict to add to self.inventory
        self.inventory.append({"item": new_item, "number": num})
        return None

    def _discard_item(item: Item, num: int) -> None:
        raise NotImplementedError

    def _equip_armour(self, armour_item: Item) -> None:
        raise NotImplementedError
        
    def _get_hurt(self, damage: int):
        raise NotImplementedError

    def isdead(self) -> bool:
        if self.health <= 0:
            return True
        return False
                

class Creature:
    """
    -- ATTRIBUTES --
    
    -- METHODS --
    """
    def __init__(self, ...):
        self.info = {}
        for i in ["name", "max hitpoints", "moves"]:
            self.info[i] = None
        self.hitpoints = None
        


    def set_name(self, name: str) -> None:
        self.info["name"] = name

    def set_maxhp(self, maxhp: int) -> None:
        self.info["max hitpoints"] = maxhp
        self.hitpoints = maxhp

    def set_moves(self, moveslist: list) -> None:
        self.info["moves"] = moveslist

    def set_creature(self, moves)


class Monster(Creature):
    """
    -- ATTRIBUTES --
    
    -- METHODS --
    """
    def __init__(self):
        

with open("content/items.json", "r") as f:
    items = json.load(f)

28