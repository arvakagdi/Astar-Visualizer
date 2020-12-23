import pygame

# RED = (	255, 142, 113)
GREENE = (0, 220, 0)
BLUE = (86, 85, 110)
RED = (	220, 0, 0)
WHITEB =(240, 240, 240)

# WHITE = (233, 226, 222)
WHITE = (0, 0, 0)
YELLOW = (220, 220, 0)
ORANGE = (255, 165 ,0)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # to make a cube on screen we need to get the row and col and then place cube by multiplying it with the width depending upon the size of grid we want
        # ex: we want a 50*50 grid and our screen is 800*800 so, 800/50 ~ 16
        # if we are at 2nd row and 2nd col our x and y is 2*16 = 32 so our location is (32,32)
        self.x = row * width 
        self.y = col * width
        self.color = WHITE   # starting color
        self.neighbors = []  # neighbors of each node
        self.width = width
        self.total_rows = total_rows

    # Getters
    # get position
    def get_pos(self):
        return self.row, self.col

    # check if node is visited. RED nodes are already visited
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == YELLOW

    def is_barrier(self):
        return self.color == WHITEB

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    # setters
    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = YELLOW

    def make_barrier(self):
        self.color = WHITEB

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = GREENE

    # where you want to draw
        # draw rectangle (where-surface, color, coords, width)
    def draw(self, win):
        pygame.draw.rect(win,self.color,(self.x, self.y, self.width, self.width))  

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])   # add below row to neighbors
        
        if self.row  > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
                self.neighbors.append(grid[self.row - 1][self.col])   # add above row to neighbors
        
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
                self.neighbors.append(grid[self.row][self.col + 1])   # add right row to neighbors
        
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
                self.neighbors.append(grid[self.row][self.col - 1])   # add left row to neighbors

    def __lt__(self, other):
        return False