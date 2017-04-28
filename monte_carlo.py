from random import choice

infinity = float('inf')

def monte_carlo(state, game, trials=10):
    def update_scores(state):
        winner = game.utility(state, player)
        for pos in state.board:
            initial_scores[pos[0]-1][pos[1]-1] += (winner) * (1 if state.board[pos] == player else -1)
    
    def get_max_score(state):
        max_score = []
        maximum = -infinity
        for move in state.moves:
            if initial_scores[move[0]-1][move[1]-1] > maximum:
                maximum = initial_scores[move[0]-1][move[1]-1]
                max_score = [move]
            elif initial_scores[move[0]-1][move[1]-1] == maximum:
                max_score.append(move)
        return choice(max_score)

    player = game.to_move(state)
    og_state = state
    initial_scores = [[0 for _ in range(game.v)] for __ in range(game.h)]

    for trial in range(trials):
        state = og_state
        moves = state.moves
        while moves:
            move = choice(moves)
            state = game.result(state, move)
            if game.terminal_test(state):
                break
            moves = state.moves
        update_scores(state)
    return get_max_score(og_state)


