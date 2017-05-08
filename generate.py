from time import time
from game.tictactoe import TicTacToe
from game.players import *
file = open("training_data/dataset.txt", "a")
def play_game(game, *players):
    """Play an n-person, move-alternating game."""
    states = []
    state = game.initial
    while True:
        for player in players:
            move = player(game, state)
            state = game.result(state, move)
            states.append(game.get_board_verbose(state))
            if game.terminal_test(state):
                return {"path": states, "winner": game.utility(state, game.to_move(game.initial))}

# for i in xrange(1, 501):
#     game = TicTacToe(5, 5, 5)
#     game_simulation = play_game(game, random_player, random_player)
#     file.write(str(game_simulation))
#     file.write("\n")

for i in xrange(1, 501):
    game = TicTacToe(5, 5, 5)
    game_simulation = play_game(game, random_player, monte_carlo_player)
    file.write(str(game_simulation))
    file.write("\n")

# for i in xrange(1, 501):
#     game = TicTacToe(5, 5, 5)
#     game_simulation = play_game(game, random_player, minimax_player)
#     file.write(str(game_simulation))
#     file.write("\n")

# for i in xrange(1, 501):
#     game = TicTacToe(5, 5, 5)
#     game_simulation = play_game(game, monte_carlo_player, monte_carlo_player)
#     file.write(str(game_simulation))
#     file.write("\n")

# for i in xrange(1, 501):
#     game = TicTacToe(5, 5, 5)
#     game_simulation = play_game(game, monte_carlo_player, minimax_player)
#     file.write(str(game_simulation))
#     file.write("\n")

# for i in xrange(1, 501):
#     game = TicTacToe(5, 5, 5)
#     game_simulation = play_game(game, monte_carlo_player, random_player)
#     file.write(str(game_simulation))
#     file.write("\n")