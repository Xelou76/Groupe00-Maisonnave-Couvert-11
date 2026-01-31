import random

class Minesweeper:
    def __init__(self, width=10, height=10, num_mines=10):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.grid = set() # Set of (x,y) tuples for mines
        self.revealed = set() # Set of revealed cells
        self.flags = set() # Set of flagged cells
        self._generate_mines()

    def _generate_mines(self):
        while len(self.grid) < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.grid.add((x, y))

    def get_neighbors(self, x, y):
        # Retourne les voisins valides (8 directions)
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))
        return neighbors

    def get_value(self, x, y):
        # Retourne le nombre de mines autour
        if (x, y) in self.grid: return -1 # C'est une mine
        count = 0
        for nx, ny in self.get_neighbors(x, y):
            if (nx, ny) in self.grid:
                count += 1
        return count
    
    def reveal(self, x, y):
        self.revealed.add((x, y))
        return (x, y) in self.grid # Retourne True si BOOM