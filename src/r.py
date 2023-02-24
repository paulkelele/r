#https://towardsdatascience.com/reinforcement-learning-implement-tictactoe-189582bea542
#https://towardsdatascience.com/implement-grid-world-with-q-learning-51151747b455
#https://towardsdatascience.com/reinforcement-learning-with-sarsa-a-good-alternative-to-q-learning-algorithm-bf35b209e1c

import numpy as np
import pickle
import pathlib
import os

ROWS = 3
COLS = 3

class Agent():
    def __init__(self,name,symbol,exp_rate=0.3) -> None:
        self.name = name
        self.symbol = symbol
        self.exp_rate = exp_rate
        self.lr = 0.2
        self.decay_gamma = 0.9
        self.states = []
        self.states_value = {}
        
    def flattenBoard(self, board):
        flattenBoard = str(board.reshape(ROWS, COLS))
        return flattenBoard
    
    def addState(self, state):
        self.states.append(state)
    
    # determine la meilleure action
    def chooseAction(self,positions,board):
        if np.ramdom.uniform(0,1) <= self.exp_rate:
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            max_value = -999
            for p in positions:
                next_board = board.copy()
                next_board[p] = self.symbol
                new_board_flatten = self.flattenBoard(next_board)
                value = 0 if self.states_value.get(new_board_flatten) is None else self.states_value.get(new_board_flatten)
                if value >= max_value:
                    max_value = value
                    action = p
        return action

    # application de la recompense
    def applyReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]
    
    # enregistrement de la policy
    def save(self):
        f = pathlib.Path('p_' + str(self.name))
        if f.exists():
            f = open('p_' + str(self.name), 'rb')
            reloaded_states_value = pickle.load(f)
            for x in reloaded_states_value:
                for y in self.states_value:
                    if(x == y):
                        if reloaded_states_value[x] < self.states_value[y]:
                            reloaded_states_value[x] = self.states_value[y]
                        else:
                            self.states_value[y] = reloaded_states_value[x]
            reloaded_states_value.update(self.states_value)
            f = open('p_' + str(self.name),'wb')
            pickle.dump(reloaded_states_value,f)
            f.close()
        else:
            if len(self.states_value) > 0:
                f = open('p_' + str(self.name),'wb')
                pickle.dump(self.states_value,f)
                f.close()

    # chargement de la politique
    def load(self):
        f = pathlib.Path('p_' + str(self.name))
        if f.exists():
            if os.path.getsize(f) > 0:
                f = open('p_' + str(self.name), 'rb')
                self.states_value = pickle.load(f)
                f.close()
                #print(self.states_value)
    

# Environnement
class Environnement:
    def __init__(self, agent:Agent, user) -> None:
        self.board = np.zeros((ROWS,COLS))
        self.isEnd = False
        self.agent = agent
        self.user = user
    
    def availablePositions(self):
        positions = []
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions
        
    def trainning(self):
        pass
    
    
######################################
if __name__ == "__main__":
    # save(states_value)
    # load(states_value)
    pass

# states_value = {'b':60, 'c':20}

# def save(states_value):
#     f = pathlib.Path('p')
#     if f.exists():
#         f = open('p', 'rb')
#         reloaded_states_value = pickle.load(f)
#         for x in reloaded_states_value:
#             for y in states_value:
#                 if(x == y):
#                     if reloaded_states_value[x] < states_value[y]:
#                         reloaded_states_value[x] = states_value[y]
#                     else:
#                         states_value[y] = reloaded_states_value[x]
#         reloaded_states_value.update(states_value)
#         f = open('p','wb')
#         pickle.dump(reloaded_states_value,f)
#         f.close()
#     else:
#         if len(states_value) > 0:
#             f = open('p','wb')
#             pickle.dump(states_value,f)
#             f.close()
        

# def load(states_value):
#     f = pathlib.Path('p')
#     if f.exists():
#         if os.path.getsize(f) > 0:
#             f = open('p', 'rb')
#             states_value = pickle.load(f)
#             f.close()
#             print(states_value)