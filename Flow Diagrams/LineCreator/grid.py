

class Grid:
    def __init__(self, x_size=300, y_size=300, d_sep=10):
        # Each grid contains cells which are identified by their top left coord.
        # Given an ID (x,y), lookup that ID in a hashmap to find a list
        # containing points in that cell
        
        self.x_size = x_size
        self.y_size = y_size
        self.map = {}
        self.d_sep = d_sep

        for y in range(0, y_size, d_sep):
            for x in range(0, x_size, d_sep):
                ID = (x, y)
                self.map[ID] = []
    
    def get_cell(self, ID): # Return list of specific cell
        if ID in self.map:
            return self.map[ID]
        else:
            return []

    def reset(self):
        self.__init__(self.x_size, self.y_size, self.d_sep)

    def find_cell_ID(self, pt): # Return cell ID from point
        # (14, 27), cell ID is (10, 20), d_sep = 10
        x = pt[0] - (pt[0] % self.d_sep) # 14 - (14 % 10) = 10
        y = pt[1] - (pt[1] % self.d_sep) # 27 - (27 % 10) = 20
        return (int(x), int(y))

    def add_to_cell(self, pt): # Find the cell a point is in and add it to that cell
        ID = self.find_cell_ID(pt)
        if pt not in self.map[ID]:
            self.map[ID].append(pt)

    def get_neighbor_cell_points(self, pt):
        ID = self.find_cell_ID(pt)
        lst = []
        lst += self.get_cell(ID) # Middle
        lst += self.get_cell((ID[0] - self.d_sep, ID[1] - self.d_sep)) # TL
        lst += self.get_cell((ID[0], ID[1] - self.d_sep)) # T
        lst += self.get_cell((ID[0] + self.d_sep, ID[1] - self.d_sep)) # TR
        lst += self.get_cell((ID[0] - self.d_sep, ID[1])) # L
        lst += self.get_cell((ID[0] + self.d_sep, ID[1])) # R
        lst += self.get_cell((ID[0] - self.d_sep, ID[1] + self.d_sep)) # BL
        lst += self.get_cell((ID[0], ID[1] + self.d_sep)) # B
        lst += self.get_cell((ID[0] + self.d_sep, ID[1] + self.d_sep)) # BR
        return lst
        


if __name__ == "__main__":
    g = Grid(400, 400, 10)
    for t in g.map.keys():
        print(t)
