import copy
import random as rd
import time
import math


horizontal_line = '\u2500'
vertical_line = '\u2502'
left_top = '\u250c'
right_top = '\u2510'
cross_road = '\u253c'

'''
functia euristica este data de diferenta dintre numarul pieselor celor 2 jucatori
'''

def heuristic_f(table, player):
    return get_player_pieces(table, player) - get_player_pieces(table, 3 - player)

'''
functie ajutatoare pentru printarea tablei de joc
'''
def f(a):
    if a == 0:
        return ' '
    if a == 1:
        return 'W'
    return 'B'

'''
returneaza numarul de piese pentru jucatorul player
'''
def get_player_pieces(table, player):
    count = 0
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == player:
                count += 1
    return count

'''
genereaza tabla de start
'''
def generate_start_table():
    ret_table = []
    for i in range(8):
        ret_table.append([])
        for j in range(8):
            ret_table[i].append(0)

    #piesele din mijloc
    ret_table[3][3] = 2
    ret_table[4][4] = 2
    ret_table[3][4] = 1
    ret_table[4][3] = 1

    return ret_table



'''
printarea numerelor de sus
'''
def print_top_line():
    #afisarea liniilor de sus
    print('    ' + '\u250c', end='')
    for i in range(7):
        print('\u2500' + '\u2500' + '\u2500' + '\u252c', end='')
    print('\u2500' + '\u2500' + '\u2500' + '\u2510')

    #afisarea numerelor de sus
    print('    ' + '\u2502', end='')
    for i in range(8):
        print(' ' + str(i + 1) + ' ' + '\u2502', end='')
    print('\n\u250c\u2500\u2500\u2500\u253c', end='')

    #afisarea urmatorului strat de linii
    for i in range(7):
        print('\u2500' + '\u2500' + '\u2500' + '\u253c', end='')
    print('\u2500\u2500\u2500\u2524')

def show_moves(possible_moves):
    ret_list = []
    for i in possible_moves:
        ret_list.append((i[0] + 1, i[1] + 1))
    
    return ret_list

'''
afisarea tabelului
'''
def print_table(table):
    print_top_line()
    for i in range(8):
        #printarea numarului corespunzator liniei
        print(vertical_line + ' ' + str(i + 1) + ' ' + vertical_line, end='')
        for j in range(8):
            print(' ' + f(table[i][j]) + ' ' + vertical_line, end='')
        print()

        #printarea primelor 7 linii din tabel
        if i < 7:
            #printarea numarului
            print('\u251c' + horizontal_line + horizontal_line + horizontal_line, end='')
            #afisarea pieselor
            for j in range(8):
                print(cross_road + horizontal_line + horizontal_line + horizontal_line, end='')
            print('\u2524')
        else:
            #afisarea ultimului strat din tabel
            print('\u2514' + horizontal_line + horizontal_line + horizontal_line, end='')
            for j in range(8):
                print('\u2534' + horizontal_line + horizontal_line + horizontal_line, end='')
            print('\u2518')

'''
obtine linie care trece prin positia piece_position
'''
def get_line(piece_position, table):
    ret_list = []
    for i in range(8):
        ret_list.append(table[piece_position[0]][i])
    return ret_list

'''
obtine coloana care trece prin positia piece_position
'''
def get_column(piece_position, table):
    ret_list = []
    for i in range(8):
        ret_list.append(table[i][piece_position[1]])
    return ret_list

'''
obtine diagonala care trece prin piece_position
'''
def get_diagonal(piece_position, table): 
    y = piece_position[0]
    x = piece_position[1]
    ret_list = ([], [])
    #cazul in care este sub diagonala principala
    if y - x >= 0:
        for i in range(0, 8 - abs(y - x)):
            ret_list[0].append(table[i + abs(y - x)][i])
            ret_list[1].append((i + abs(y - x), i))
    #cazul in care este deasupra diagonalei principale
    else:
        for i in range(0, 8 - abs(y - x)):
            ret_list[0].append(table[i][i + abs(y - x)])
            ret_list[1].append((i, i + abs(y - x)))
    return ret_list

'''
obtine diagonala inversa
'''
def get_inverse_diagonal(piece_position, table):
    y = piece_position[0]
    x = piece_position[1]
    ret_list = ([], [])
    
    #cazul in care este sub diagonala
    if x + y >= 7:
        for i in range(7, x + y - 8, -1):
            ret_list[0].append(table[i][x + y - i])
            ret_list[1].append((i, x + y - i))
    #cazul in care este deasupra diagonalei
    else:
        for i in range(0, x + y + 1):
            ret_list[0].append(table[x + y - i][i])
            ret_list[1].append((x + y - i, i))
    
    
    return ret_list
'''
obtine subsirul din linie care incadreaza
pos intre cele mai apropiate 2 piese de acelasi
fel de pe linie(linie, coloana, diagonala)
'''
def get_closest_positions(player, pos, line):
    i = pos - 1
    j = pos + 1
    top = None
    bottom = None
    #mergem la stange
    while i >= 0:
        if line[i] == player:
            top = i
            break
        i -= 1
    #mergem la dreapta
    while j < len(line):
        if line[j] == player:
            bottom = j
            break
        j += 1

    return (top, bottom)

'''
functia cea mai importanta pentru joc. verifica daca o mutare este valida
si daca da, face schimbarile necesare
'''
def is_valid_move(player, piece_position, table):
    #cazul cand pozitia piece_position este deja ocupata
    if table[piece_position[0]][piece_position[1]] != 0:
        return False
    # cream un tabel temporar pentru ca schimbarile facute pe parcurs
    # sa nu afecteze urmatoarele verificari
    temp_table = copy.deepcopy(table)

    #verificarea coloanei
    line = get_column(piece_position, table)
    column_bool = True
    column_player_vec = []
    column_adv_vec = []

    #adaugam in 2 liste diferite numarul de piese de fiecare tip de pe coloana
    for i in range(8):
        if table[i][piece_position[1]] == player:
            column_player_vec.append((i, piece_position[1]))
        if table[i][piece_position[1]] == 3 - player:
            column_adv_vec.append((i, piece_position[1]))
    
    #daca coloana nu contine piese de ambele tipuri, nu modificam nimic
    if len(column_player_vec) == 0 or len(column_adv_vec) == 0:
        column_bool = False
    else:

        a, b = get_closest_positions(player, piece_position[0], line)
        #in functie de caz, setam startul si finalul subsirului pentru care ar trebui sa schimbam piesele
        if a is not None and b is not None:
            # print('cola')
            start = a
            finish = b
        elif a is None and b is not None:
            # print('colb')
            start = piece_position[0]
            finish = b
        elif b is None and a is not None:
            # print('colc')
            start = a
            finish = piece_position[0]
        else:
            print('cold')
        adv_count = 0

        #verificam daca subsirul corespunde regulilor
        for i in range(start + 1, finish):
            if table[i][piece_position[1]] == 3 - player:
                adv_count += 1
            if table[i][piece_position[1]] == 0 and i != piece_position[0]:
                #print('s-a gasit un spatiu gol pe coloana')
                column_bool = False
                break
        if adv_count == 0:
            column_bool = False
        if column_bool:
            #print('se vor modifica piesele pe coloana')
            for i in range(start, finish):
                if table[i][piece_position[1]] == 3 - player:
                    temp_table[i][piece_position[1]] = 3 - table[i][piece_position[1]]
            temp_table[piece_position[0]][piece_position[1]] = player

    #print('verificam linia piesei')
    line = get_line(piece_position, table)
    line_bool = True
    line_player_vec = []
    line_adv_vec = []
    for i in range(8):
        if table[piece_position[0]][i] == player:
            line_player_vec.append((piece_position[0], i))
        if table[piece_position[0]][i] == 3 - player:
            line_adv_vec.append((piece_position[0], i))

    if len(line_player_vec) == 0 or len(line_adv_vec) == 0:
        #print('nu se afla nicio piesa a jucatorului pe linie')
        line_bool = False
    else:
        # print(piece_position[1], line)
        a, b = get_closest_positions(player, piece_position[1], line)
        # print(a, b)
        if a is not None and b is not None:
            # print('linea')
            start = a
            finish = b
        elif a is None and b is not None:
            # print('lineb')
            start = piece_position[1]
            finish = b
        elif b is None and a is not None:
            # print('linec')
            start = a
            finish = piece_position[1]
        else:
            print('lined')
        adv_count = 0
        for i in range(start + 1, finish):
            if table[piece_position[0]][i] == 3 - player:
                adv_count += 1
            if table[piece_position[0]][i] == 0 and i != piece_position[1]:
                #print('s-a gasit un spatiu gol pe linie')
                line_bool = False
                break
        if adv_count == 0:
            line_bool = False
        if line_bool:
            #print('se vor modifica piesele pe linie')
            for i in range(start + 1, finish):
                if table[piece_position[0]][i] == 3 - player:
                    temp_table[piece_position[0]][i] = 3 - table[piece_position[0]][i]
            temp_table[piece_position[0]][piece_position[1]] = player

    #print('verificam diagonala piesei')
    line, poz_vec = get_diagonal(piece_position, table)
    # print(line, poz_vec)
    diag_bool = True
    diag_player_vec = []
    diag_adv_vec = []
    for i in poz_vec:
        if table[i[0]][i[1]] == player:
            diag_player_vec.append((i[0], i[1]))
        if table[i[0]][i[1]] == 3 - player:
            diag_adv_vec.append((i[0], i[1]))
    if len(diag_player_vec) == 0 or len(diag_adv_vec) == 0:
        #print('nu se afla nicio piesa a jucatorului pe diagonala')
        diag_bool = False
    else:
        # print(diag_adv_vec, diag_player_vec)
        # print(line, poz_vec.index(piece_position))
        a, b = get_closest_positions(player, poz_vec.index(piece_position), line)
        # print(a, b)
        if a is not None and b is not None:
            # print('diaga')
            start = a
            finish = b
        elif a is None and b is not None:
            # print('diagb')
            start = poz_vec.index(piece_position)
            finish = b
        elif b is None and a is not None:
            # print('diagc')
            start = a
            finish = poz_vec.index(piece_position)
        else:
            print('diagd')
        adv_count = 0
        for i in range(start + 1, finish):
            if table[poz_vec[i][0]][poz_vec[i][1]] == 3 - player:
                adv_count += 1
            if table[poz_vec[i][0]][poz_vec[i][1]] == 0 and i is not piece_position:
                #print('s-a gasit un spatiu gol pe diagonala')
                diag_bool = False
                break
        if adv_count == 0:
            diag_bool = False
        if diag_bool:
            #print('se vor modifica piesele pe diagonala')
            for i in range(start + 1, finish):
                if table[poz_vec[i][0]][poz_vec[i][1]] == 3 - player:
                    temp_table[poz_vec[i][0]][poz_vec[i][1]] = 3 - table[poz_vec[i][0]][poz_vec[i][1]]
            temp_table[piece_position[0]][piece_position[1]] = player

    #print('verificam inversa diagonalei piesei')
    line, poz_vec = get_inverse_diagonal(piece_position, table)

    idiag_bool = True
    idiag_player_vec = []
    idiag_adv_vec = []
    for i in poz_vec:
        if table[i[0]][i[1]] == player:
            idiag_player_vec.append((i[0], i[1]))
        if table[i[0]][i[1]] == 3 - player:
            idiag_adv_vec.append((i[0], i[1]))

    if len(idiag_player_vec) == 0 or len(idiag_adv_vec) == 0:
        #print('nu se afla nicio piesa a jucatorului pe inversa diagonalei')
        idiag_bool = False
    else:
        # print(idiag_adv_vec, idiag_player_vec)
        #print(line, poz_vec.index(piece_position))
        a, b = get_closest_positions(player, poz_vec.index(piece_position), line)
        #print(a, b)
        if a is not None and b is not None:
            #print('idiaga')
            start = a
            finish = b
        elif a is None and b is not None:
            #print('idiagb')
            start = poz_vec.index(piece_position)
            finish = b
        elif b is None and a is not None:
            #print('idiagc')
            start = a
            finish = poz_vec.index(piece_position)
        else:
            print('idiagd')
        adv_count = 0
        for i in range(start + 1, finish):
            if table[poz_vec[i][0]][poz_vec[i][1]] == 3 - player:
                adv_count += 1
            if table[poz_vec[i][0]][poz_vec[i][1]] == 0 and i is not piece_position:
                #print('s-a gasit un spatiu gol pe inversa diagonalei')
                idiag_bool = False
                break
        if adv_count == 0:
            idiag_bool = False
        if idiag_bool:
            #print('se vor modifica piesele pe inversa diagonalei')
            for i in range(start + 1, finish):
                if table[poz_vec[i][0]][poz_vec[i][1]] == 3 - player:
                    temp_table[poz_vec[i][0]][poz_vec[i][1]] = 3 - table[poz_vec[i][0]][poz_vec[i][1]]
            temp_table[piece_position[0]][piece_position[1]] = player
    # print(column_bool, line_bool, diag_bool, idiag_bool)
    if column_bool or line_bool or diag_bool or idiag_bool:
        # print(column_bool, line_bool, diag_bool, idiag_bool, piece_position)
        return temp_table
    return False

'''
obtine locurile goale de pe tabla
'''
def get_empty_spots(table):
    count = 0
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == 0:
                count += 1
    return count


def get_all_possible_moves(player, table):
    ret_list = []
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == 0:
                if is_valid_move(player, (i, j), table):
                    ret_list.append((i, j))
    return ret_list

def move(player, piece_position, table):
    temp_table = is_valid_move(player, piece_position, table)
    if not temp_table:
        return False
    return temp_table

def random_metod(possible_moves):
    return possible_moves[rd.randint(0, len(possible_moves) - 1)]



def is_final(table):
    if get_player_pieces(table, 1) == 0 or get_player_pieces(table, 2) == 0:
        return True
    if len(get_all_possible_moves(1, table)) == 0 and len(get_all_possible_moves(2, table)) == 0:
        #print('a')
        return True

    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == 0:
                #print('b')
                return False

    return True  

def get_winner(table):
    nr1_pieces = get_player_pieces(table, 1)
    nr2_pieces = get_player_pieces(table, 2)
    if nr1_pieces > nr2_pieces:
        return 1
    return 2
