"""Games, or Adversarial Search (Chapter 5)"""

from collections import namedtuple
import random

from utils import argmax
from canvas import Canvas

from time import time

infinity = float('inf')
GameState = namedtuple('GameState', 'to_move, utility, board, moves')


def intuition_heuristic(state):
    ret = 0
    for cell in state.board:
        # ret += (1 if state.board[cell] == state.to_move else -1) * (2 - (cell[1]+cell[0])%2)
        # ret += (1 if state.board[cell] == state.to_move else -1) * (1 if cell[0]==cell[1]==2 else 0)
        # ret += (1 if state.board[cell] == state.to_move else -1) * (min(min(cell[0], cell[1]), min(7-cell[0], 7-cell[1])))
        ret += (1 if state.board[cell] == state.to_move else -1) #* (min(min(cell[0], cell[1]), min(7-cell[0], 7-cell[1])))
    # print ret, state.board, state.to_move
    return -1*ret

def monte_carlo(state, game, trials=100):
    def update_scores(state):
        winner = game.utility(state, player)
        for pos in state.board:
            initial_scores[pos[0]-1][pos[1]-1] += (winner)
    
    def get_max_score(state):
        max_score = []
        maximum = -infinity
        for move in state.moves:
            if initial_scores[move[0]-1][move[1]-1] > maximum:
                maximum = initial_scores[move[0]-1][move[1]-1]
                max_score = [move]
            elif initial_scores[move[0]-1][move[1]-1] == maximum:
                max_score.append(move)
        return random.choice(max_score)

    player = game.to_move(state)
    og_state = state
    initial_scores = [[0 for _ in range(game.v)] for __ in range(game.h)]

    for trial in range(trials):
        moves = state.moves
        while moves:
            move = random.choice(moves)
            state = game.result(state, move)
            moves = state.moves
            if not moves:
                break
        update_scores(state)
    return get_max_score(og_state)
# ______________________________________________________________________________
# Minimax Search

def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minimax_decision:
    return argmax(game.actions(state),
                  key=lambda a: min_value(game.result(state, a)))

# ______________________________________________________________________________


def alphabeta_full_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

# ______________________________________________________________________________
# Players for Games
def query_player(game, state):
    "Make a move by querying standard input."
    move_string = input('Your move? ')
    try:
        move = eval(move_string)
    except NameError:
        move = move_string
    return move


def random_player(game, state):
    "A player that chooses a legal move at random."
    return random.choice(game.actions(state))


def alphabeta_player(game, state):
    return alphabeta_full_search(state, game)

def minimax_player(game, state):
    return minimax_decision(state, game)

def alphabeta_heuristic_player(game, state):
    return alphabeta_search(state, game, eval_fn=intuition_heuristic)

def monte_carlo_player(game, state):
    return monte_carlo(state, game)

# ______________________________________________________________________________
def play_game(game, *players):
    """Play an n-person, move-alternating game."""

    state = game.initial
    while True:
        for player in players:
            move = player(game, state)
            state = game.result(state, move)
            if game.terminal_test(state):
                # game.display(state)
                print game.utility(state, game.to_move(game.initial))
                return game.utility(state, game.to_move(game.initial))

# ______________________________________________________________________________
# Some Sample Games


class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        "Return a list of the allowable moves at this point."
        raise NotImplementedError

    def result(self, state, move):
        "Return the state that results from making a move from a state."
        raise NotImplementedError

    def utility(self, state, player):
        "Return the value of this final state to player."
        raise NotImplementedError

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.actions(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print(state)

    def __repr__(self):
        return '<%s>' % self.__class__.__name__



class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        "Legal moves are any square not yet taken."
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print board.get((x, y), '.'), 
            print  

    def compute_utility(self, board, move, player):
        "If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        "Return true if there is a line through move on board for player."
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k

times_random = []

for i in xrange(1, 11):
    t = 0
    for j in xrange(1, i+1):
        game = TicTacToe()
        t1 = time()
        play_game(game, random_player, monte_carlo_player)
        t2 = time()
        t += t2-t1
    times_random.append(t)
        
print "times_random =", times_random
