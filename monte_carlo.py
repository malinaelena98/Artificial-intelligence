from othello_game import *
import random as rd
import copy

def convert(table):
    tmp = copy.deepcopy(table)
    for i, row in enumerate(table):
        tmp[i] = tuple(row)
    return tuple(tmp)
    
def ucb1_function(node_dict, node, it):
    node = node_dict[node]
    return node[0] / node[1] + (2 * math.log(it) / node[1]) ** 1 / 2

def get_node(player, table):
    return (player, convert(table))

def get_next_nodes(player, table, possible_moves):
    ret_list = []
    for mov in possible_moves:
        ret_list.append(get_node(3 - player, move(player, mov, table)))
    return ret_list

def get_best_node(children, it, node_dict):
    arg = 0
    maxv = 0
    for node in children:
        if maxv < ucb1_function(node_dict, node, it):
            maxv = ucb1_function(node_dict, node, it)
            arg = node
    return arg

def get_empty_nodes(children, node_dict):
    ret_list = []
    for node in children:
        if node not in node_dict.keys():
            ret_list.append((node, children.index(node)))
    return ret_list


if __name__ == '__main__':
    nodes = dict()
    count = 0
    for i in range(100000):
        parcurs = []
        table = generate_start_table()
        player = 1
        print('incepe iteratia %s' % (i + 1))
        while not is_final(table):
            #print_table(table)
            curr_node = (player, convert(table))
            if curr_node in nodes.keys():
                nodes[curr_node][1] += 1
            else:
                nodes[curr_node] = [0, 1]
            #print(nodes[curr_node])

            parcurs.append(curr_node)

            pos_movs = get_all_possible_moves(player, table)
            if len(pos_movs) == 0:
                player = 3 - player
                pos_movs = get_all_possible_moves(player, table)

            if player == 1:
                mov = random_metod(pos_movs)

            if player == 2:
                child_nodes = get_next_nodes(player, table, pos_movs)
                empty_child_nodes = get_empty_nodes(child_nodes, nodes)
                if len(empty_child_nodes) > 0:
                    print('a', end='')
                    mov = pos_movs[empty_child_nodes[rd.randint(0, len(empty_child_nodes) - 1)][1]]
                else:
                    print('b', end='')
                    mov = pos_movs[child_nodes.index(get_best_node(child_nodes, i + 1, nodes))]

            table = move(player, mov, table)
            player = 3 - player
        #print_table(table)
        if get_winner(table) == 2:
            count += 1
            print(count)
            for i in parcurs:
                nodes[i][0] += 1
