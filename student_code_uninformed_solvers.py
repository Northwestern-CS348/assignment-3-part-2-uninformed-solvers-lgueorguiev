
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
    q = Queue()
    move_counter = 0

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
        movables = self.gm.getMovables()
        visited = self.visited
        if self.currentState.state == self.victoryCondition:  # check to make sure we're not already at victory state

            if (self.q != self.q.empty()):
                while not self.q.empty():
                    self.q.get()
            return True

        if (movables):
            for i in movables:
                self.gm.makeMove(i)
                child = GameState(self.gm.getGameState(), 0, i)
                self.currentState.children.append(child)
                child.parent = self.currentState
                self.gm.reverseMove(i)

        for i in self.currentState.children:
            if i not in visited:
                self.q.put(i)

        while not self.q.empty():

            child = self.q.get()

            if child not in visited:
                curr = self.currentState
                base = []

                while (curr.requiredMovable):
                    base.append(curr.requiredMovable)
                    curr = curr.parent
                curr = child
                branch = []

                while curr.requiredMovable:
                    branch.append(curr.requiredMovable)
                    curr = curr.parent
                branch = reversed(branch)

                for k in base:
                    self.gm.reverseMove(k)

                for j in branch:
                    self.gm.makeMove(j)

                visited[child] = True
                self.currentState = child
                self.move_counter = self.move_counter + 1
                self.currentState.depth = self.move_counter
                break
