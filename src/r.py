import pickle
import pathlib
import os

states_value = {'b':10}

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