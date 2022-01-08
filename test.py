import pygame as pg
import sys
import os
import numpy as np

from etm import ETM
from bug2 import Bug2Planner
# Color
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
yellow = (255, 255, 0)

# Create cell
WIDTH = 20
HEIGHT = 20
MARGIN = 5
grid = []


# Screen

# create grid


with open('map_1.txt') as f:
  lines = f.readlines()

# print(lines[1].split(' '))
# w_grid, h_grid = int(lines[1].split(' ')[0]), int(lines[1].split(' ')[1])
# print(w_grid)
# print(h_grid)
# os._exit(1)

WIDTH = int(lines[0])
HEIGHT = int(lines[0])
w_grid = int(lines[1])
h_grid = int(lines[1])


DISPLAY_SIZE = [h_grid*(HEIGHT+MARGIN)+MARGIN, w_grid*(WIDTH+MARGIN)+MARGIN]
pg.init()
dis = pg.display.set_mode(DISPLAY_SIZE) 
pg.display.set_caption("Coverage")

x_cell = DISPLAY_SIZE[0] // (WIDTH+MARGIN)
y_cell = DISPLAY_SIZE[1] // (HEIGHT+MARGIN)


for row, line in enumerate(lines[2:]):
    grid.append([])
    for cell in line.split(' '):
        grid[row].append(-int(cell))

obs_x = []
obs_y = []

for ind_row, row in enumerate(grid):
    for ind_col, value in enumerate(row):
        if value == -1:
            obs_x.append(ind_row)
            obs_y.append(ind_col)

# os._exit(1)
    
# start, goal
s_start = [0,0]
s_goal = [y_cell-1,x_cell-1]
# robot



class Robot():
    def __init__(self, s_start):
        self.width = WIDTH
        self.height = HEIGHT
        self.pos = s_start # array position = grid position
        self.robot_image = pg.transform.scale(pg.image.load("robot3.jpg"), (WIDTH,HEIGHT))

        self.etm = ETM([h_grid, w_grid])

        self.count_num_cell = 1
        self.deadlock = 0

        

    def draw(self):
        dis_pos = (self.pos[1]*(MARGIN+WIDTH) + MARGIN,self.pos[0]*(MARGIN+HEIGHT) + MARGIN)
        grid[self.pos[0]][self.pos[1]] = 2
        dis.blit(self.robot_image, dis_pos)

    # tra ve chuong ngai vat
    def vision(self):
        x_cur, y_cur = self.pos
        # đánh dấu ô đã đi qua
        self.etm.your_map[x_cur][y_cur] = 1

        obstacle = []
        for row in [-1, 0, 1]:
            for col in [-1, 0, 1]:
                if (x_cur+row) >=0 and (x_cur+row)<h_grid and (y_cur+col)>=0 and (y_cur+col)<w_grid:
                    # print(x_cur+row)
                    # print(y_cur+col)
                    # kiểm tra môi trường là chướng ngại vật và chướng ngại vật đó chưa được cập nhật trong your_map
                    if grid[x_cur+row][y_cur+col] == -1 and self.etm.your_map[x_cur+row][y_cur+col] != -1:
                        self.etm.your_map[x_cur+row][y_cur+col] = -1
                        obstacle.append([x_cur+row, y_cur+col])
                    # nếu map môi trường là ô có thể đi thì cập nhập lại map nội tại của robot là 2 đánh dấu ô đó là đã nhìn thấy và có thể đến
                    elif grid[x_cur+row][y_cur+col] == 0 and self.etm.your_map[x_cur+row][y_cur+col] == 0:
                        self.etm.your_map[x_cur+row][y_cur+col] = 2
                    
        return obstacle

    # tìm bước đi tiếp theo
    def one_step(self):
        obstacle = self.vision()
        self.etm.update(current=self.pos, obstacle=obstacle)
        # [print(etm) for etm in self.etm.MAPS]
        # [print(row) for row in self.etm.your_map]
        next_step, useBug2 = self.etm.next_step(self.pos)

        if useBug2:
            # print(111)
            # print(self.pos[0], self.pos[1], next_step[0], next_step[1], obs_y, obs_x)
            print(self.pos)
            print(next_step)
            bug = Bug2Planner(self.pos[0], self.pos[1], next_step[0], next_step[1], obs_x, obs_y)
            x_cell, y_cell = bug.bug2()
            print(x_cell)
            print(y_cell)
            self.count_num_cell += len(x_cell)
            print(len(x_cell))
            self.deadlock += 1
            self.pos = next_step
            # for x, y in zip(x_cell, y_cell):
            #     self.pos = [x, y]
        else:
            self.pos = next_step
            self.count_num_cell += 1



    # def coverage(self):
    #     while(True):

    #         # [print(etm) for etm in self.etm.MAPS]
    #         obstacle = self.vision()
    #         self.etm.update(current=self.pos, obstacle=obstacle)
    #         # [print(etm) for etm in self.etm.MAPS]
    #         self.pos = self.etm.next_step(self.pos)


    def __call__(self):
        self.coverage()
        
    """
    direction: 
    7     8     9
    4  cur_pos  6
    1     2     3  
    """
    def move(self, direction): # test move
        if direction == 7:
            self.pos[0] -= 1
            self.pos[1] -= 1
        if direction == 8:
            self.pos[0] -= 1
        if direction == 9:
            self.pos[0] -= 1
            self.pos[1] += 1
        if direction == 4:
            self.pos[1] -= 1
        if direction == 6:
            self.pos[1] += 1
        if direction == 1:
            self.pos[0] += 1
            self.pos[1] -= 1
        if direction == 2:
            self.pos[0] += 1
        if direction == 3:
            self.pos[0] += 1
            self.pos[1] += 1

robot = Robot(s_start)
def clean():
    # robot()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN: # click event
                pos = pg.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if grid[row][column] == 0 :
                    grid[row][column] = -1
                else :
                    grid[row][column] = 0
                print("Click ",pos, "Grid coordinates: ", row, column)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_0:
                    robot.move(0)
                elif event.key == pg.K_1:
                    robot.move(1)
                elif event.key == pg.K_DOWN and robot.pos[0] < (y_cell - 1) and grid[robot.pos[0]+1][robot.pos[1]] != -1:
                    # print(robot.pos, y_cell)
                    robot.move(2)
                elif event.key == pg.K_3:
                    robot.move(3)
                elif event.key == pg.K_LEFT and robot.pos[1] > 0 and grid[robot.pos[0]][robot.pos[1]-1] != -1:
                    robot.move(4)
                elif event.key == pg.K_RIGHT and robot.pos[1] < (x_cell - 1) and grid[robot.pos[0]][robot.pos[1]+1] != -1:
                    robot.move(6)
                elif event.key == pg.K_7:
                    robot.move(7)
                elif event.key == pg.K_UP and robot.pos[0] > 0 and grid[robot.pos[0]-1][robot.pos[1]] != -1:
                    robot.move(8)
                elif event.key == pg.K_9:
                    robot.move(9)

        robot.one_step()
                    # print('aaaa')

        dis.fill(black)
        for row in range(y_cell):
            for column in range(x_cell):
                color = white
                if grid[row][column] == -1:
                    color = red
                if s_goal == [row,column]:
                    color = green
                if grid[row][column] == 2:
                    color = (255,255,0)
                pg.draw.rect(dis,
                             color,
                             [(MARGIN + WIDTH)*column + MARGIN,
                             (MARGIN + HEIGHT)*row + MARGIN,
                             WIDTH,
                             HEIGHT])
        robot.draw()
        pg.display.flip()
        pg.time.delay(50)
        print('quang duong: {}'.format(robot.count_num_cell))
        print("so lan deadlock: {}".format(robot.deadlock))

def main():
    clean()
    # robot = Robot(s_start)
    # robot()
    # print(robot.your_map)

if __name__ == "__main__":
    main()