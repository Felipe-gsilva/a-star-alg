import numpy as np 
import copy
import heapq 
from dataclasses import dataclass
from enum import Enum


def heuristic_one(current_state:np.array, desired_state:np.array):

    """
    Function that implements counter of wrong position for heuristic one
    """

    counter = 0
    for i in range(len(current_state)):
        for j in range(len(current_state)):
            counter += current_state[i, j] != desired_state[i, j]

    return counter

def heuristic_two(current_state:np.array, desired_state:np.array) -> int:

    """
    Function that implements Manhattan Distance for heuristic two
    """

    dist = 0
    for i in range(len(current_state)): 
        for j in range(len(current_state)): 
            if current_state[i, j] == 0: 
                continue 
            xi, xj = np.where(desired_state == current_state[i, j])
            dist += abs(i - xi)[0] + abs(j-xj)[0]

    return dist


def init_table(n_pieces:int) -> set:
    """
    Function that initializes the table randomly, where '0' is the empty position 
    """

    sqr = int(np.sqrt(n_pieces))
    table = np.arange(n_pieces)

    desired_state = copy.deepcopy(table)
    np.random.shuffle(table)

    table = table.reshape(sqr,sqr)
    desired_state = desired_state.reshape(sqr, sqr)

    return table, desired_state

@dataclass
class Node: 
    g:int 
    h: int 

    state: np.array 
    parent: object

    def __lt__(self, other):
        return self.g + self.h < other.g + other.h

    def __hash__(self):
        return hash(tuple(self.state.flatten()))
    
    def __eq__(self, other):
        if not isinstance(other, Node):  # FIX 3: guard para comparações mistas
            return False
        return np.array_equal(self.state, other.state)

def verify_action(state:np.array):

    i, j = np.where(state == 0)  
    i,j = i[0], j[0]
    actions = []

    if i - 1 >= 0:  
        actions.append(((i,j), (i-1, j)))
    if i + 1 < state.shape[0]:  
        actions.append(((i,j), (i+1, j)))
    if j - 1 >= 0:  
        actions.append(((i,j), (i, j-1)))
    if j + 1 < state.shape[1]:  
        actions.append(((i,j), (i, j+1)))
    
    return actions



def swap_values(state_copy:np.array, action:tuple):
    i,j = action[0]
    xi,xj = action[1]

    state_copy[i, j], state_copy[xi, xj] =  state_copy[xi,xj], state_copy[i, j]
    

def estimate(node: Node, edge: list, actions: list, desired_state: np.array, heuristic):  # FIX 4: recebe heuristic e desired_state
    for a in actions:
        st_copy = copy.deepcopy(node.state)
        swap_values(st_copy, a)
        
        h = heuristic(st_copy, desired_state)
        new_node = Node(node.g + 1, h, st_copy, parent=node)
        
        heapq.heappush(edge, new_node)



def search(table:np.array, desired_state:np.array, heuristic=heuristic_one):
    h0 = heuristic(table, desired_state)
    node =  Node(0, h0, table, parent=None)
    edge = []
    heapq.heappush(edge, node)

    explored = set()
    while True:
        if not edge: return False
        node = heapq.heappop(edge)
        if node in explored:
            continue

        if np.array_equal(node.state, desired_state):
            return True  
        
        explored.add(node)
        actions = verify_action(node.state)
        estimate(node, edge, actions, desired_state, heuristic)
    

table, desired_state = init_table(9)
print(table)
print(desired_state)
print(search(table, desired_state, heuristic=heuristic_one))   # FIX 4: chama a função, não só referencia
print(search(table, desired_state, heuristic=heuristic_two))