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
import sys
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
    initial = Node(problem.getStartState())
    if problem.isGoalState(problem.getStartState()):
        return initial.total_path()

    fringe = util.Stack()
    fringe.push(initial)
    generated = set()

    while not fringe.isEmpty():
        n = fringe.pop()
        generated.add(n.state)

        for state, action, cost in problem.getSuccessors(n.state):
            succ_node = Node(state, n, action, n.cost + cost)
            if succ_node.state not in generated:
                if problem.isGoalState(succ_node.state):
                    return succ_node.total_path()
                fringe.push(succ_node)
                generated.add(succ_node.state)

    print("No solution")
    sys.exit(-1)


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    initial = Node(problem.getStartState())
    if problem.isGoalState(problem.getStartState()):
        return initial.total_path()

    fringe = util.Queue()
    fringe.push(initial)
    generated = set()
    generated.add(n.state)  # Expanded,
    # Ho posem aquí perque aquesta línia és només útil pel primer node, si no estaria després del pop

    while not fringe.isEmpty():
        n = fringe.pop()

        for state, action, cost in problem.getSuccessors(n.state):
            succ_node = Node(state, n, action, n.cost + cost)
            if succ_node.state not in generated:  # Not in expanded and not in Fringe
                if problem.isGoalState(succ_node.state):
                    return succ_node.total_path()
                fringe.push(succ_node)
                generated.add(succ_node.state)  # Fringe

    print("No solution")
    sys.exit(-1)


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    # fringe = util.NodePriorityQueue()
    # generated = set()
    #
    # inicial = Node(problem.getStartState())
    # if problem.isGoalState(problem.getStartState()):
    #     return inicial.total_path()
    # fringe.push(inicial, 0)
    #
    # while True:
    #     if fringe.isEmpty():
    #         return None
    #     n = fringe.pop()
    #
    #     if problem.isGoalState(n.state):
    #         return n.total_path()
    #     expanded.push(n)
    #
    #     for state, action, cost in problem.getSuccessors(n.state):
    #         node_successor = Node(state, n, action, n.cost + cost)
    #         if not fringe.has_state(node_successor.state) and \
    #                 not expanded.has_state(node_successor.state):
    #             fringe.push(node_successor, node_successor.cost)
    #         elif fringe.has_node_with_higher_cost(node_successor):
    #             fringe.update(node_successor, node_successor.cost)
    initial = Node(problem.getStartState())
    if problem.isGoalState(problem.getStartState()):
        return initial.total_path()

    fringe = util.Queue()
    fringe.push(initial)
    generated = set()

    while not fringe.isEmpty():
        n = fringe.pop()
        generated.add(n.state)

        for state, action, cost in problem.getSuccessors(n.state):
            succ_node = Node(state, n, action, n.cost + cost)
            if succ_node.state not in generated:
                if problem.isGoalState(succ_node.state):
                    return succ_node.total_path()
                fringe.push(succ_node)
                generated.add(succ_node.state)

    print("No solution")
    sys.exit(-1)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    fringe = util.NodePriorityQueue()
    expanded = util.NodeQueue()

    inicial = Node(problem.getStartState())
    if problem.isGoalState(problem.getStartState()):
        return inicial.total_path()
    fringe.push(inicial, 0)

    while True:
        if fringe.isEmpty():
            return None
        n = fringe.pop()

        if problem.isGoalState(n.state):
            return n.total_path()
        expanded.push(n)

        for state, action, cost in problem.getSuccessors(n.state):
            node_successor = Node(state, n, action, n.cost + cost)
            if not fringe.has_state(node_successor.state) and \
                    not expanded.has_state(node_successor.state):
                fringe.push(node_successor, node_successor.cost)
            elif fringe.has_node_with_higher_cost(node_successor):
                fringe.update(node_successor, node_successor.cost)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
