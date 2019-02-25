
from solver import *
from queue import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        currState = self.currentState
        vicCond = self.victoryCondition

        if currState.state == vicCond:
            return True
        else:
            if self.gm.getMovables():
                for i in self.gm.getMovables():
                    self.gm.makeMove(i)

                    newState = GameState(self.gm.getGameState(), currState.depth + 1, i)
                    newState.parent = currState

                    self.gm.reverseMove(i)

                    if not newState in self.visited:
                        currState.children.append(newState)

            while True:
                if currState.state == vicCond:
                    return True
                else:
                    index = currState.nextChildToVisit

                    if index < len(currState.children):
                        currState.nextChildToVisit = currState.nextChildToVisit + 1
                        self.gm.makeMove(currState.children[index].requiredMovable)
                        self.currentState = currState.children[index]
                        self.visited[currState] = True

                        if currState.state == vicCond:
                            return True
                        else:
                            return False
                    else:
                        currState = currState.parent

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    que = Queue()
    counter = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        currState = self.currentState
        vicCond = self.victoryCondition

        if currState.state == vicCond:
            if not self.que.empty():
                while not self.que.empty():
                    self.que.get()
            return True

        else:
            if (self.gm.getMovables()):
                for i in self.gm.getMovables():
                    self.gm.makeMove(i)
                    child = GameState(self.gm.getGameState(), 0, i)
                    currState.children.append(child)
                    child.parent = currState
                    self.gm.reverseMove(i)

            for i in currState.children:
                if i not in self.visited:
                    self.que.put(i)
            if self.que.empty():
                pass
            else:
                while not self.que.empty():
                    child = self.que.get()

                    if child not in self.visited:
                        lower = list()

                        while currState.requiredMovable:
                            lower.append(currState.requiredMovable)
                            currState = currState.parent
                        currState = child
                        upper = list()

                        while currState.requiredMovable:
                            upper.append(currState.requiredMovable)
                            currState = currState.parent
                        upper = reversed(upper)

                        for i in lower:
                            self.gm.reverseMove(i)

                        for i in upper:
                            self.gm.makeMove(i)

                        self.visited[child] = True
                        self.currentState = child
                        self.counter+=1
                        self.currentState.depth = self.counter
                        break
