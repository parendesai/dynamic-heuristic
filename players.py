from random import choice
from monte_carlo import monte_carlo
from minimax import minimax_decision
from heuristics import intuition_heuristic, outside_heuristic
from alphabeta import alphabeta_full_search, alphabeta_search

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
    return choice(game.actions(state))

def monte_carlo_player(game, state):
    return  monte_carlo(state, game, trials=10)

def minimax_player(game, state):
    return minimax_decision(state, game)

def alphabeta_player(game, state):
    return alphabeta_full_search(state, game)

def alphabeta_heuristic_outisde_player(game, state):
    return alphabeta_search(state, game, eval_fn=outside_heuristic)

def alphabeta_heuristic_intuition_player(game, state):
    return alphabeta_search(state, game, eval_fn=intuition_heuristic)