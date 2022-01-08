import numpy as np

class Bug2Planner:
  def __init__(self, start_x, start_y, goal_x, goal_y, obs_x, obs_y):
    self.goal_x = goal_x
    self.goal_y = goal_y
    self.obs_x = obs_x
    self.obs_y = obs_y
    self.r_x = [start_x]
    self.r_y = [start_y]
    self.out_x = []
    self.out_y = []
    # self.straight_x = [start_x]
    # self.straight_y = [start_y]
    # self.hit_x = []
    # self.hit_y = []
    # lưu các điểm bao quanh chướng ngại vật
    for o_x, o_y in zip(obs_x, obs_y):
        for add_x, add_y in zip([1, 0, -1, -1, -1, 0, 1, 1],
                                [1, 1, 1, 0, -1, -1, -1, 0]):
            cand_x, cand_y = o_x+add_x, o_y+add_y
            valid_point = True
            for _x, _y in zip(obs_x, obs_y):
                if cand_x == _x and cand_y == _y:
                    valid_point = False
                    break
            if valid_point:
                self.out_x.append(cand_x), self.out_y.append(cand_y)

    # while True:
    #   if self.straight_x[-1] == self.goal_x and \
    #           self.straight_y[-1] == self.goal_y:
    #       break

    #   c_x = self.straight_x[-1] + np.sign(self.goal_x - self.straight_x[-1])
    #   c_y = self.straight_y[-1] + np.sign(self.goal_y - self.straight_y[-1])
    #   for x_ob, y_ob in zip(self.out_x, self.out_y):
    #       if c_x == x_ob and c_y == y_ob:
    #           # lưu điểm bị va chạm
    #           self.hit_x.append(c_x), self.hit_y.append(c_y)
    #           break
    #   # lưu các điểm đi trên đường thẳng
    #   self.straight_x.append(c_x), self.straight_y.append(c_y)

  def mov_normal(self):
    return self.r_x[-1] + np.sign(self.goal_x - self.r_x[-1]), \
            self.r_y[-1] + np.sign(self.goal_y - self.r_y[-1])

  def mov_to_next_obs(self, visited_x, visited_y):
    for add_x, add_y in zip([1, 0, -1, 0], [0, 1, 0, -1]):
        c_x, c_y = self.r_x[-1] + add_x, self.r_y[-1] + add_y
        for _x, _y in zip(self.out_x, self.out_y):
            use_pt = True
            if c_x == _x and c_y == _y:
                for v_x, v_y in zip(visited_x, visited_y):
                    if c_x == v_x and c_y == v_y:
                        use_pt = False
                        break
                if use_pt:
                    return c_x, c_y, False
            if not use_pt:
                break
    return self.r_x[-1], self.r_y[-1], True

  def bug2(self):
    mov_dir = 'normal'
    cand_x, cand_y = -np.inf, -np.inf

    straight_x, straight_y = [self.r_x[-1]], [self.r_y[-1]]
    hit_x, hit_y = [], []
    while True:
        if straight_x[-1] == self.goal_x and \
                straight_y[-1] == self.goal_y:
            break

        c_x = straight_x[-1] + np.sign(self.goal_x - straight_x[-1])
        c_y = straight_y[-1] + np.sign(self.goal_y - straight_y[-1])
        for x_ob, y_ob in zip(self.out_x, self.out_y):
            if c_x == x_ob and c_y == y_ob:
                # lưu điểm bị va chạm
                hit_x.append(c_x), hit_y.append(c_y)
                break
        # lưu các điểm đi trên đường thẳng
        straight_x.append(c_x), straight_y.append(c_y)
    # nếu đường thẳng k có chướng ngại vật
    print(len(hit_x))
    print('======')
    if len(hit_x) == len(straight_x) - 1:
        return straight_x, straight_y
    for x_ob, y_ob in zip(self.out_x, self.out_y):
      if self.r_x[-1] == x_ob and self.r_y[-1] == y_ob:
        mov_dir = 'obs'
        break
    loop = False
    visited_x, visited_y = [], []
    while True:
      if self.r_x[-1] == self.goal_x \
              and self.r_y[-1] == self.goal_y:
          break
      if mov_dir == 'normal':
          cand_x, cand_y = self.mov_normal()
      if mov_dir == 'obs':
          cand_x, cand_y, loop = self.mov_to_next_obs(visited_x, visited_y)
      if mov_dir == 'normal':
          found_boundary = False
          for x_ob, y_ob in zip(self.out_x, self.out_y):
              if cand_x == x_ob and cand_y == y_ob:
                  self.r_x.append(cand_x), self.r_y.append(cand_y)
                  visited_x[:], visited_y[:] = [], []
                  visited_x.append(cand_x), visited_y.append(cand_y)
                  del hit_x[0]
                  del hit_y[0]
                  mov_dir = 'obs'
                  found_boundary = True
                  break
          if not found_boundary:
              self.r_x.append(cand_x), self.r_y.append(cand_y)
      elif mov_dir == 'obs':
          if loop: 
              return self.r_x, self.r_y
          self.r_x.append(cand_x), self.r_y.append(cand_y)
          visited_x.append(cand_x), visited_y.append(cand_y)
          for i_x, i_y in zip(range(len(hit_x)), range(len(hit_y))):
              if cand_x == hit_x[i_x] and cand_y == hit_y[i_y]:
                  del hit_x[i_x]
                  del hit_y[i_y]
                  mov_dir = 'normal'
                  break

    return self.r_x, self.r_y

if __name__ == '__main__':
  with open('map_5.txt') as f:
    lines = f.readlines()

  grid = []
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

  bug = Bug2Planner(24, 24, 24, 27, obs_x, obs_y)
  x , y = bug.bug2()
  # print(x, y)
  for x_, y_ in zip(x, y):
    print(x_, y_)