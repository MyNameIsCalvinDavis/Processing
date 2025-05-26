
HASH_TO_TILE = {}
TILE_TO_HASH = {}
HASH_TO_NAME = {} # 123123123 : "AA", printing purposes only
_NAMES = [x+y for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for y in "1234567890"]

class Tile:
    """
    A Tile represents a sliced-out chunk from an image. A Cell's domain contains multiple Tiles
    """
    
    def __init__(self, color_rows):
        self.data = color_rows # NxN list of color values
        
        HASH_TO_TILE[self.hash()] = self
        TILE_TO_HASH[self] = self.hash()
        for name in _NAMES:
            if name not in list(HASH_TO_NAME.values()):
                HASH_TO_NAME[self.hash()] = name
                break
        else:
            raise # Run out of tile names, add more
        
    def hash(self):
        return hash(self.data)
    
    def __str__(self):
        return HASH_TO_NAME[self.hash()]
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        # I want collisions on identical data
        return self.hash()
    
    def __del__(self):
        # I anticipate this being called when I try to add a Tile to a dict,
        # and it collides with an existing Tile, and disappears
        print("This tile is being deleted from memory", self.hash())