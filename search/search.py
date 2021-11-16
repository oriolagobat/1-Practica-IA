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

import sys
import util
from node import Node


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

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first."""
    # Creamos y miramos si el nodo incial es objetivo
    initial = Node(problem.getStartState())
    if problem.isGoalState(problem.getStartState()):
        return initial.total_path()

    # Cargamos nodo incial en fringe i generated
    fringe = util.Stack()
    fringe.push(initial)
    generated = set()
    generated.add(initial.state)

    # Entramos en bucle que va sacando nodos de fringe
    # hasta que no este vacio o no se encuentre solución
    while not fringe.isEmpty():
        n = fringe.pop()

        # Generamos sucesores
        for state, action, cost in problem.getSuccessors(n.state):
            succ_node = Node(state, n, action, n.cost + cost)
            if succ_node.state not in generated:
                # Miramos test objectivo
                if problem.isGoalState(succ_node.state):
                    return succ_node.total_path()

                # Si no es objetivo, ponemos nodo en fringe y en generated
                fringe.push(succ_node)
                generated.add(succ_node.state)

    # Si no hemos encontrado solucion, imprimimos y salimos
    print("No solution")
    sys.exit(-1)


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    # Creamos y miramos si el nodo incial es objetivo
    initial = Node(problem.getStartState())
    if problem.isGoalState(problem.getStartState()):
        return initial.total_path()

    # Cargamos nodo incial en fringe i generated
    fringe = util.Queue()
    fringe.push(initial)
    generated = set()
    generated.add(initial.state)

    # Entramos en bucle que va sacando nodos de fringe
    # hasta que no este vacio o no se encuentre solución
    while not fringe.isEmpty():
        n = fringe.pop()

        # Generamos sucesores
        for state, action, cost in problem.getSuccessors(n.state):
            succ_node = Node(state, n, action, n.cost + cost)
            if succ_node.state not in generated:  # Not in expanded and not in Fringe
                if problem.isGoalState(succ_node.state):
                    return succ_node.total_path()

                # Si no es objetivo, ponemos nodo en fringe y en generated
                fringe.push(succ_node)
                generated.add(succ_node.state)  # Fringe

    # Si no hemos encontrado solucion, imprimimos y salimos
    print("No solution")
    sys.exit(-1)


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    # Retornamos el valor de la búsqueda de astar sin especificar heurísticament,
    # puesto que la predefinida es la heurística nula (UCS)
    return aStarSearch(problem)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # Creamos y miramos si el nodo incial es objetivo
    initial = Node(problem.getStartState())
    if problem.isGoalState(problem.getStartState()):
        return initial.total_path()

    # Cargamos nodo incial en fringe i generated
    fringe = util.PriorityQueue()
    generated = {}
    fringe.push(initial, 0)
    generated[initial.state] = ("F", 0 + heuristic(initial.state, problem))

    # Entramos en bucle que va sacando nodos de fringe
    # hasta que no este vacio o no se encuentre solución
    while not fringe.isEmpty():
        n = fringe.pop()

        # Test en sacar del frigne
        if problem.isGoalState(n.state):
            return n.total_path()

        # Si ya hemos expandido nodo, pasamos a la siguiente iteración
        if generated[n.state][0] == "E":
            continue

        # Alternativamente, canviamos el estado del nodo a generado
        generated[n.state] = ("E", n.cost)

        # Bucle de generación de sucesores
        for state, action, cost in problem.getSuccessors(n.state):
            succ_node = Node(state, n, action, n.cost + cost)

            # Si no lo hemos generado, lo metemos en fringe
            if succ_node.state not in generated:
                fringe.push(succ_node, succ_node.cost + heuristic(state, problem))
                generated[succ_node.state] = ("F", succ_node.cost)

            # Si está en fringe pero tiene un coste mayor, actualizamos su coste al menor
            elif generated[succ_node.state][0] == 'F' \
                    and generated[succ_node.state][1] > succ_node.cost:
                fringe.update(succ_node, succ_node.cost)
                generated[succ_node.state] = ("F", succ_node.cost)

    # Si no hemos encontrado solucion, imprimimos y salimos
    print("No solution")
    sys.exit(-1)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
