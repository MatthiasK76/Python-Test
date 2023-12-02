import matplotlib.pyplot as plt
import numpy as np
import random


class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[1.0] * cols for _ in range(rows)]  # 0 repräsentiert einen freien Weg, 1 repräsentiert eine Wand

    def unset_wall(self, row, col, val=0.0):
        self.grid[row][col] = val

    def __str__(self):
        maze_str = ""
        for row in self.grid:
            maze_str += " ".join(map(str, row)) + "\n"
        return maze_str

class MazeGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = Maze(rows, cols)
        self.t = 0.0
        self.dt = (1.0/8.0)
        self.maxt = 0.8

    def generate_maze(self):

        start_row=random.randint(0,self.rows//2)*2
        start_col=random.randint(0,self.cols//2)*2

        stack = [(start_row, start_col)]
        visited = set([(start_row, start_col)])

        while stack:
            current_row, current_col = stack[-1]

            # Finde unbesuchte Nachbarn
            neighbors = self.get_unvisited_neighbors(current_row, current_col, visited)
            
            if neighbors:
                # Zufällig einen Nachbarn auswählen
                next_row, next_col = random.choice(neighbors)

                # Entferne die Wand zwischen den Zellen
                self.remove_wall(current_row, current_col, next_row, next_col)

                # Markiere die Zelle als besucht
                visited.add((next_row, next_col))

                # Füge die nächste Zelle dem Stack hinzu
                stack.append((next_row, next_col))
            else:
                # Backtrack, wenn keine unbesuchten Nachbarn vorhanden sind
                stack.pop()
                self.t+=self.dt
                if self.t > self.maxt: 
                    self.t = 0.0


    def get_unvisited_neighbors(self, row, col, vis):
        neighbors = []
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Rechts, Unten, Links, Oben

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and (new_row, new_col) not in vis:
                neighbors.append((new_row, new_col))

        return neighbors

    def remove_wall(self, current_row, current_col, next_row, next_col):
        # Entferne die Wand zwischen zwei Zellen
        if current_row==next_row:
            if current_col < next_col:
                for dc in range (current_col, next_col+1):
                    self.maze.unset_wall(current_row, dc, self.t)
            else:
                for dc in range (next_col, current_col+1):
                    self.maze.unset_wall(current_row, dc, self.t)                
        elif current_col==next_col:
            if current_row < next_row:
                for dr in range (current_row, next_row+1):
                    self.maze.unset_wall(dr, current_col, self.t)
            else:
                for dr in range (next_row, current_row+1):
                    self.maze.unset_wall(dr, current_col, self.t)
            

def draw_maze_with_matplotlib(maze):
    plt.imshow(maze.grid, cmap='Accent', interpolation='nearest')
    plt.xticks([]), plt.yticks([])  # Deaktiviere Achsenbeschriftungen
    plt.show()

# Beispiel für die Verwendung des MazeGenerator und die Darstellung des Labyrinths
rows = 30
cols = 30
cell_size = 20

maze_generator = MazeGenerator(2*rows+1, 2*cols+1)
maze_generator.generate_maze()

print("Generiertes Labyrinth:")
print(maze_generator.maze)

draw_maze_with_matplotlib(maze_generator.maze)
