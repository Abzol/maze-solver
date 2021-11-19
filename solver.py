#!/usr/bin/python3

from PIL import Image
import sys 
from time import time
N, E, S, W = 1, 2, 4, 8
inverse = {N:S, S:N, W:E, E:W}

class Node:
    x = 0
    y = 0
    back_dir = 0
    ways = 0
    def __init__(self, back_dir, ways, x, y):
        self.back_dir = back_dir
        self.ways = ways
        self.x = x
        self.y = y
    def walk(self):
        try:
            return self.ways.pop()
        except (AttributeError, IndexError):
            return None

def scan_exits(maze):
    entrance = None
    exit = None
    def check_exit(x, y):
        nonlocal entrance, exit
        l = maze.getpixel((x,y))
        if l == (255, 255, 255):
            if entrance == None:
                entrance = (x, y)
            else:
                exit = (x, y)
    for y in [0, maze.size[1]-1]:
        for x in range(maze.size[0]):
            check_exit(x, y)
    for x in [0, maze.size[0]-1]:
        for y in range(maze.size[1]):
            check_exit(x, y)
    return entrance, exit

def choose_path(pos, goal, options):
    if len(options) < 2:
        return options
    sortkey = []
    off_x = pos[0] - goal[0]
    off_y = pos[1] - goal[1]
    hor = [E, W] if off_x > 0 else [W, E]
    vert = [N, S] if off_y > 0 else [S, N]
    if off_x > off_y:
        sortkey.extend(hor)
        sortkey.extend(vert)
    else:
        sortkey.extend(vert)
        sortkey.extend(hor)
    paths = [v for v in sortkey if v in options]
    return paths

def walk_maze(entrance, exit, maze):
    def check_walls(x, y, back):
        ways = []
        try:
            if maze.getpixel((x, y-1)) == (255, 255, 255):
                ways.append(N)
            if maze.getpixel((x+1, y)) == (255, 255, 255):
                ways.append(E)
            if maze.getpixel((x, y+1)) == (255, 255, 255):
                ways.append(S)
            if maze.getpixel((x-1, y)) == (255, 255, 255):
                ways.append(W)
            ways.remove(back)
            return ways
        except IndexError:
            return ways
    path = []
    if entrance[0] == 0:
        path.append(Node(None, [E], entrance[0], entrance[1]))
    elif entrance[0] == maze.size[0]-1:
        path.append(Node(None, [W], entrance[0], entrance[1]))
    elif entrance[1] == 0:
        path.append(Node(None, [S], entrance[0], entrance[1]))
    elif entrance[1] == maze.size[1]-1:
        path.append(Node(None, [N], entrance[0], entrance[1]))
    x = entrance[0]
    y = entrance[1]
    while((x,y) != (exit[0], exit[1])):
        d = path[-1].walk()
        if d:
            if d == N:
                y -= 1
            elif d == S:
                y += 1
            elif d == E:
                x += 1
            elif d == W:
                x -= 1
            ways = choose_path((x,y), (exit[0], exit[1]), check_walls(x, y, inverse[d]))
            path.append(Node(inverse[d], ways, x, y))
        else:
            try:
                if sys.argv[2] == '-a':
                    maze.putpixel((x,y), (0, 0, 255))
            except IndexError:
                pass
            back = path.pop()
            x = path[-1].x
            y = path[-1].y
    return path

def render_path(maze, path):
    length = len(path)
    for index, node in enumerate(path):
        maze.putpixel((node.x, node.y), (255-int(index/length*255), int(index/length*255), 0))

def main():
    stime = time()
    maze = Image.open(sys.argv[1])
    #find exits
    entrance, exit = scan_exits(maze)
    path = walk_maze(entrance, exit, maze)
    render_path(maze, path)
    maze.save('solved.png', 'PNG')
    print(f'Maze solved in {(time() - stime) * 1000.0}ms')
    
if __name__ == "__main__":
    main()
