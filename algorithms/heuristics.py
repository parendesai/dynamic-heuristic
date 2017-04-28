def intuition_heuristic(state):
    ret = 0
    player = state.to_move
    for cell in state.board:
        ret += (1 if state.board[cell] == player else -1)
    return ret

def outside_heuristic(state):
    ret = 0
    player = state.to_move
    for cell in state.board:
        ret += (1 if state.board[cell] == state.to_move else -1) * (min(min(cell[0], cell[1]), min(5-cell[0], 5-cell[1])))