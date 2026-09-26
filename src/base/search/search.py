# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# Questao 1 - DFS

def depthFirstSearch(problem):
    """
    Busca em profundidade (DFS) utilizando busca em grafo.
    Retorna uma lista de ações que leva o Pacman até o objetivo.
    """

    # cria a pilha que armazenará os estados a explorar
    frontier = util.Stack()
    # conjunto de estados já explorados
    expanded = set()
    # obtém o estado inicial
    startState = problem.getStartState()
    # cada elemento contém (estado atual, caminho percorrido)
    frontier.push((startState, []))

    # continua enquanto houver estados na pilha
    while not frontier.isEmpty():
        # remove o último estado inserido
        state, path = frontier.pop()
        # evita expandir estados já visitados
        if state in expanded:
            continue
        # verifica se chegou ao objetivo
        if problem.isGoalState(state):
            return path

        # marca o estado como explorado
        expanded.add(state)

        # pega os sucessores do estado atual
        for nextState, action, cost in problem.expand(state):
            # adiciona os estados ainda não explorados
            if nextState not in expanded:
                # cria o caminho até o sucessor
                newPath = path + [action]
                # insere o sucessor na pilha
                frontier.push((nextState, newPath))

    # retorna lista vazia caso não encontre solução
    return []

# Questao 2 - BFS

def breadthFirstSearch(problem):
    """
    Busca em largura (BFS).

    Encontra um caminho do estado inicial até o objetivo,
    utilizando uma fila para explorar os estados por nível.
    """

    # cria a fila de estados a serem explorados
    frontier = util.Queue()
    # conjunto de estados já visitados
    visited = set()
    # busca o estado inicial
    startState = problem.getStartState()
    # insere o estado inicial e o caminho vazio na fila
    frontier.push((startState, []))
    # marca o estado inicial como visitado
    visited.add(startState)

    # continua enquanto houver estados na fila
    while not frontier.isEmpty():
        # remove o primeiro estado inserido
        state, path = frontier.pop()

        # verifica se o estado atual é o objetivo
        if problem.isGoalState(state):
            return path

        # expande os sucessores do estado atual
        for nextState, action, cost in problem.expand(state):
            # verifica se o sucessor ainda não foi visitado
            if nextState not in visited:
                # marca o sucessor como visitado
                visited.add(nextState)
                # atualiza o caminho até o sucessor
                newPath = path + [action]
                # insere o sucessor no final da fila
                frontier.push((nextState, newPath))

    # retorna uma lista vazia se não encontrar solução
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# Questao 3 - A* Search

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    # fila de prioridade usada pelo algoritmo a* (prioriza menor custo total g + h)
    frontier = util.PriorityQueue()
    start_state = problem.getStartState()
    
    # adiciona o estado inicial com caminho vazio e custo zero
    # a prioridade inicial é apenas a heuristica do estado inicial
    frontier.push((start_state, [], 0), heuristic(start_state, problem))
    
    # dicionario
    visited = dict()
    
    # enquanto houver nós na fronteira
    while not frontier.isEmpty():
        # remove o nó com menor prioridade (menor custo total estimado)
        state, path, cost = frontier.pop()

        # se este estado já foi visitado com custo menor ou igual, ignora
        if state in visited and visited[state] <= cost:
            continue
        
        # registra o custo atual como o menor conhecido para este estado
        visited[state] = cost

        # verifica se o estado atual é o objetivo
        if problem.isGoalState(state):
            return path  # retorna o caminho de ações até o objetivo
        
        # expande o nó atual gerando seus sucessores
        for successor, action, step_cost in problem.expand(state):
            # calcula o novo custo acumulado até o sucessor
            new_cost = cost + step_cost
            # se o sucessor ainda não foi visitado ou encontramos um custo menor
            if successor not in visited or visited[successor] > new_cost:
                # calcula a prioridade como g(n) + h(n)
                priority = new_cost + heuristic(successor, problem)
                # adiciona o sucessor na fronteira com caminho atualizado e nova prioridade
                frontier.push((successor, path + [action], new_cost), priority)

    # se a fronteira esvaziar sem encontrar solução, retorna caminho vazio
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
