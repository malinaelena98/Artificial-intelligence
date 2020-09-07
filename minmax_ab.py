from othello_game import *

def minmax_alfa_beta(player, table, possible_moves, max_depth):
    tmp_tbl = copy.deepcopy(table)
    move = val_max(player, tmp_tbl, -10000, 10000, 0, min(max_depth, len(possible_moves)))
    return move[0]

def val_max(player, table, alfa, beta, curr_depth, max_depth):
    if curr_depth >= max_depth:
        return (None, heuristic_f(table, player))

    val_max = -10000
    optimum_act = None
    pos_movs = get_all_possible_moves(player, table)
    for i in pos_movs:
        act, val = val_min(3 - player, move(player, i, table), alfa, beta, curr_depth + 1, max_depth)
        if act is None:
            act = i
        
        if val_max < val:
            val_max = val
            optimum_act = i
        if val_max >= beta:
            return optimum_act, val_max
        alfa = max(val_max, alfa)
    return optimum_act, val_max

def val_min(player, table, alfa, beta, curr_depth, max_depth):
    if curr_depth >= max_depth:
        return (None, heuristic_f(table, player))

    val_min = 10000
    optimum_act = None
    pos_movs = get_all_possible_moves(player, table)
    for i in pos_movs:
        act, val = val_max(3 - player, move(player, i, table), alfa, beta, curr_depth + 1, max_depth)
        if act is None:
            act = i
        if val_min > val:
            val_min = val
            optimum_act = i
        if alfa >= val_min:
            return(optimum_act, val_min)
        beta = min(val_min, beta)
    return (optimum_act, val_min)



if __name__ == '__main__':
    table = generate_start_table()
    print('incepe jocul')
    player = 1
    
    while not is_final(table):
        print_table(table)
        pos_movs = get_all_possible_moves(player, table)
        tmp_pos_movs = show_moves(pos_movs)
        if len(pos_movs) == 0:
            player = 3 - player
            pos_movs = get_all_possible_moves(player, table)
        
        if player == 1:
            print('alegeti una din urmatoarele mutari', tmp_pos_movs)
            # mov = random_metod(pos_movs)
            mov = input('introduceti mutarea:\n')
            mov = (int(mov[0]), int(mov[1]))
            while mov not in pos_movs:
                mov = input('mutare gresita, introduceti alta')
                mov = (int(mov[0]) - 1, int(mov[1]) - 1)

        else:
            print('va muta calculatorul')
            print('calculatorul are de ales din urmatoarele mutari:', pos_movs)
            mov = minmax_alfa_beta(player, table, pos_movs, 5)


        print((mov[0] + 1, mov[1] + 1))


        tmp = move(player, mov, table)
        table = copy.deepcopy(tmp)
        player = 3 - player
    print_table(table)

    max_p = max(get_player_pieces(table, 1), get_player_pieces(table, 2))

    print('s-a terminat jocul, iar castigatorul este %s' % (f(get_winner(table))))