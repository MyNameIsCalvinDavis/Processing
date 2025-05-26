# PY5 IMPORTED MODE CODE
import random

WEIGHTS = {}

class Cell:
    """
    Abstraction for Tile superposition
    """
    
    def __init__(self, d, pos):
        self.domain = d
        self.pos = pos
        self.value = None
        self.se = 0
        
    def __str__(self):
        return str(len(self.domain))
    
    def __repr__(self):
        return self.__str__()

    def shannonEntropy(self):
        result = 0
        for t in self.domain:
            result += WEIGHTS[t] * log(WEIGHTS[t])
        self.se = round(-result, 4)
        
    def collapse(self):
        # Collapse the cell into a single domain, chosen randomly & weighted
        #print("Collapsing", self.pos, self.__str__())
        
        weights = []
        list_domain = list(self.domain) # Sets are unordered
        if len(self.domain) == 0: raise
        for col in list_domain:
            weights.append(WEIGHTS[str(col)]*10)
        collapsed_value = random.choices(list_domain, weights=weights)
        self.domain = set(collapsed_value)
        self.shannonEntropy()
        self.value = collapsed_value[0]
        
        #print("VAL:", self.value, type(self.value)) # Should be a tile not str
        #print("Final value for collapsed cell", self.pos, self.value)
        

if __name__ == "__main__":
    print("Cell.py can't be run standalone")