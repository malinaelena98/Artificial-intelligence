from othello_game import *


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
            mov = (int(mov[0]) - 1, int(mov[1]) - 1)
            while mov not in pos_movs:
                mov = input('mutare gresita, introduceti alta')
                mov = (int(mov[0]), int(mov[1]))

        else:
            print('calculatorul are de ales din urmatoarele mutari:', tmp_pos_movs)
            mov = random_metod(pos_movs)


        print(mov)


        tmp = move(player, mov, table)
        table = copy.deepcopy(tmp)
        # print_table(table)
        player = 3 - player
        #time.sleep(5)

    print_table(table)

    max_p = max(get_player_pieces(table, 1), get_player_pieces(table, 2))

    print('s-a terminat jocul, iar castigatorul este %s' % (f(get_winner(table))))