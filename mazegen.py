#!/usr/bin/python3

from PIL import Image, ImageDraw
import sys
from random import seed, shuffle, choice
from time import sleep, time

N, S, E, W = 1, 2, 4, 8    #byte-packable!
DX = {W:-1, E:1, S:0, N:0} #two hashmaps of int:int
DY = {N:-1, S:1, W:0, E:0}
OPPOSITE = {E:W, W:E, S:N, N:S}

def render_image(name, grid):
    image = Image.new("RGB", ((len(grid[0]) * 2) + 1, (len(grid) * 2) + 1))
    pixels = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if not (grid[y][x] == 0):
                pixels.append(((x*2)+1, (y*2)+1))
            if (grid[y][x] & N):
                pixels.append(((x*2)+1, (y*2)))
            if (grid[y][x] & S):
                pixels.append(((x*2)+1, (y*2)+2))
            if (grid[y][x] & E):
                pixels.append(((x*2)+2, (y*2)+1))
            if (grid[y][x] & W):
                pixels.append(((x*2),   (y*2)+1))
    im = ImageDraw.Draw(image)
    im.point(pixels, "white")
    image.save(name, "PNG")

# recursive function to carve paths
# tends to run out of max depth rather quickly, but it's here as an alternative to show
# how you'd do it with a recursive function
def carve_paths(cx, cy, grid):
    directions = [N, S, E, W]
    shuffle(directions)
    for way in directions:
        nx, ny = cx + DX[way], cy + DY[way]
        try:
            if (ny >= 0 and nx >= 0 and grid[ny][nx] == 0):
                grid[cy][cx] = grid[cy][cx] | way #store the direction we open
                grid[ny][nx] = grid[ny][nx] | OPPOSITE[way] #and the direction we entered the next cell from
                carve_paths(nx, ny, grid)
            else:
                continue
        except IndexError:
            continue # if we hit an outside wall



# we use a list (visited) as a stack and emulate being a recursive function in order to avoid running into
# pythons recursive function depth limit. the data we put in the list is also massively smaller
# than stack frames end up being, so its a lot easier on RAM and we can build much bigger mazes
def carve_list(cx, cy, grid):
    class Cell:
        def __init__(self, x, y, directions):
            self.x = x
            self.y = y
            self.directions = directions
    directions = [N, S, E, W]
    shuffle(directions)
    visited = []
    visited.append(Cell(cx, cy, directions))
    stime = time()
    while (len(visited) > 0):
        cell = visited.pop()
        cx = cell.x
        cy = cell.y
        directions = cell.directions
        way = directions.pop()
        nx, ny = cx + DX[way], cy + DY[way] #walk to a new cell, one step away in `way` direction
        if (len(directions) > 0):
            visited.append(Cell(cx, cy, directions))
        try:
            if(ny >= 0 and nx >= 0 and grid[ny][nx] == 0):
                grid[cy][cx] = grid[cy][cx] | way #store the direction we open
                grid[ny][nx] = grid[ny][nx] | OPPOSITE[way] #and the direction we entered the next cell from
                ndir = [N, S, E, W]
                shuffle(ndir)
                visited.append(Cell(nx,ny,ndir))
            else:
                pass
        except IndexError:
            pass
    print("Maze built in " + str((time() - stime)*1000.0) + "ms")

def add_exit(grid):
    entry_side = choice([N, S, E, W])
    if (entry_side == N):
        cell = choice(range(len(grid[0])))
        grid[0][cell] = grid[0][cell] | N
    elif (entry_side == S):
        cell = choice(range(len(grid[0])))
        grid[-1][cell] = grid[-1][cell] | S
    elif (entry_side == E):
        cell = choice(range(len(grid)))
        grid[cell][-1] = grid[cell][-1] | E
    elif (entry_side == W):
        cell = choice(range(len(grid)))
        grid[cell][0] = grid[cell][0] | W


if __name__ == "__main__":
    seed() #defaults to systime or dev/urandom
    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
    except IndexError:
        print("Too few arguments!")
        sys.exit()
    maze = [[0 for x in range(width)] for x in range(height)]
    carve_list(0, 0, maze)
    add_exit(maze)
    add_exit(maze)
    render_image("out.png", maze)
