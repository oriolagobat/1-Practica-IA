"""
Programa para representar los diferentes nodos
"""
from collections import namedtuple

class Node:
    """
    Esta clase representa un nodo, con el cual identificaremos los estados de nuestros problemas,
    con los diferentes parametros nodo padre, accion, y coste acumulado
    """
    def __init__(self, _state, _parent=None, _action=None, _cost=0):
        self.state = _state
        self.parent = _parent
        self.action = _action
        self.cost = _cost

    def total_path_rec(self):
        """
        Devuelve el coste total del camino para llegar a ese nodo, calculado de manera recursiva
        """
        if not self.parent:
            return []
        return self.parent.total_path_rec() + [self.action]

    def total_path(self):
        """
        Devuelve el coste total del camino para llegar a ese nodo
        """
        current_state = self
        actions = []
        while current_state.parent:
            actions += [current_state.action]
            current_state = current_state.parent
        return actions[::-1]

    def __str__(self):
        return "Node[%s,%s,%d]" % (self.state, self.action, self.cost)

    def __repr__(self):
        return self.__str__()


def test_robot():
    """
    Funcion para hacer tests para la clase nodo
    """
    # For the problem of the robot cleaning two cells
    State = namedtuple("State", "cell clean0 clean1")
    # de las dos celdas.
    root = Node(State(0, False, False))
    step1 = Node(
        State(0, True, False),
        root, "SWEEP"
    )
    step2 = Node(
        State(1, True, False),
        step1, "MOVE"
    )
    step3_1 = Node(
        State(0, True, False),
        step2, "MOVE"
    )
    step3_2 = Node(
        State(1, True, True),
        step2, "SWEEP"
    )

    print(root)
    print([root, step1])
    print(step3_1.total_path())
    print(step3_2.total_path())


if __name__ == "__main__":
    test_robot()
