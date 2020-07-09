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
        self.t = 0
        # previous action
        self.prev_action = None
        prob = 1.0 / len(self.locations)
        self.P0 = prob * np.ones([len(self.locations)], dtype=np.float)
        self.P1 = prob * np.ones([len(self.locations)], dtype=np.float)
        self.P2 = prob * np.ones([len(self.locations)], dtype=np.float)
        self.P3 = prob * np.ones([len(self.locations)], dtype=np.float)

    def __call__(self, percept, idx_orient):
        # update posterior
        # TODO PUT YOUR CODE HERE
        for i in range(4):
            if self.prev_action == "turnleft":
                idx_orient[i] = idx_orient[i] - 1
                if idx_orient[i] == -1:
                    idx_orient[i] = 3
            if self.prev_action == "turnright":
                idx_orient[i] = idx_orient[i] + 1
                if idx_orient[i] == 4:
                    idx_orient[i] = 0

        orientations = ['N', 'E', 'S', 'W']

        percept_tmp = [list(percept), list(percept), list(percept), list(percept)]
        print('before: ', percept_tmp)
        for k in range(4):
            if orientations[idx_orient[k]] == 'N':
                for i in range(len(percept_tmp[k])):
                    if percept_tmp[k][i] == 'fwd': percept_tmp[k][i] = 'N'
                    if percept_tmp[k][i] == 'bckwd': percept_tmp[k][i] = 'S'
                    if percept_tmp[k][i] == 'left': percept_tmp[k][i] = 'W'
                    if percept_tmp[k][i] == 'right': percept_tmp[k][i] = 'E'
            if orientations[idx_orient[k]] == 'W':
                for i in range(len(percept_tmp[k])):
                    if percept_tmp[k][i] == 'fwd': percept_tmp[k][i] = 'W'
                    if percept_tmp[k][i] == 'bckwd': percept_tmp[k][i] = 'E'
                    if percept_tmp[k][i] == 'left': percept_tmp[k][i] = 'S'
                    if percept_tmp[k][i] == 'right': percept_tmp[k][i] = 'N'
            if orientations[idx_orient[k]] == 'S':
                for i in range(len(percept_tmp[k])):
                    if percept_tmp[k][i] == 'fwd': percept_tmp[k][i] = 'S'
                    if percept_tmp[k][i] == 'bckwd': percept_tmp[k][i] = 'N'
                    if percept_tmp[k][i] == 'left': percept_tmp[k][i] = 'E'
                    if percept_tmp[k][i] == 'right': percept_tmp[k][i] = 'W'
            if orientations[idx_orient[k]] == 'E':
                for i in range(len(percept_tmp[k])):
                    if percept_tmp[k][i] == 'fwd': percept_tmp[k][i] = 'E'
                    if percept_tmp[k][i] == 'bckwd': percept_tmp[k][i] = 'W'
                    if percept_tmp[k][i] == 'left': percept_tmp[k][i] = 'N'
                    if percept_tmp[k][i] == 'right': percept_tmp[k][i] = 'S'
        print('after: ', percept_tmp)
        for ULTRA_ITEREATOR in range(4):
            if ULTRA_ITEREATOR == 0: T0 = np.zeros([len(self.locations), len(self.locations)], dtype=np.float)
            if ULTRA_ITEREATOR == 1: T1 = np.zeros([len(self.locations), len(self.locations)], dtype=np.float)
            if ULTRA_ITEREATOR == 2: T2 = np.zeros([len(self.locations), len(self.locations)], dtype=np.float)
            if ULTRA_ITEREATOR == 3: T3 = np.zeros([len(self.locations), len(self.locations)], dtype=np.float)

            if self.prev_action == "forward":
                for idx, loc in enumerate(self.locations):
                    if ULTRA_ITEREATOR == 0: next_loc = nextLoc(loc, orientations[idx_orient[0]])
                    if ULTRA_ITEREATOR == 1: next_loc = nextLoc(loc, orientations[idx_orient[1]])
                    if ULTRA_ITEREATOR == 2: next_loc = nextLoc(loc, orientations[idx_orient[2]])
                    if ULTRA_ITEREATOR == 3: next_loc = nextLoc(loc, orientations[idx_orient[3]])
                    # ___
                    if legalLoc(next_loc, self.size) and (next_loc not in self.walls):
                        next_idx = self.loc_to_idx[next_loc]
                        if ULTRA_ITEREATOR == 0:
                            T0[idx, next_idx] = 1.0 - self.eps_move
                            T0[idx, idx] = self.eps_move
                        if ULTRA_ITEREATOR == 1:
                            T1[idx, next_idx] = 1.0 - self.eps_move
                            T1[idx, idx] = self.eps_move
                        if ULTRA_ITEREATOR == 2:
                            T2[idx, next_idx] = 1.0 - self.eps_move
                            T2[idx, idx] = self.eps_move
                        if ULTRA_ITEREATOR == 3:
                            T3[idx, next_idx] = 1.0 - self.eps_move
                            T3[idx, idx] = self.eps_move
                    # __
                    else:
                        if ULTRA_ITEREATOR == 0: T0[idx, idx] = 1.0
                        if ULTRA_ITEREATOR == 1: T1[idx, idx] = 1.0
                        if ULTRA_ITEREATOR == 2: T2[idx, idx] = 1.0
                        if ULTRA_ITEREATOR == 3: T3[idx, idx] = 1.0
            else:
                # __
                for idx, loc in enumerate(self.locations):
                    if ULTRA_ITEREATOR == 0: T0[idx, idx] = 1.0
                    if ULTRA_ITEREATOR == 1: T1[idx, idx] = 1.0
                    if ULTRA_ITEREATOR == 2: T2[idx, idx] = 1.0
                    if ULTRA_ITEREATOR == 3: T3[idx, idx] = 1.0
                # __

            if ULTRA_ITEREATOR == 0: O0 = np.zeros([len(self.locations)], dtype=np.float)
            if ULTRA_ITEREATOR == 0: O1 = np.zeros([len(self.locations)], dtype=np.float)
            if ULTRA_ITEREATOR == 0: O2 = np.zeros([len(self.locations)], dtype=np.float)
            if ULTRA_ITEREATOR == 0: O3 = np.zeros([len(self.locations)], dtype=np.float)

            for idx, loc in enumerate(self.locations):
                prob = 1.0

                for d in ['N', 'E', 'S', 'W']:
                    nh_loc = nextLoc(loc, d)
                    # __
                    obstacle = (not legalLoc(nh_loc, self.size)) or (nh_loc in self.walls)
                    # __
                    if obstacle == (d in percept_tmp[ULTRA_ITEREATOR]):
                        prob *= (1 - self.eps_perc)
                    # __
                    else:
                        prob *= self.eps_perc
                # O_tmp[i] = prob
                if ULTRA_ITEREATOR == 0: O0[idx] = prob
                if ULTRA_ITEREATOR == 1: O1[idx] = prob
                if ULTRA_ITEREATOR == 2: O2[idx] = prob
                if ULTRA_ITEREATOR == 3: O3[idx] = prob

            self.t += 1
            # print(self.t)
            # __
            if ULTRA_ITEREATOR == 0:
                self.P0 = T0.transpose() @ self.P0
                self.P0 = O0 * self.P0
                self.P0 /= np.sum(self.P0)
            if ULTRA_ITEREATOR == 1:
                self.P1 = T1.transpose() @ self.P1
                self.P1 = O1 * self.P1
                self.P1 /= np.sum(self.P1)
            if ULTRA_ITEREATOR == 2:
                self.P2 = T2.transpose() @ self.P2
                self.P2 = O2 * self.P2
                self.P2 /= np.sum(self.P2)
            if ULTRA_ITEREATOR == 3:
                self.P3 = T3.transpose() @ self.P3
                self.P3 = O3 * self.P3
                self.P3 /= np.sum(self.P3)

        # TODO _HEURISTICS_
        action = 'forward'

        # if left-corner turn right
        if 'fwd' in percept and 'left' in percept and 'right' not in percept:
            action = 'turnright'
        elif 'fwd' in percept and 'right' in percept and 'left' not in percept:
            action = 'turnleft'
        # elif 'left' in percept and 'fwd' not in percept and 'bckwd' not in percept:
        #     action = 'turnright'
        # elif 'right' in percept and 'fwd' not in percept and 'bckwd' not in percept:
        #     action = 'turnleft'
        elif 'right' in percept and 'left' in percept and 'fwd' not in percept:
            action = 'forward'
        elif 'fwd' in percept:
            # higher chance of turning left to avoid getting stuck in one location
            action = np.random.choice(['turnleft', 'turnright'], 1, p=[0.8, 0.2])

        else:
            # prefer moving forward to explore
            action = np.random.choice(['forward', 'turnleft', 'turnright'], 1, p=[0.8, 0.1, 0.1])

        self.prev_action = action
        # print('Percept: ', percept_tmp[2])
        # print('Orientation: ', orientations[idx_orient[2]])
        # print('Action ', action)
        return action, idx_orient

    def getPosterior(self, idx_orient, pewnosc):
        # directions in order 'N', 'E', 'S', 'W'
        orientations = ['N', 'E', 'S', 'W']
        P_arr = np.zeros([self.size, self.size, 4], dtype=np.float)

        # put probabilities in the array
        # TODO PUT YOUR CODE HERE
        # OSZACOWANIE
        besty = [np.max(self.P0), np.max(self.P1), np.max(self.P2), np.max(self.P3)]
        for i in range(4):
            pewnosc[i] = pewnosc[i] + besty[i]

        print(pewnosc)
        v_best = -1
        for i in range(4):
            if pewnosc[i] > v_best:
                v_best = pewnosc[i]
                idx_best = i
        if idx_best == 0: super_P = self.P0
        if idx_best == 1: super_P = self.P1
        if idx_best == 2: super_P = self.P2
        if idx_best == 3: super_P = self.P3

        if orientations[idx_orient[idx_best]] == 'N':
            for idx, loc in enumerate(self.locations):
                P_arr[loc[0], loc[1], 0] = super_P[idx]

        if orientations[idx_orient[idx_best]] == 'E':
            for idx, loc in enumerate(self.locations):
                P_arr[loc[0], loc[1], 1] = super_P[idx]

        if orientations[idx_orient[idx_best]] == 'S':
            for idx, loc in enumerate(self.locations):
                P_arr[loc[0], loc[1], 2] = super_P[idx]

        if orientations[idx_orient[idx_best]] == 'W':
            for idx, loc in enumerate(self.locations):
                P_arr[loc[0], loc[1], 3] = super_P[idx]

        return P_arr, pewnosc

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
