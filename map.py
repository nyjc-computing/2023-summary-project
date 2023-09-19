import platform
class game_map:
    """
    Attributes:
    - map: contains the map for the game
    - self.e_trigger: records whether the enter event for a room has been called before
      in order to avoid screwing up the map, each enter event should be called only once,
      and in a specific order
    Methods:
    - each room has two map update events
        - one is for when the player enters the room for the first time
        - the other is for when the players has done everything in the room
    """

    def __init__(self):
        self.map = [[" " for x in range(130)] for x in range(32)]
        self.e_trigger = [0] * 29
        self.secret_trigger = 0
        self.current_color = "red"

    def make_room(self, y: int, x: int, name: str) -> None:
        """
        draws a box, centered on coords (x,y) on the map
        name is the name of the room
        """
        layer1 = "┌" + "─"*len(name) + "┐"
        layer2 = "│" + name + "│"
        layer3 = "└"+ "─"*len(name) + "┘"
        box = [layer1, layer2, layer3]
        x = x - int(len(name)/2) - 1
        y = y - 1
        for row in range(3):
            for column in range(2+len(name)):
                self.map[row + y][column + x] = box[row][column]

    def finish_room(self, y: int, x: int, name: str) -> None:
        """
        draws a bold box, centered on coords (x,y) on the map
        name is the name of the room
        """

        layer1 = "┌" + "─"*len(name) + "*"
        layer2 = "│" + name + "│"
        layer3 = "└"+ "─"*len(name) + "┘"

        box = [layer1, layer2, layer3]
        x = x - int(len(name)/2) - 1
        y = y - 1
        for row in range(3):
            for column in range(2+len(name)):
                self.map[row + y][column + x] = box[row][column]

    def hconnect(self, y: int, x: int, l: int) -> None:
        """
        draws a horizontal connector from (x,y) to (x+l,y)
        """
        self.map[y][x] = "╠"
        for i in range(l):
            self.map[y][x+1+i] = "═"
        self.map[y][x+1+l] = "╣"

    def vconnect(self, y: int, x: int, l: int) -> None:
        """
        draws a vertical connector from (x,y) to (x,y+l)
        """
        self.map[y][x] = "╦"
        for i in range(l):   
            self.map[y+1+i][x] = "║"
        self.map[y+1+l][x] = "╩"
    
    def current(self, y, x, name):
        x = x - int(len(name)/2) - 1
        tag1 = [self.current_color, f"{y}.{x}", f"{y}.{x+len(name)+2}"]
        tag2 = [self.current_color, f"{y+1}.{x}", f"{y+1}.{x+len(name)+2}"]
        tag3 = [self.current_color, f"{y+2}.{x}", f"{y+2}.{x+len(name)+2}"]
        return [tag1, tag2, tag3]
                
    def dirtmouth_enter(self) -> None:
        """
        updates map for first time visiting dirtmouth
        """
        if self.e_trigger[0] != 0:
            return
        self.e_trigger[0] = 1
        #make room
        self.make_room(10,60,"Dirtmouth")
        
        #make hidden rooms
        self.make_room(10,51," ? ")
        self.make_room(10,69," ? ")
        self.make_room(6,60, " ? ")

        #(re)make paths
        self.hconnect(10,53,1)
        self.hconnect(10,65,1)
        self.vconnect(7,60,1)

    def dirtmouth_clear(self) -> None:
        """
        updates map for fully clearing dirtmouth
        """
        #make room
        self.finish_room(10,60,"Dirtmouth")

        #(re)make paths
        self.hconnect(10,53,1)
        self.hconnect(10,65,1)
        self.vconnect(7,60,1)

    def dirtmouth_current(self):
        return self.current(10,60,"Dirtmouth")

    def end_dimension_enter(self) -> None:
        """
        updates map for first time visiting the end
        """
        if self.e_trigger[1] != 0:
            return
        self.e_trigger[1] = 1
        #make room
        self.make_room(6,60,"The End Dimension")
        
        #make hidden rooms
        self.make_room(2,60, " ? ")

        #(re)make paths
        self.vconnect(3,60,1)
        self.vconnect(7,60,1)

    def end_dimension_clear(self) -> None:
        """
        updates map for fully clearing the end
        """
        #make room
        self.finish_room(6,60,"The End Dimension")

        #(re)make paths
        self.vconnect(3,60,1)
        self.vconnect(7,60,1)

    def end_dimension_current(self):
        return self.current(6,60,"The End Dimension")

    def hyrule_enter(self) -> None:
        """
        updates map for first time visiting hyrule
        """
        if self.e_trigger[2] != 0:
            return
        self.e_trigger[2] = 1
        #make room
        self.make_room(10,75,"Hyrule Kingdom")
        
        #make hidden rooms
        self.make_room(14,75, " ? ")

        #(re)make paths
        self.hconnect(10,65,1)
        self.vconnect(11,75,1)

    def hyrule_clear(self) -> None:
        """
        updates map for fully clearing hyrule
        """
        #make room
        self.finish_room(10,75,"Hyrule Kingdom")

        #(re)make paths
        self.hconnect(10,65,1)
        self.vconnect(11,75,1)

    def hyrule_current(self):
        return self.current(10,75,"Hyrule Kingdom")

    def celestial_resort_enter(self) -> None:
        """
        updates map for first time visiting celestial resort
        """
        if self.e_trigger[3] != 0:
            return
        self.e_trigger[3] = 1
        #make room
        self.make_room(14,75,"Celestial Resort")
        
        #make hidden rooms
        self.make_room(18,75, " ? ")

        #(re)make paths
        self.vconnect(11,75,1)
        self.vconnect(15,75,1)

    def celestial_resort_clear(self) -> None:
        """
        updates map for fully clearing celestial resort
        """
        #make room
        self.finish_room(14,75,"Celestial Resort")

        #(re)make paths
        self.vconnect(11,75,1)
        self.vconnect(15,75,1)

    def celestial_resort_current(self):
        return self.current(14,75,"Celestial Resort")

    def sixth_circle_enter(self) -> None:
        """
        updates map for first time visiting 6th circle of hell
        """
        if self.e_trigger[4] != 0:
            return
        self.e_trigger[4] = 1
        #make room
        self.make_room(18,75,"6th Circle Of Hell")

        #make hidden rooms
        self.make_room(18,92," ? ")

        #(re)make paths
        self.vconnect(15,75,1)
        self.hconnect(18,84,5)

    def sixth_circle_clear(self) -> None:
        """
        updates map for fully clearing 6th circle of hell
        """
        #make room
        self.finish_room(18,75,"6th Circle Of Hell")

        #(re)make paths
        self.vconnect(15,75,1)
        self.hconnect(18,84,5)

    def sixth_circle_current(self):
        return self.current(18,75,"6th Circle Of Hell")

    def ascent_enter(self) -> None:
        """
        updates map for first time visiting ascent
        """
        if self.e_trigger[5] != 0:
            return
        self.e_trigger[5] = 1
        #make room
        self.make_room(18,94,"Ascent")

        #make hidden rooms
        self.make_room(14,94," ? ")
        self.make_room(18,107," ? ")

        #(re)make paths
        self.hconnect(18,84,5)
        self.hconnect(18,97,7)
        self.vconnect(15,94,1)

    def ascent_clear(self) -> None:
        """
        updates map for fully clearing ascent
        """
        #make room
        self.finish_room(18,94,"Ascent")

        #(re)make paths
        self.hconnect(18,84,5)
        self.hconnect(18,97,7)
        self.vconnect(15,94,1)

    def ascent_current(self):
        return self.current(18,94,"Ascent")

    def tower_enter(self) -> None:
        """
        updates map for first time visiting tower of fate
        """
        if self.e_trigger[6] != 0:
            return
        self.e_trigger[6] = 1
        #make room
        self.make_room(14,94,"Tower of Fate")

        #make hidden rooms

        #(re)make paths
        self.vconnect(15,94,1)

    def tower_clear(self) -> None:
        """
        updates map for fully clearing tower of fate
        """
        #make room
        self.finish_room(14,94,"Tower of Fate")

        #(re)make paths
        self.vconnect(15,94,1)

    def tower_current(self):
        return self.current(14,94,"Tower of Fate")

    def haligtree_enter(self) -> None:
        """
        updates map for first time visiting Miquella's Haligtree
        """
        if self.e_trigger[7] != 0:
            return
        self.e_trigger[7] = 1
        #make room
        self.make_room(18,116,"Miquella's Haligtree")

        #make hidden rooms
        self.make_room(14,114," ? ")
        self.make_room(25,114," ? ")

        #(re)make paths
        self.vconnect(15,114,1)
        self.vconnect(19,114,4)
        self.hconnect(18,97,7)

    def haligtree_clear(self) -> None:
        """
        updates map for fully clearing Miquella's Haligtree
        """
        #make room
        self.finish_room(18,116,"Miquella's Haligtree")

        #(re)make paths
        self.vconnect(15,114,1)
        self.vconnect(19,114,4)
        self.hconnect(18,97,7)

    def haligtree_current(self):
        return self.current(18,116,"Miquella's Haligtree")

    def hallow_enter(self) -> None:
        """
        updates map for first time visiting the hallow
        """
        if self.e_trigger[8] != 0:
            return
        self.e_trigger[8] = 1
        #make room
        self.make_room(14,114,"The Hallow")

        #make hidden rooms
        self.make_room(10,114," ? ")

        #(re)make paths
        self.vconnect(15,114,1)
        self.vconnect(11,114,1)

    def hallow_clear(self) -> None:
        """
        updates map for fully clearing the hallow
        """
        #make room
        self.finish_room(14,114,"The Hallow")

        #(re)make paths
        self.vconnect(15,114,1)
        self.vconnect(11,114,1)

    def hallow_current(self):
        return self.current(14,114,"The Hallow")

    def obradinn_enter(self) -> None:
        """
        updates map for first time visiting the obra dinn
        """
        if self.e_trigger[9] != 0:
            return
        self.e_trigger[9] = 1
        #make room
        self.make_room(10,114,"The Obra Dinn")

        #make hidden rooms

        #(re)make paths
        self.vconnect(11,114,1)

    def obradinn_clear(self) -> None:
        """
        updates map for fully clearing the obra dinn
        """
        #make room
        self.finish_room(10,114,"The Obra Dinn")

        #make hidden rooms

        #(re)make paths
        self.vconnect(11,114,1)

    def obradinn_current(self):
        return self.current(10,114,"The Obra Dinn")

    def kamurocho_enter(self) -> None:
        """
        updates map for first time visiting kamurocho
        """
        if self.e_trigger[10] != 0:
            return
        self.e_trigger[10] = 1
        #make room
        self.make_room(25,114,"Kamurocho")

        #make hidden rooms
        self.make_room(25,102," ? ")

        #(re)make paths
        self.vconnect(19,114,4)
        self.hconnect(25,104,4)

    def kamurocho_clear(self) -> None:
        """
        updates map for fully clearing kamurocho
        """
        #make room
        self.finish_room(25,114,"Kamurocho")

        #make hidden rooms

        #(re)make paths
        self.vconnect(19,114,4)
        self.hconnect(25,104,4)

    def kamurocho_current(self):
        return self.current(25,114,"Kamurocho")

    def snowdin_enter(self) -> None:
        """
        updates map for first time visiting snowdin
        """
        if self.e_trigger[11] != 0:
            return
        self.e_trigger[11] = 1
        #make room
        self.make_room(25,100,"Snowdin")

        #make hidden rooms
        self.make_room(25,89," ? ")
        self.make_room(21,100," ? ")
        self.make_room(29,100," ? ")

        #(re)make paths
        self.hconnect(25,104,4)
        self.hconnect(25,91,4)
        self.vconnect(22,100,1)
        self.vconnect(26,100,1)

    def snowdin_clear(self) -> None:
        """
        updates map for fully clearing snowdin
        """
        #make room
        self.finish_room(25,100,"Snowdin")

        #(re)make paths
        self.hconnect(25,104,4)
        self.hconnect(25,91,4)
        self.vconnect(22,100,1)
        self.vconnect(26,100,1)

    def snowdin_current(self):
        return self.current(25,100,"Snowdin")

    def aperture_enter(self) -> None:
        """
        updates map for first time visiting aperture
        """
        if self.e_trigger[12] != 0:
            return
        self.e_trigger[12] = 1
        #make room
        self.make_room(25,84,"Aperture Labs")

        #make hidden rooms

        #(re)make paths
        self.hconnect(25,91,4)

    def aperture_clear(self) -> None:
        """
        updates map for fully clearing aperture
        """
        #make room
        self.finish_room(25,84,"Aperture Labs")

        #make hidden rooms

        #(re)make paths
        self.hconnect(25,91,4)

    def aperture_current(self):
        return self.current(25,84,"Aperture Labs")

    def astral_plane_enter(self) -> None:
        """
        updates map for first time visiting the astral plane
        """
        if self.e_trigger[13] != 0:
            return
        self.e_trigger[13] = 1
        #make room
        self.make_room(21,100,"The Astral Plane")

        #make hidden rooms

        #(re)make paths
        self.vconnect(22,100,1)

    def astral_plane_clear(self) -> None:
        """
        updates map for fully clearing the astral plane
        """
        #make room
        self.finish_room(21,100,"The Astral Plane")

        #(re)make paths
        self.vconnect(22,100,1)

    def astral_plane_current(self):
        return self.current(21,100,"The Astral Plane")

    def sealed_temple_enter(self) -> None:
        """
        updates map for first time visiting the sealed temple
        """
        if self.e_trigger[14] != 0:
            return
        self.e_trigger[14] = 1
        #make room
        self.make_room(29,100,"The Sealed Temple")

        #make hidden rooms

        #(re)make paths
        self.vconnect(26,100,1)

    def sealed_temple_clear(self) -> None:
        """
        updates map for fully clearing the sealed temple
        """
        #make room
        self.finish_room(29,100,"The Sealed Temple")

        #(re)make paths
        self.vconnect(26,100,1)

    def sealed_temple_current(self):
        return self.current(29,100,"The Sealed Temple")

    def midgar_enter(self) -> None:
        """
        updates map for first time visiting midgar
        """
        if self.e_trigger[15] != 0:
            return
        self.e_trigger[15] = 1
        #make room
        self.make_room(10,50,"Midgar")

        #make hidden rooms
        self.make_room(10,42," ? ")

        #(re)make paths
        self.hconnect(10,53,1)
        self.hconnect(10,44,1)

    def midgar_clear(self) -> None:
        """
        updates map for fully clearing midgar
        """
        #make room
        self.finish_room(10,50,"Midgar")

        #make hidden rooms

        #(re)make paths
        self.hconnect(10,53,1)
        self.hconnect(10,44,1)

    def midgar_current(self):
        return self.current(10,50,"Midgar")

    def forge_enter(self) -> None:
        """
        updates map for first time visiting the forge
        """
        if self.e_trigger[16] != 0:
            return
        self.e_trigger[16] = 1
        #make room
        self.make_room(10,39,"The Forge")

        #make hidden rooms
        self.make_room(6,39," ? ")

        #(re)make paths
        self.hconnect(10,44,1)
        self.vconnect(7,39,1)

    def forge_clear(self) -> None:
        """
        updates map for fully clearing the forge
        """
        #make room
        self.finish_room(10,39,"The Forge")

        #(re)make paths
        self.hconnect(10,44,1)
        self.vconnect(7,39,1)

    def forge_current(self):
        return self.current(10,39,"The Forge")

    def mementos_enter(self) -> None:
        """
        updates map for first time visiting mementos
        """
        if self.e_trigger[17] != 0:
            return
        self.e_trigger[17] = 1
        #make room
        self.make_room(6,39,"Mementos")

        #make hidden rooms
        self.make_room(2,39," ? ")
        self.make_room(6,27," ? ")

        #(re)make paths
        self.vconnect(7,39,1)
        self.vconnect(3,39,1)
        self.hconnect(6,29,4)

    def mementos_clear(self) -> None:
        """
        updates map for fully clearing mementos
        """
        #make room
        self.finish_room(6,39,"Mementos")

        #(re)make paths
        self.vconnect(7,39,1)
        self.vconnect(3,39,1)
        self.hconnect(6,29,4)

    def mementos_current(self):
        return self.current(6,39,"Mementos")

    def shores_enter(self) -> None:
        """
        updates map for first time visiting shores of 9
        """
        if self.e_trigger[18] != 0:
            return
        self.e_trigger[18] = 1
        #make room
        self.make_room(2,39,"Shores of Nine")

        #make hidden rooms

        #(re)make paths
        self.vconnect(3,39,1)

    def shores_clear(self) -> None:
        """
        updates map for fully clearing shores of 9
        """
        #make room
        self.finish_room(2,39,"Shores of Nine")

        #make hidden rooms

        #(re)make paths
        self.vconnect(3,39,1)

    def shores_current(self):
        return self.current(2,39,"Shores of Nine")

    def asphodel_enter(self) -> None:
        """
        updates map for first time visiting asphodel
        """
        if self.e_trigger[19] != 0:
            return
        self.e_trigger[19] = 1
        #make room
        self.make_room(6,25,"Asphodel")

        #make hidden rooms
        self.make_room(6,13," ? ")
        self.make_room(14,30," ? ")

        #(re)make paths
        self.hconnect(6,29,4)
        self.hconnect(6,15,4)
        self.vconnect(7,25,6)
        self.hconnect(14,25,2)
        self.map[14][25] = "╚"

    def asphodel_clear(self) -> None:
        """
        updates map for fully clearing asphodel
        """
        #make room
        self.finish_room(6,25,"Asphodel")

        #(re)make paths
        self.hconnect(6,29,4)
        self.hconnect(6,15,4)
        self.vconnect(7,25,6)
        self.hconnect(14,25,2)
        self.map[14][25] = "╚"

    def asphodel_current(self):
        return self.current(6,25,"Asphodel")

    def commencement_enter(self) -> None:
        """
        updates map for first time visiting commencement
        """
        if self.e_trigger[20] != 0:
            return
        self.e_trigger[20] = 1
        #make room
        self.make_room(6,9,"Commencement")

        #make hidden rooms
        self.make_room(10,8," ? ")

        #(re)make paths
        self.hconnect(6,15,4)
        self.vconnect(7,8,1)

    def commencement_clear(self) -> None:
        """
        updates map for fully clearing commencement
        """
        #make room
        self.finish_room(6,9,"Commencement")

        #(re)make paths
        self.hconnect(6,15,4)
        self.vconnect(7,8,1)

    def commencement_current(self):
        return self.current(6,9,"Commencement")

    def walled_enter(self) -> None:
        """
        updates map for first time visiting walled city 99
        """
        if self.e_trigger[21] != 0:
            return
        self.e_trigger[21] = 1
        #make room
        self.make_room(10,9,"Walled City 99")

        #make hidden rooms

        #(re)make paths
        self.vconnect(7,8,1)

    def walled_clear(self) -> None:
        """
        updates map for fully clearing walled city 99
        """
        #make room
        self.finish_room(10,9,"Walled City 99")

        #(re)make paths
        self.vconnect(7,8,1)
        self.vconnect(11,10,1)

    def walled_current(self):
        return self.current(10,9,"Walled City 99")

    def meow_reveal(self) -> None:
        """
        shows hidden room after unlocking secret
        """
        if self.secret_trigger == 0:
            #make hidden room
            self.make_room(14,10," ? ")
    
            #(re)make paths
            self.vconnect(11,10,1)
            
            self.secret_trigger = 1

    def last_resort_enter(self) -> None:
        """
        updates map for first time visiting the last resort
        """
        if self.e_trigger[22] != 0:
            return
        self.e_trigger[22] = 1
        #make room
        self.make_room(14,10,"The Last Resort")

        #make hidden rooms

        #(re)make paths
        self.vconnect(11,10,1)

    def last_resort_clear(self) -> None:
        """
        updates map for fully clearing the last resort
        """
        #make room
        self.finish_room(14,10,"The Last Resort")

        #(re)make paths
        self.vconnect(11,10,1)

    def last_resort_current(self):
        return self.current(14,10,"The Last Resort")

    def greenhill_enter(self) -> None:
        """
        updates map for first time visiting greenhill zone
        """
        if self.e_trigger[23] != 0:
            return
        self.e_trigger[23] = 1
        #make room
        self.make_room(14,36,"Greenhill Zone")

        #make hidden rooms
        self.make_room(18,36," ? ")
        self.make_room(14,48," ? ")

        #(re)make paths
        self.vconnect(7,25,6)
        self.hconnect(14,25,2)
        self.map[14][25] = "╚"
        self.hconnect(14,43,2)
        self.vconnect(15,36,1)

    def greenhill_clear(self) -> None:
        """
        updates map for fully clearing greenhill zone
        """
        #make room
        self.finish_room(14,36,"Greenhill Zone")

        #(re)make paths
        self.vconnect(7,25,6)
        self.hconnect(14,25,2)
        self.map[14][25] = "╚"
        self.hconnect(14,43,2)
        self.vconnect(15,36,1)

    def greenhill_current(self):
        return self.current(14,36,"Greenhill Zone")
        
    def mushroom_enter(self) -> None:
        """
        updates map for first time visiting the mushroom kingdom
        """
        if self.e_trigger[24] != 0:
            return
        self.e_trigger[24] = 1
        #make room
        self.make_room(14,55,"Mushroom Kingdom")

        #make hidden rooms

        #(re)make paths
        self.hconnect(14,43,2)

    def mushroom_clear(self) -> None:
        """
        updates map for fully clearing mushroom kingdom
        """
        #make room
        self.finish_room(14,55,"Mushroom Kingdom")

        #make hidden rooms

        #(re)make paths
        self.hconnect(14,43,2)

    def mushroom_current(self):
        return self.current(14,55,"Mushroom Kingdom")

    def kingdom_ku_enter(self) -> None:
        """
        updates map for first time visiting kingdom of ku
        """
        if self.e_trigger[25] != 0:
            return
        self.e_trigger[25] = 1
        #make room
        self.make_room(18,36,"The Kingdom of Ku")

        #make hidden rooms
        self.make_room(18,49," ? ")
        self.make_room(18,23," ? ")

        #(re)make paths
        self.vconnect(15,36,1)
        self.hconnect(18,45,1)
        self.hconnect(18,25,1)

    def kingdom_ku_clear(self) -> None:
        """
        updates map for fully clearing kingdom of ku
        """
        #make room
        self.finish_room(18,36,"The Kingdom of Ku")

        #(re)make paths
        self.vconnect(15,36,1)
        self.hconnect(18,45,1)
        self.hconnect(18,25,1)

    def kingdom_ku_current(self):
        return self.current(18,36,"The Kingdom of Ku")

    def zebes_enter(self) -> None:
        """
        updates map for first time visiting zebes
        """
        if self.e_trigger[26] != 0:
            return
        self.e_trigger[26] = 1
        #make room
        self.make_room(18,50,"Zebes")

        #make hidden rooms

        #(re)make paths
        self.hconnect(18,45,1)

    def zebes_clear(self) -> None:
        """
        updates map for fully clearing zebes
        """
        #make room
        self.finish_room(18,50,"Zebes")

        #make hidden rooms

        #(re)make paths
        self.hconnect(18,45,1)

    def zebes_current(self):
        return self.current(18,50,"Zebes")

    def bunker_enter(self) -> None:
        """
        updates map for first time visiting bunker
        """
        if self.e_trigger[27] != 0:
            return
        self.e_trigger[27] = 1
        #make room
        self.make_room(18,22,"Bunker")

        #make hidden rooms

        #(re)make paths
        self.hconnect(18,25,1)

    def bunker_clear(self) -> None:
        """
        updates map for fully clearing bunker
        """
        #make room
        self.finish_room(18,22,"Bunker")

        #make hidden rooms

        #(re)make paths
        self.hconnect(18,25,1)
    
    def bunker_current(self):
        return self.current(18,22,"Bunker")

    def office_enter(self) -> None:
        """
        updates map for first time visiting principals office
        """
        if self.e_trigger[28] != 0:
            return
        self.e_trigger[28] = 1
        #make room
        self.make_room(2,60,"Principal's Office")

        #make hidden rooms

        #(re)make paths
        self.vconnect(3,60,1)

    def office_clear(self) -> None:
        """
        updates map for fully clearing principals office
        """
        #make room
        self.finish_room(2,60,"Principal's Office")

        #make hidden rooms

        #(re)make paths
        self.vconnect(3,60,1)

    def office_current(self):
        return self.current(2,60,"Principal's Office")

    def full_reveal(self) -> None:
        """
        Fully reveals the map
        """
        self.dirtmouth_enter()
        self.end_dimension_enter()
        self.office_enter()
        self.hyrule_enter()
        self.celestial_resort_enter()
        self.sixth_circle_enter()
        self.ascent_enter()
        self.tower_enter()
        self.haligtree_enter()
        self.hallow_enter()
        self.obradinn_enter()
        self.kamurocho_enter()
        self.snowdin_enter()
        self.sealed_temple_enter()
        self.astral_plane_enter()
        self.aperture_enter()
        self.midgar_enter()
        self.forge_enter()
        self.mementos_enter()
        self.shores_enter()
        self.asphodel_enter()
        self.commencement_enter()
        self.walled_enter()
        self.last_resort_enter()
        self.greenhill_enter()
        self.mushroom_enter()
        self.kingdom_ku_enter()
        self.zebes_enter()
        self.bunker_enter()
        
    def full_clear(self) -> None:
        """
        Fully clears the map
        """
        self.dirtmouth_clear()
        self.end_dimension_clear()
        self.office_clear()
        self.hyrule_clear()
        self.celestial_resort_clear()
        self.sixth_circle_clear()
        self.ascent_clear()
        self.tower_clear()
        self.haligtree_clear()
        self.hallow_clear()
        self.obradinn_clear()
        self.kamurocho_clear()
        self.snowdin_clear()
        self.sealed_temple_clear()
        self.astral_plane_clear()
        self.aperture_clear()
        self.midgar_clear()
        self.forge_clear()
        self.mementos_clear()
        self.shores_clear()
        self.asphodel_clear()
        self.commencement_clear()
        self.walled_clear()
        self.last_resort_clear()
        self.greenhill_clear()
        self.mushroom_clear()
        self.kingdom_ku_clear()
        self.zebes_clear()
        self.bunker_clear()


