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
        # detect bump in percept
        if 'bump' in percept:
            bump = True
            if 'fwd' not in percept:
                percept[0] = 'fwd'
            else:
                percept.pop(0)
        else:
            bump = False

        # swap self.P considering the error if there was a turnleft/turnright before
        P_turn = self.P
        if self.prev_action == 'turnleft':
            P_turn[0] = (0.05 * self.P[0]) + (0.95 * self.P[1])
            P_turn[1] = (0.05 * self.P[1]) + (0.95 * self.P[2])
            P_turn[2] = (0.05 * self.P[2]) + (0.95 * self.P[3])
            P_turn[3] = (0.05 * self.P[3]) + (0.95 * self.P[0])
        if self.prev_action == 'turnright':
            P_turn[0] = (0.05 * self.P[0]) + (0.95 * self.P[3])
            P_turn[1] = (0.05 * self.P[1]) + (0.95 * self.P[0])
            P_turn[2] = (0.05 * self.P[2]) + (0.95 * self.P[1])
            P_turn[3] = (0.05 * self.P[3]) + (0.95 * self.P[2])
        self.P = P_turn

        # T matrix calculation considering the bump
        T = np.zeros([len(self.locations), len(self.locations)], dtype=np.float)
        T = np.array([T, T, T, T])
        dirs = ['N', 'E', 'S', 'W']
        for i in range(4):
            if self.prev_action == "forward" and not bump:
                for idx, loc in enumerate(self.locations):
                    next_loc = nextLoc(loc, dirs[i])
                    if legalLoc(next_loc, self.size) and (next_loc not in self.walls):
                        next_idx = self.loc_to_idx[next_loc]
                        T[i, idx, next_idx] = 1.0 - self.eps_move
                        T[i, idx, idx] = self.eps_move
                    else:
                        T[i, idx, idx] = 1.0
            else:
                for idx, loc in enumerate(self.locations):
                    T[i, idx, idx] = 1.0

        # translation percept ['fwd', 'bckwd', 'left', 'right'] to percept_tmp [N, E, S, W]
        percept_tmp = [list(percept), list(percept), list(percept), list(percept)]
        for k in range(4):
            if k == 0:
                for j in range(len(percept_tmp[k])):
                    if percept_tmp[k][j] == 'fwd': percept_tmp[k][j] = 'N'
                    if percept_tmp[k][j] == 'bckwd': percept_tmp[k][j] = 'S'
                    if percept_tmp[k][j] == 'left': percept_tmp[k][j] = 'W'
                    if percept_tmp[k][j] == 'right': percept_tmp[k][j] = 'E'
            if k == 1:
                for j in range(len(percept_tmp[k])):
                    if percept_tmp[k][j] == 'fwd': percept_tmp[k][j] = 'E'
                    if percept_tmp[k][j] == 'bckwd': percept_tmp[k][j] = 'W'
                    if percept_tmp[k][j] == 'left': percept_tmp[k][j] = 'N'
                    if percept_tmp[k][j] == 'right': percept_tmp[k][j] = 'S'
            if k == 2:
                for j in range(len(percept_tmp[k])):
                    if percept_tmp[k][j] == 'fwd': percept_tmp[k][j] = 'S'
                    if percept_tmp[k][j] == 'bckwd': percept_tmp[k][j] = 'N'
                    if percept_tmp[k][j] == 'left': percept_tmp[k][j] = 'E'
                    if percept_tmp[k][j] == 'right': percept_tmp[k][j] = 'W'
            if k == 3:
                for j in range(len(percept_tmp[k])):
                    if percept_tmp[k][j] == 'fwd': percept_tmp[k][j] = 'W'
                    if percept_tmp[k][j] == 'bckwd': percept_tmp[k][j] = 'E'
                    if percept_tmp[k][j] == 'left': percept_tmp[k][j] = 'S'
                    if percept_tmp[k][j] == 'right': percept_tmp[k][j] = 'N'

        # O matrix calculation considering the bump
        O = np.zeros([len(self.locations)], dtype=np.float)
        O = np.array([O, O, O, O])
        for i in range(4):
            for idx, loc in enumerate(self.locations):
                prob = 1.0
                for d in ['N', 'E', 'S', 'W']:
                    nh_loc = nextLoc(loc, d)
                    obstacle = (not legalLoc(nh_loc, self.size)) or (nh_loc in self.walls)
                    if obstacle == (d in percept_tmp[i]):
                        # if there is a bump, the sensor is error-free for the fwd direction
                        if bump and d == percept_tmp[i][0]:
                            prob = 1
                        else:
                            prob *= (1 - self.eps_perc)
                    else:
                        prob *= self.eps_perc
                # if there is bump, set prob = 0 for orientations where fwd-location is not a wall
                if bump:
                    bump_wall = nextLoc(loc, percept_tmp[i][0])
                    if bump_wall not in self.walls:
                        prob = 0
                O[i, idx] = prob

        # P matrix calculation each submatrix separately
        for i in range(4):
            self.P[i] = T[i].transpose() @ self.P[i]
            self.P[i] = O[i] * self.P[i]

        self.P /= np.sum(self.P)

        # TODO CHANGE THIS HEURISTICS TO SPEED UP CONVERGENCE
        # if there is a wall ahead then lets turn
        action = 'forward'
        if 'fwd' in percept:
            action = 'turnright'
        if self.prev_action == 'turnleft' and 'left' not in percept:
            action = 'forward'
        else:
            if 'left' in percept and 'fwd' not in percept:
                action = 'forward'
            if 'left' not in percept:
                action = 'turnleft'
            if 'left' in percept and 'fwd' in percept:
                action = 'turnright'

        self.prev_action = action

        return action

    def getPosterior(self):
        # directions in order 'N', 'E', 'S', 'W'
        P_arr = np.zeros([self.size, self.size, 4], dtype=np.float)
        # put probabilities in the array
        # TODO PUT YOUR CODE HERE
        for i in range(4):
            for idx, loc in enumerate(self.locations):
                P_arr[loc[0], loc[1], i] = self.P[i, idx]
        P_arr = P_arr / np.sum(P_arr)

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
