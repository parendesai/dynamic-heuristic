from helper.utils import print_table
from time import time
from game.tictactoe import TicTacToe
from game.players import *

def play_game(game, *players):
    """Play an n-person, move-alternating game."""

    state = game.initial
    while True:
        for player in players:
            move = player(game, state)
            state = game.result(state, move)
            if game.terminal_test(state):
                print game.utility(state, game.to_move(game.initial))
                return game.utility(state, game.to_move(game.initial))



times_random = []
res = []
for i in xrange(1, 2):
    t = 0
    temp = []
    for j in xrange(1, i+1):
        game = TicTacToe(5, 5, 5)
        t1 = time()
        winner = play_game(game, alphabeta_heuristic_outisde_player, monte_carlo_player)
        t2 = time()
        t += t2-t1
        temp.append(winner)
    times_random.append(t)
    res.append(temp)
        
print "times_random =", times_random
print "Winner = "
print "\n".join(map(lambda val: " ".join(map(str, val)), res))
accuracy = []
for row in res:
    accuracy.append([row.count(1), row.count(-1), row.count(0), len(row), 100.0*row.count(1)/float(len(row)), 100.0*row.count(-1)/float(len(row)), 100.0*row.count(0)/float(len(row))])

print "accuracy = "
print_table(map(lambda val: map(str, val), accuracy), 
            header=["Won", "Lost", "Draw", "Total", "% Win", "% Loss", "% Draw"])
