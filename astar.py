import pygame
import math
from queue import PriorityQueue # to get min number value nodes as PQ uses heap
from node import Node   # node class

GREY = (41, 41, 41)
BLACK = (0, 0, 0)
WIDTH = 800   # global var for width
WIN = pygame.display.set_mode((WIDTH,WIDTH))   # set size of window
pygame.display.set_caption("A* Path Finding Algorithm Visualizer")   # set up caption for the window

# HEuristic function
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x2 - x1) + abs(y2 - y1)

def reconstruct_path(parent_node, current, draw):
    while current in parent_node:
        current = parent_node[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start,end):
    count = 0  # to deal with nodes with equal F values
    open_set = PriorityQueue()
    open_set.put((0, count, start))   # add F(n), count, start node 
    parent_node = {}
    
    g_score = {node:float("inf") for row in grid for node in row} # distance from start to curr node
    g_score[start] = 0
    
    f_score = {node:float("inf") for row in grid for node in row} # g+h
    f_score[start] = h(start.get_pos(), end.get_pos())

    # Make a set to knoe which values are in hash as priority queue doesn't allow to check if an elem is in queue
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]   # get the lowest score node from the queue
        open_set_hash.remove(current)    # delete the visited node from hash

        if current == end:
            # construct path
            reconstruct_path(parent_node,end,draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:   # Ex initially all g scores are set to infinity, so if new g score is less update it and set the parent node to current node
                parent_node[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())  

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()      
        draw()

        # if current is not start make it red and close as we have already visited it
        if current != start:
            current.make_closed()
    return False   # if path not found


# make a grid
def make_grid(rows, width):
    grid = []
    node_size = width // rows   # will give width of each cube (or the dostance b/w each row)
    for i in range(rows):  # row
        grid.append([])
        for j in range(rows): # column
            node = Node(i, j, node_size, rows)
            grid[i].append(node)  # append currently created node to current row
    return grid


def draw_grid(win, rows,width):
    node_size = width // rows
    for i in range(rows):

        # creating horizontal lines
        # ex line starts from (0, 16) and goes upto (800, 16)
        # incrementing x everytime 
        #(0,16)--------------------(800,16)
        #(0,32)--------------------(800,32)
        #(0,48)--------------------(800,48)
        
        pygame.draw.line(win, GREY, (0, i * node_size), (width, i * node_size))
        
        # creating vertical lines
        # ex line starts from (16(x), 0(y)) and goes upto (16, 800)
        # incrementing y everytime 
        #(0,0)  (16,0) (32,0)   (48,0)  (64,0)
        # |       |       |       |        |
        # |       |       |       |        |
        # |       |       |       |        |
        #(0,800)(16,800)(32,800)(48,800) (64,800)

        for j in range(rows):
            pygame.draw.line(win, GREY, (j * node_size, 0), (j * node_size, width))

# this function draws everything
def draw(win, grid, rows, width):
    win.fill(BLACK)          # fill the screen with black color
    for row in grid:         # get the rows
        for node in row:     # get columns in each row
            node.draw(win)   # draw cube(rectangle)
    
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width): # pos is the mouse position
    node_size = width // rows
    x, y = pos
    row = x // node_size
    col = y // node_size 

    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True        # runnning main loop or not

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
            if pygame.mouse.get_pressed()[0]:  # if left mouse button is pressed
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS, width)
                node = grid[row][col]

                if not start and node!= end:  # if this is a mouse click, start is not set, set start as curr pos of mouse
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != start and node != end:
                    node.make_barrier()
                
            elif pygame.mouse.get_pressed()[2]: # right mouse button
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end: # to start we need an end and start
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda : draw(win, grid, ROWS, width), grid, start, end)

                # reset the game
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS,WIDTH)
    pygame.quit()

main(WIN, WIDTH)