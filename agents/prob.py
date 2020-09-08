# prob.py
# This is

import random
import numpy as np

from gridutil import *

best_turn = {('N', 'E'): 'turnright',
             ('N', 'S'): 'turnright',
             ('N', 'W'): 'turnleft',
             ('E', 'S'): 'turnright',
             ('E', 'W'): 'turnright',
             ('E', 'N'): 'turnleft',
             ('S', 'W'): 'turnright',
             ('S', 'N'): 'turnright',
             ('S', 'E'): 'turnleft',
             ('W', 'N'): 'turnright',
             ('W', 'E'): 'turnright',
             ('W', 'S'): 'turnleft'}


class LocAgent:

    def __init__(self, size, walls, eps_perc, eps_move):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.eps_perc = eps_perc
        self.eps_move = eps_move

        # previous action
        self.prev_action = None

        prob = 1.0 / len(self.locations)
        self.P = prob * np.ones([len(self.locations)], dtype=np.float)
        self.P = np.array([self.P, self.P, self.P, self.P])

    def __call__(self, percept):
        # update posterior
        # TODO PUT YOUR CODE HERE
        T = np.zeros([len(self.locations), len(self.locations)], dtype=np.float)
        T = np.array([T, T, T, T])
        dirs = ['N', 'E', 'S', 'W']
        for i in range(4):
            if self.prev_action == "forward":
                for idx, loc in enumerate(self.locations):
                    next_loc = nextLoc(loc, dirs[i])
                    # ___
                    if legalLoc(next_loc, self.size) and (next_loc not in self.walls):
                        next_idx = self.loc_to_idx[next_loc]
                        T[i, idx, next_idx] = 1.0 - self.eps_move
                        T[i, idx, idx] = self.eps_move
                    # __
                    else:
                        T[i, idx, idx] = 1.0
            else:
                # __
                for idx, loc in enumerate(self.locations):
                    T[i, idx, idx] = 1.0

        # -----------------------
        O = np.zeros([len(self.locations), 4], dtype=np.float)
        O = np.array([O, O, O, O])
        for i in range(4):
            for idx, loc in enumerate(self.locations):
                prob = 1.0
                for d in ['N', 'E', 'S', 'W']:
                    nh_loc = nextLoc(loc, d)
                    # __
                    obstacle = (not legalLoc(nh_loc, self.size)) or (nh_loc in self.walls)
                    # __
                    if obstacle == (d in percept):
                        prob *= (1 - self.eps_perc)
                    # __
                    else:
                        prob *= self.eps_perc
                O[idx] = prob
        # __
        # __
        # __
        self.P = T.transpose() @ self.P
        # __
        self.P = O * self.P
        # __
        self.P /= np.sum(self.P)
        action = 'forward'
        # TODO CHANGE THIS HEURISTICS TO SPEED UP CONVERGENCE
        # if there is a wall ahead then lets turn
        if 'fwd' in percept:
            # higher chance of turning left to avoid getting stuck in one location
            action = np.random.choice(['turnleft', 'turnright'], 1, p=[0.8, 0.2])
        else:
            # prefer moving forward to explore
            action = np.random.choice(['forward', 'turnleft', 'turnright'], 1, p=[0.8, 0.1, 0.1])

        self.prev_action = action

        return action

    def getPosterior(self):
        # directions in order 'N', 'E', 'S', 'W'
        P_arr = np.zeros([self.size, self.size, 4], dtype=np.float)
        # put probabilities in the array
        # TODO PUT YOUR CODE HERE
        for idx, loc in enumerate(self.locations):
            # print(self.P.shape)
            # print(P_arr.shape)
            P_arr[loc[0], loc[1], 0] = self.P[0, idx, 0]

        # -----------------------

        return P_arr

    def forward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    def backward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    @staticmethod
    def turnright(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 1) % 4
        return cur_loc, dirs[idx]

    @staticmethod
    def turnleft(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 4 - 1) % 4
        return cur_loc, dirs[idx]
