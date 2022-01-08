import numpy as np
import copy
import queue

from numpy.lib import math

class ETM:
    def __init__(self, size):
        height, width = size
        self.height = height
        self.width = width
        gridB = []
        for row in range(height):
            gridB.append([])
            for col in range(width):
                gridB[row].append(height-row)
        self.potential = np.array(gridB)
        print(self.potential)

        self.MAPS = []

        # your_map = []
        # for row in range(height):
        #     your_map.append([])
        #     for column in range(width):
        #         your_map[row].append(0)
        self.your_map = np.zeros(size)
        # print(self.your_map)

        
        maps_2 = max(height, width)
        num_maps = math.ceil(np.log2(maps_2)) 

        for ind_maps in range(num_maps):
            # print(ind_maps)
            if ind_maps == 0:
                self.MAPS.append(self.potential)
            else:
                step = int(np.exp2(ind_maps))
                maps = copy.deepcopy(self.potential).astype(np.float32)

                for row in range(height):
                    if row % step != 0:
                        continue
                    for col in range(width):
                        if col % step != 0:
                            continue
                        value = 0
                        num_cell = 0
                        num_u_cell = 0
                        for row_ in range(step):
                            if ((row + row_)>=height): break
                            for col_ in range(step):
                                if (col + col_ >= width): continue
                                num_cell += 1
                                value += maps[(row + row_), (col + col_)]
                                if (self.your_map[(row + row_), (col + col_)]==0): num_u_cell += 1
                        # công thức tính giá trị tiềm năng
                        value = value/num_cell*1.0*num_u_cell/num_cell
                        # print(value)
                        for row_ in range(step):
                            if ((row + row_)>=height): break
                            for col_ in range(step):
                                if (col + col_ >= width): continue
                                maps[(row + row_), (col + col_)] = value

                self.MAPS.append(maps)

    def update(self, current, obstacle = []):
        # duyệt qua từng level MAPS
        for ind, maps in enumerate(self.MAPS):
            if ind == 0:
                if obstacle:
                    for cell in obstacle:
                        x, y = cell
                        maps[x, y] = -1
                maps[current[0]][current[1]] = 0
            else:
                # update current position
                x, y = current
                step = int(np.exp2(ind))
                x = int(x/step)
                y = int(y/step)
                # tìm lại tọa độ trong maps với các ô ở đầu mỗi coarse cell
                x = x * step
                y = y * step

                
                coordinate_maps = [x, y]# tìm lại tọa độ trong maps
                # print(coordinate_maps)

                value = 0
                num_cell = 0
                num_u_cell = 0
                for row_ in range(step):
                    if (coordinate_maps[0] + row_) >= self.height: break
                    for col_ in range(step):
                        if (coordinate_maps[1] + col_) >= self.width: break
                        num_cell += 1
                        if self.MAPS[0][(coordinate_maps[0] + row_), (coordinate_maps[1] + col_)] > 0:
                            num_u_cell += 1
                            value += self.MAPS[0][(coordinate_maps[0] + row_), (coordinate_maps[1] + col_)]

                value = value/num_cell

                for row_ in range(step):
                    if (coordinate_maps[0] + row_) >= self.height: break
                    for col_ in range(step):
                        if (coordinate_maps[1] + col_) >= self.width: break
                        maps[(coordinate_maps[0] + row_), (coordinate_maps[1] + col_)] = value
                
                # nếu có chướng ngại vật thì update
                if obstacle:
                    for cell in obstacle:
                        x, y = cell
                        step = int(np.exp2(ind))
                        x = int(x/step)
                        y = int(y/step)
                        # tìm lại tọa độ trong maps
                        x = x * step
                        y = y * step

                        
                        coordinate_maps = [x, y]# tìm lại tọa độ trong maps
                        # print(coordinate_maps)

                        value = 0
                        num_cell = 0
                        num_u_cell = 0
                        for row_ in range(step):
                            if (coordinate_maps[0] + row_) >= self.height: break
                            for col_ in range(step):
                                if (coordinate_maps[1] + col_) >= self.width: break
                                num_cell += 1
                                if self.MAPS[0][(coordinate_maps[0] + row_), (coordinate_maps[1] + col_)] > 0:
                                    num_u_cell += 1
                                    value += self.MAPS[0][(coordinate_maps[0] + row_), (coordinate_maps[1] + col_)]

                        value = value/num_cell

                        for row_ in range(step):
                            if (coordinate_maps[0] + row_) >= self.height: break
                            for col_ in range(step):
                                if (coordinate_maps[1] + col_) >= self.width: break
                                maps[(coordinate_maps[0] + row_), (coordinate_maps[1] + col_)] = value
                
    # next step
    def next_step(self, current):
        x_cur, y_cur =  current
        # di 8 huong
        rows_go_ = [-1, 0, 1, 0, -1, -1, 1, 1, 0]
        cols_go_ = [0, -1, 0, 1, -1, 1, 1, -1, 0]

        for ind, maps in enumerate(self.MAPS):
            next_step = {}

            if ind == 0:
                # di chuyen 4 huong
                potential  = 0
                nt = []

                for r, c in zip(rows_go_[:-1], cols_go_[:-1]):
                    if (x_cur+r) >=0 and (x_cur+r)<self.height and (y_cur+c)>=0 and (y_cur+c)<self.width:
                        if maps[x_cur+r][y_cur+c] > potential:
                            potential = maps[x_cur+r][y_cur+c]
                            nt = [x_cur+r, y_cur+c]
                if nt:
                    return nt, False


            ratio = int(np.exp2(ind))
            rows_go = np.array(rows_go_)*ratio
            cols_go = np.array(cols_go_)*ratio
            for r, c in zip(rows_go, cols_go):
                if (x_cur+r) >=0 and (x_cur+r)<self.height and (y_cur+c)>=0 and (y_cur+c)<self.width:
                    if maps[x_cur+r][y_cur+c] > 0:
                        # lưu key là số potential, value là tọa độ
                        next_step[maps[x_cur+r][y_cur+c]] = [x_cur+r, y_cur+c]
            
            # nếu tìm được bước đi ở tầm thứ ind MAPS thì trả về bước đi tiếp theo
            if next_step:
                next_step = dict(sorted(next_step.items(), key=lambda item: item[1], reverse=True))
                print(next_step)
                # ở MAPS giá trị lớn nhất thì robot sẽ đi tới
                if ind == 0:
                    for key in reversed(list(next_step.keys())):
                        print(next_step)
                        print(next_step[key])
                        return next_step[key]

                for cordinate in next_step.values():
                    root_cordinate = []
                    x_cor = cordinate[0] - int(cordinate[0] % ratio)
                    y_cor = cordinate[1] - int(cordinate[1] % ratio)

                    for r in range(ratio):
                        if (x_cor+r >= self.height): break
                        for c in range(ratio):
                            if (y_cor+c >= self.width): break
                            if self.your_map[x_cor+r][y_cor+c] == 2:
                                # self.bfs([x_cur, y_cur], [x_cor+r, y_cor+c])
                                return [x_cor+r, y_cor+c], True
                # return next_step
        return []
        

if __name__ == '__main__':
    etm = ETM([10, 10])
    print(etm.potential)
    [print(maps) for maps in etm.MAPS]
    
    etm.update((0,0) ,[[1,1], [6,3], [0, 9]])
    [print(maps) for maps in etm.MAPS]
    etm.update([7,3])
    [print(maps) for maps in etm.MAPS]
    # etm.update([5,6])
    # [print(maps) for maps in etm.MAPS]
