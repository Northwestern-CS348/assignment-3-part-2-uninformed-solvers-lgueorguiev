from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        ret_lst = list()

        tup1 = self.kb.kb_ask(parse_input("fact: (on ?X peg1)"))
        t1lst = list()

        tup2 = self.kb.kb_ask(parse_input("fact: (on ?X peg2)"))
        t2lst = list()

        tup3 = self.kb.kb_ask(parse_input("fact: (on ?X peg3)"))
        t3lst = list()

        if not tup1:
            pass
        else:
            for i in tup1:
                t1lst.append(int(str(i)[-1]))

        t1lst.sort()
        ret_lst.append(tuple(t1lst))

        if not tup2:
            pass
        else:
            for i in tup2:
                t2lst.append(int(str(i)[-1]))

        t2lst.sort()
        ret_lst.append(tuple(t2lst))

        if not tup3:
            pass
        else:
            for i in tup3:
                t3lst.append(int(str(i)[-1]))

        t3lst.sort()
        ret_lst.append(tuple(t3lst))

        return tuple(ret_lst)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        disk = movable_statement.terms[0].__str__()
        op = movable_statement.terms[1].__str__()
        np = movable_statement.terms[2].__str__()

        self.kb.kb_retract(Fact(Statement(['on', disk, op])))
        self.kb.kb_assert(Fact(Statement(['on', disk, np])))

        if self.kb.kb_ask(Fact(Statement(["onTopOf", disk, '?X']))):
            under = self.kb.kb_ask(Fact(Statement(["onTopOf", disk, '?X'])))[0].bindings_dict['?X']
            self.kb.kb_retract(Fact(Statement(['onTopOf', disk, under])))
        else:
            self.kb.kb_assert(Fact(Statement(['empty', op])))

        if parse_input("fact: (empty %s)" % np):
            self.kb.kb_retract(Fact(Statement(['empty', np])))

        self.kb.kb_retract(Fact(Statement(['top', disk, op])))
        self.kb.kb_assert(Fact(Statement(['top', disk, np])))

        if self.kb.kb_ask(Fact(Statement(['onTopOf', '?X', np]))):
            rep = self.kb.kb_ask(Fact(Statement(['onTopOf', '?X', np])))[0].bindings_dict['?X']
            self.kb.kb_retract(Fact(Statement(['onTop', rep, np])))
            self.kb.kb_assert(Fact(Statement(['onTopOf', disk, rep])))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        t_dict = {"tile1": 1, "tile2": 2, "tile3": 3, "tile4": 4, "tile5": 5, "tile6": 6, "tile7": 7, "tile8": 8, "empty": -1}
        x_dict = {"pos1": 0, "pos2": 1, "pos3": 2}

        list_r1 = [0,0,0]
        for i in self.kb.kb_ask(Fact(Statement(["coordinate", '?tile', '?X', "pos1"]))):
            list_r1[x_dict[i.bindings_dict['?X']]] = t_dict[i.bindings_dict['?tile']]

        list_r2 = [0, 0, 0]
        for i in self.kb.kb_ask(Fact(Statement(["coordinate", '?tile', '?X', "pos2"]))):
            list_r2[x_dict[i.bindings_dict['?X']]] = t_dict[i.bindings_dict['?tile']]

        list_r3 = [0, 0, 0]
        for i in self.kb.kb_ask(Fact(Statement(["coordinate", '?tile', '?X', "pos3"]))):
            list_r3[x_dict[i.bindings_dict['?X']]] = t_dict[i.bindings_dict['?tile']]

        return tuple((tuple(list_r1), tuple(list_r2), tuple(list_r3)))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile_num = movable_statement.terms[0].__str__()
        o_x_posn = movable_statement.terms[1].__str__()
        n_x_posn = movable_statement.terms[3].__str__()
        o_y_posn = movable_statement.terms[2].__str__()
        n_y_posn = movable_statement.terms[4].__str__()

        self.kb.kb_retract(Fact(Statement(['coordinate', tile_num, o_x_posn, o_y_posn])))
        self.kb.kb_assert(Fact(Statement(['coordinate', tile_num, n_x_posn, n_y_posn])))
        self.kb.kb_retract(Fact(Statement(['coordinate', 'empty', n_x_posn, n_y_posn])))
        self.kb.kb_assert(Fact(Statement(['coordinate', 'empty', o_x_posn, o_y_posn])))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
