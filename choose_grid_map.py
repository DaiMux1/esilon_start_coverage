import pygame
import os.path
from pathlib import Path

class GridMap():

    def __init__(self, n_square, square_width = 40, square_height = 40, margin = 1):
        self.n_square = n_square
        self.square_width = square_width
        self.square_height = square_height
        self.margin = margin
        self.window_size = [self.n_square*square_width+(self.n_square+1)*self.margin,
                            self.n_square*square_height+(self.n_square+1)*self.margin]

        self.start = [0,0]
        self.end = [square_height, square_width]

    def create_grid_map(self):
        black = (0, 0, 0)
        white = (255, 255, 255)

        red = (255, 0, 0)
        WIDTH = self.square_width
        HEIGHT = self.square_height
        MARGIN = self.margin
        grid = []
        for row in range(self.n_square):
            grid.append([])
            for column in range(self.n_square):
                grid[row].append(0)

        pygame.init()
        window_size = self.window_size
        scr = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Grid")
        done = False
        clock = pygame.time.Clock()

        i = 0

        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (WIDTH + MARGIN)
                    row = pos[1] // (HEIGHT + MARGIN)
                    if (i == 0):
                        grid[row][column] = 2
                        self.start = [row, column]  # start position
                        i = i+1
                        # print("Click ", pos, "Grid coordinates: ", row, column)
                    elif (i == 1):
                        grid[row][column] = 3
                        self.end = [row, column]  # end position
                        i = i+1
                        # print("Click ", pos, "Grid coordinates: ", row, column)
                    else:
                        grid[row][column] = 1
                        # print("Click ", pos, "Grid coordinates: ", row, column)
            scr.fill(black)
            for row in range(self.n_square):
                for column in range(self.n_square):
                    color = white
                    if grid[row][column] == 1:
                        color = red
                    pygame.draw.rect(scr,
                                     color,
                                     [(MARGIN + WIDTH) * column + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH,
                                      HEIGHT])

                    color = white
                    if grid[row][column] == 2:
                        color = (255,255,0)
                        pygame.draw.rect(scr,
                                         color,
                                         [(MARGIN + WIDTH) * column + MARGIN,
                                          (MARGIN + HEIGHT) * row + MARGIN,
                                          WIDTH,
                                          HEIGHT])

                    color = white
                    if grid[row][column] == 3:
                        color = (0,255,0)
                        pygame.draw.rect(scr,
                                         color,
                                         [(MARGIN + WIDTH) * column + MARGIN,
                                          (MARGIN + HEIGHT) * row + MARGIN,
                                          WIDTH,
                                          HEIGHT])

            clock.tick(50)
            pygame.display.flip()

        pygame.quit()
        return grid


def create_grid_map():
    my_file = Path("grid_map.txt")
    if my_file.is_file():
        print(1)
        G = GridMap(n_square=20)
        grid = G.create_grid_map()
        f = open("grid_map.txt", "w")
        f.write(str(G.square_height) + " " + str(G.square_width) +"\n")
        f.write(str(G.start[0]) + " " + str(G.start[1]) + "\n")
        f.write(str(G.end[0]) + " " + str(G.end[1]) + "\n")
        for row in grid:
            for column in row:
                f.write(str(column) + " ")
            f.write("\n")
    else:
        print("File does not exist")

create_grid_map()