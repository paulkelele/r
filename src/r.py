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
    def __init__(self,name,exp_rate=0.3) -> None:
        self.name = name
        self.exp_rate = exp_rate
        self.lr = 0.2
        self.decay_gamma = 0.9
        self.etat = []
        self.states_value = {}
        
    def flattenBoard(self, board):
        flattenBoard = str(board.reshape(ROWS, COLS))
        return flattenBoard
    
    def addState(self, state):
        self.states.append(state)
    
    def chooseAction(self,positions,board,symbol):
        if np.ramdom.uniform(0,1) <= self.exp_rate:
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            max_value = -999
            for p in positions:
                next_board = board.copy()
                next_board[p] = symbol
                new_board_flatten = self.flattenBoard(next_board)
                value = 0 if self.states_value.get(new_board_flatten) is None else self.states_value.get(new_board_flatten)
                if value >= max_value:
                    max_value = value
                    action = p
        return action

    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]
            
    
class Environement:
    def __init__(self) -> None:
        pass

states_value = {'b':60, 'c':20}

def save(states_value):
    f = pathlib.Path('p')
    if f.exists():
        f = open('p', 'rb')
        reloaded_states_value = pickle.load(f)
        for x in reloaded_states_value:
            for y in states_value:
                if(x == y):
                    if reloaded_states_value[x] < states_value[y]:
                        reloaded_states_value[x] = states_value[y]
                    else:
                        states_value[y] = reloaded_states_value[x]
        reloaded_states_value.update(states_value)
        f = open('p','wb')
        pickle.dump(reloaded_states_value,f)
        f.close()
    else:
        if len(states_value) > 0:
            f = open('p','wb')
            pickle.dump(states_value,f)
            f.close()
        

def load(states_value):
    f = pathlib.Path('p')
    if f.exists():
        if os.path.getsize(f) > 0:
            f = open('p', 'rb')
            states_value = pickle.load(f)
            f.close()
            print(states_value)

if __name__ == "__main__":
    save(states_value)
    load(states_value)