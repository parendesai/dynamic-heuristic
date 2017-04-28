def intuition_heuristic(state):
    ret = 0
    player = game.to_move(state)
    for cell in state.board:
        ret += (1 if state.board[cell] == player else -1)
    return ret

def outside_heuristic(state):
    ret = 0
    player = game.to_move(state)
    for cell in state.board:
        ret += (1 if state.board[cell] == state.to_move else -1) * (min(min(cell[0], cell[1]), min(game.h-cell[0], game.v-cell[1])))