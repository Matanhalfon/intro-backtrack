import ex11_map_coloring as re
from ex11_backtrack import general_backtracking
import time

# from map_coloring_gui import color_map #uncomment if you installed the required libraries
SMALL_LIST_OF_COUNTRIES=100
BIGGEST_COUNTRIES=8
MINMAL_RANK = 0


### to implement

def read_adj_file(adjacency_file):
    '''A function that read the file of the Adjacent to each country and than create a dict of each country is
    the key and value is a list of the neighbors and return it
    :param 'a':[1,2,3],'b':[3,4,5]
    :return {'a':[1,2,3],'b':[3,4,5]}'''
    f = open(adjacency_file)
    dic = {}
    for line in f:
        line = line.rstrip().strip("ï»¿")
        (key, val) = line.split(":")
        dic[key] = val.split(',')
        if dic[key] == ['']:
            dic[key] = []
    f.close()
    return dic


def back_track_degree_heuristic(adj_dict, colors):
    '''A function that sort all the countries by num of there neighbors and than preform the
     genral back track'''
    color_dic = {key: None for key in adj_dict}
    block_dic = re.get_land_blocks(adj_dict)
    for block in block_dic:
        list_of_countreys = list(block_dic[block])
        list_of_countreys = sorted(list_of_countreys, key=lambda x: len(adj_dict[x]), reverse=True)
        if not general_backtracking(list_of_countreys, color_dic, 0, colors, re.legal_coloring_func, adj_dict):
            return None
    return color_dic


def mrv_general_backtracking(list_of_items, dict_items_to_vals, index,
                             set_of_assignments, legal_assignment_func, mrv_index_func, dic_of_possbeltes,
                             *args):
    '''A function that choose the index of the country by the minimum of remaining colors
    and then do the back track by so'''
    colors = list(dict_items_to_vals.values())
    if None not in colors:
        return True
    for assigm_val in set_of_assignments:
        index = list_of_items.index(mrv_index_func(list_of_items, dict_items_to_vals,
                                                   dic_of_possbeltes, set_of_assignments))
        old_val = dict_items_to_vals[list_of_items[index]]
        if not legal_assignment_func(dict_items_to_vals, list_of_items[index], assigm_val, *args):
            continue
        dict_items_to_vals[list_of_items[index]] = assigm_val
        nighbors_of_country = args[0][list_of_items[index]]
        for nighbor in nighbors_of_country:
            if assigm_val in dic_of_possbeltes[nighbor]:
                new_possbeltes = dic_of_possbeltes[nighbor][:]
                new_possbeltes.remove(assigm_val)
                dic_of_possbeltes[nighbor] = new_possbeltes
        if mrv_general_backtracking(list_of_items, dict_items_to_vals, index,
                                    set_of_assignments, legal_assignment_func, mrv_index_func, dic_of_possbeltes,
                                    *args):
            return True
        dict_items_to_vals[list_of_items[index]] = old_val
        backtrek_possbeltes(adj_dic, dict_items_to_vals, dic_of_possbeltes, list_of_items[index],
                            assigm_val)

    return False


def mrv_index_get(list_of_items, color_list, possibilities_dic, colors):
    min_long = len(colors)
    mrv_cuntry = None
    for country in list_of_items:
        if color_list[country] != None:
            continue
        if len(possibilities_dic[country]) <= min_long:
            min_long = len(possibilities_dic[country])
            mrv_cuntry = country
    return mrv_cuntry


# def mrv_index_get(list_of_index, dic_of_colors, num_of_colors, dic_of_nighbers):
#     ''' A function that return the index of the country with the minimum_remaining_values '''
#     min_possbeltis = num_of_colors
#     mrv_country = None
#     for country in list_of_index:
#         if dic_of_colors[country] != None:
#             continue
#         num_color_used = 0
#         color_used = ''
#         for neighbor in dic_of_nighbers[country]:
#             if dic_of_colors[neighbor] != None:
#                 if dic_of_colors[neighbor] not in color_used:
#                     color_used += dic_of_colors[neighbor]
#                     num_color_used += 1
#         if num_of_colors - num_color_used <= min_possbeltis:
#             min_possbeltis = num_of_colors - num_color_used
#             mrv_country = country
#     return list_of_index.index(mrv_country)


def back_track_MRV(adj_dict, colors):
    '''A function that operates the  mrv back track '''
    world_color_dic = {}
    block_dic = re.get_land_blocks(adj_dict)
    for block in block_dic:
        dic_of_poobiltes = {key: colors for key in adj_dict}
        color_dic = {key: None for key in block_dic[block]}
        list_of_countreys = list(block_dic[block])
        list_of_countreys = sorted(list_of_countreys, key=lambda x: len(adj_dict[x]))
        if not mrv_general_backtracking(list_of_countreys, color_dic, 0, colors, re.legal_coloring_func, mrv_index_get,
                                        dic_of_poobiltes, adj_dict):
            return None
        world_color_dic.update(color_dic)
    return world_color_dic


def fc_neighbors(country, color, dic_of_possbeltes, dic_of_nighbors):
    '''A function that get a color  and a country and than checks if placeing this color will create a situation
     in which one r more of neighbors will have no more color options'''

    nighbors = dic_of_nighbors[country]
    if nighbors == []:
        return True
    for nighb in nighbors:
        if color in dic_of_possbeltes[nighb]:
            posbel_colors = dic_of_possbeltes[nighb][:]
            posbel_colors.remove(color)
            if posbel_colors == False:
                return False
    return True


def fc_general_backtracking(list_of_items, dict_items_to_vals, index,
                            set_of_assignments, legal_assignment_func, legal_nighbers_assign_func,
                            dic_of_possbeltes, dic_of_nighb):
    '''A function that preform a backtrack in which in every assignment the function also checks if placing the
    color will make one or more of the neighbors to left no more options '''
    if index == len(list_of_items):
        return True
    for assigm_val in set_of_assignments:
        old_val = dict_items_to_vals[list_of_items[index]]
        if not legal_assignment_func(dict_items_to_vals, list_of_items[index], assigm_val, dic_of_nighb):
            continue
        if not legal_nighbers_assign_func(list_of_items[index], assigm_val,
                                          dic_of_possbeltes, dic_of_nighb):
            continue
        dict_items_to_vals[list_of_items[index]] = assigm_val
        for nighbor in dic_of_nighb[list_of_items[index]]:
            if assigm_val in dic_of_possbeltes[nighbor]:
                dic_of_possbeltes[nighbor].remove(assigm_val)
        if fc_general_backtracking(list_of_items, dict_items_to_vals, index + 1,
                                   set_of_assignments, legal_assignment_func, legal_nighbers_assign_func,
                                   dic_of_possbeltes, dic_of_nighb):
            return True
        dict_items_to_vals[list_of_items[index]] = old_val
        backtrek_possbeltes(dic_of_nighb, dict_items_to_vals, dic_of_possbeltes, list_of_items[index],
                            assigm_val)
    return False


def back_track_FC(adj_dict, colors):
    '''A function the preform the FC back trekking'''
    world_color_dic = {key: None for key in adj_dict}
    block_dic = re.get_land_blocks(adj_dict)
    for block in block_dic:
        dic_of_poobiltes = {key: colors[:] for key in adj_dict}
        color_dic = {key: None for key in block_dic[block]}
        list_of_countreys = list(block_dic[block])
        list_of_countreys = sorted(list_of_countreys, key=lambda x: len(adj_dict[x]), reverse=True)
        if not fc_general_backtracking(list_of_countreys, color_dic, 0, colors, re.legal_coloring_func,
                                       fc_neighbors, dic_of_poobiltes, adj_dict):
            return None
        world_color_dic.update(color_dic)
    return world_color_dic


def get_rank(country, color, dic_of_nighbors, dic_of_possbeltis):
    '''A function that return sum of all the colors options for all the nieghbors countryes if the color will be
    placed'''
    rank = 0
    for nighb in dic_of_nighbors[country]:
        rank += len(dic_of_possbeltis[nighb])
        if color in dic_of_possbeltis[nighb]:
            rank -= 1
    return rank


def get_lcv(country, colors, dic_of_possbeltis, used_colors, dic_of_nighb):
    '''A function that return the color with the lowest rank by the function "grt rank" '''
    lcv_color = colors[0]
    lcv_rank = MINMAL_RANK
    for color in colors:
        if color in used_colors:
            continue
        rank = get_rank(country, color, dic_of_nighb, dic_of_possbeltis)
        if rank >= lcv_rank:
            lcv_color = color
            lcv_rank = rank
    return lcv_color, lcv_rank


def update_country_possbiltis(nighbor, color, dict_item_to_val, dict_of_nighbors):
    for nieghbor in dict_of_nighbors[nighbor]:
        if dict_item_to_val[nieghbor] == color:
            return False
    return True


def backtrek_possbeltes(dic_of_nighbors, dict_items_to_vals, dict_of_possbiltis, country, assigm_val):
    for nigbor in dic_of_nighbors[country]:
        if not update_country_possbiltis(nigbor, assigm_val, dict_items_to_vals, dic_of_nighbors):
            continue
        dict_of_possbiltis[nigbor].append(assigm_val)


def LCV_general_backtracking(list_of_items, dict_items_to_vals, index,
                             set_of_assignments, legal_assignment_func, legal_nighbers_assign_func, lcv_func,
                             world_color_dic,
                             dic_of_possbeltes, dic_of_nighbors):
    '''A function that preform the back trek and all ways chose the Least Constraining Value'''
    if index == len(list_of_items):
        return True
    used_colors = []
    for color_num in range(len(set_of_assignments)):
        assigm_val = lcv_func(list_of_items[index], set_of_assignments, dic_of_possbeltes,
                              used_colors, dic_of_nighbors)[0]
        used_colors.append(assigm_val)
        old_val = dict_items_to_vals[list_of_items[index]]
        if not legal_assignment_func(dict_items_to_vals, list_of_items[index], assigm_val, dic_of_nighbors):
            continue
        if not legal_nighbers_assign_func(list_of_items[index], assigm_val,
                                          dic_of_possbeltes, dic_of_nighbors):
            continue
        dict_items_to_vals[list_of_items[index]] = assigm_val
        for nighbor in dic_of_nighbors[list_of_items[index]]:
            if assigm_val in dic_of_possbeltes[nighbor]:
                dic_of_possbeltes[nighbor].remove(assigm_val)
        world_color_dic[list_of_items[index]] = assigm_val
        if LCV_general_backtracking(list_of_items, dict_items_to_vals, index + 1,
                                    set_of_assignments, legal_assignment_func, legal_nighbers_assign_func, lcv_func,
                                    world_color_dic,
                                    dic_of_possbeltes, dic_of_nighbors):
            return True
        dict_items_to_vals[list_of_items[index]] = old_val
        backtrek_possbeltes(dic_of_nighbors, dict_items_to_vals, dic_of_possbeltes, list_of_items[index],
                            assigm_val)
        world_color_dic[list_of_items[index]] = old_val
    return False


def back_track_LCV(adj_dict, colors):
    '''A function the operates the LCV back treack'''
    world_color_dic = {key: None for key in adj_dict}
    block_dic = re.get_land_blocks(adj_dict)
    for block in block_dic:
        dic_of_poobiltes = {key: colors[:] for key in adj_dict}
        color_dic = {key: None for key in block_dic[block]}
        list_of_countreys = list(block_dic[block])
        list_of_countreys = sorted(list_of_countreys, key=lambda x: len(adj_dict[x]), reverse=True)
        if not LCV_general_backtracking(list_of_countreys, color_dic, 0, colors, re.legal_coloring_func,
                                        fc_neighbors, get_lcv, world_color_dic, dic_of_poobiltes, adj_dict):
            return None
    return world_color_dic


# def best_choose(dict_of_neighbors, dict_of_possibilities, )
# def best_index_and_colors(list_of_countryes, used_colors,
#                           dic_of_nighbors, dict_colors, dict_of_possibilities, colors):
#     min_long = len(colors)
#     mrv_cuntry = None
#     best_color = None
#     best_rank = 0
#     for country in list_of_countryes:
#         if dict_colors[country] != None:
#             continue
#         if len(dict_of_possibilities[country]) == min_long:
#             attempt_color, attempt_rank = get_lcv(country, colors, dict_of_possibilities, used_colors,
#                                                   dic_of_nighbors)
#             if attempt_rank >= best_rank:
#                 min_long = len(dict_of_possibilities[country])
#                 mrv_cuntry = country
#                 best_color = attempt_color
#                 best_rank = attempt_rank
#         if len(dict_of_possibilities[country]) < min_long:
#             best_color, best_rank = get_lcv(country, colors, dict_of_possibilities, used_colors, dic_of_nighbors)
#             min_long = len(dict_of_possibilities[country])
#             mrv_cuntry = country
#     return list_of_countryes.index(mrv_cuntry), best_color


def fast_gn_back_trak(list_of_items, dict_items_to_vals, index,
                      set_of_assignments, dict_of_nighb, dict_of_possbeltes,
                      mrv_func, legal_assignment_func, legal_nighbers_assign_func):
    '''the fastest back track option , the function start by place the 8 countries with the most nighbors
      and after that coose the index by the MRV indev function and the function all ways use the FC alghoritem'''
    colors = list(dict_items_to_vals.values())
    if None not in colors:
        return True
    for assigm_val in set_of_assignments:
        if index > 8:
            index=list_of_items.index(
                mrv_func(list_of_items, dict_items_to_vals,dict_of_possbeltes, set_of_assignments))
        old_val = dict_items_to_vals[list_of_items[index]]
        if not legal_assignment_func(dict_items_to_vals, list_of_items[index], assigm_val, dict_of_nighb):
            continue
        if not legal_nighbers_assign_func(list_of_items[index], assigm_val,
                                          dict_of_possbeltes, dict_of_nighb):
            continue
        dict_items_to_vals[list_of_items[index]] = assigm_val
        for nighbor in dict_of_nighb[list_of_items[index]]:
            if assigm_val in dict_of_possbeltes[nighbor]:
                dict_of_possbeltes[nighbor].remove(assigm_val)
        if fast_gn_back_trak(list_of_items, dict_items_to_vals, index+1,
                      set_of_assignments, dict_of_nighb, dict_of_possbeltes,
                      mrv_func, legal_assignment_func, legal_nighbers_assign_func):
            return True
        dict_items_to_vals[list_of_items[index]] = old_val
        backtrek_possbeltes(dict_of_nighb, dict_items_to_vals, dict_of_possbeltes, list_of_items[index],
                            assigm_val)
    return False


def fast_back_track(adj_dict, colors):
    '''The function the activate the fast back trek with i have to dill with a small amount of ccountries(100)
    i use the fc back trek for best time and if more then that i use the fast back trek '''
    dic_of_poobiltes = {key: colors[:] for key in adj_dict}
    color_dic = {key: None for key in dic_of_poobiltes}
    list_of_countreys = list(color_dic.keys())
    list_of_countreys = sorted(list_of_countreys, key=lambda x: len(adj_dict[x]), reverse=True)
    if len(list_of_countreys)>SMALL_LIST_OF_COUNTRIES:
        if not fast_gn_back_trak(list_of_countreys, color_dic, 0, colors[:], adj_dict, dic_of_poobiltes,
                                 mrv_index_get,re.legal_coloring_func, fc_neighbors):
            return None
    else:
        if not  fc_general_backtracking(list_of_countreys, color_dic, 0, colors[:], re.legal_coloring_func,
                                       fc_neighbors,  dic_of_poobiltes, adj_dict):
            return None
    return color_dic


