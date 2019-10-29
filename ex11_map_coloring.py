from ex11_backtrack import general_backtracking

# from map_coloring_gui import color_map #uncomment if you installed the required libraries

COLORS = ['red', 'blue', 'green', 'magenta', 'yellow', 'cyan']


### to implement

def read_adj_file(adjacency_file):
    '''A function that read the file and return the ajd dict
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
    return dic


def legal_coloring_func(country_color_dic, country, color, dic_of_nighb):
    '''A function that return true if the color placing is legal and False if not'''
    countreys_to_cheak = dic_of_nighb[country]
    for n_country in countreys_to_cheak:
        if country_color_dic[n_country] == color:
            return False
    return True


def all_connected_countries(dic_of_neighbors, country, set_of_connected):
    '''A function the return a set of all the connected country recursively'''
    set_of_connected.add(country)
    neighbors = dic_of_neighbors[country]
    if set(neighbors) <= set_of_connected:
        return set_of_connected
    for neighbor in neighbors:
        if neighbor not in set_of_connected:
            set_of_connected.add(neighbor)
            all_connected_countries(dic_of_neighbors, neighbor, set_of_connected)
    return set_of_connected


def get_land_blocks(dic_of_nighbors):
    '''A function that  return a dict of all the land blocks in the map
    each block is a set of all the connected countrys'''
    dic_of_blocks = {}
    countries_placed = []
    for country in dic_of_nighbors:
        if country not in countries_placed:
            block = all_connected_countries(dic_of_nighbors, country, set({}))
            dic_of_blocks['block' + country] = block
            countries_placed += [country for country in block]
    return dic_of_blocks


def run_map_coloring(adjacency_file, num_colors=4, map_type=None):
    '''A function that operate the back trek function on the map coloring problam by seting the right
    parameters to the function backtrak'''
    neighbors_dic = read_adj_file(adjacency_file)
    color_dic = {key: None for key in neighbors_dic}
    assiment = COLORS[:num_colors]
    block_dic=get_land_blocks(neighbors_dic)
    for block in block_dic:
        list_of_countreys=list(block_dic[block])
        list_of_countreys = sorted(list_of_countreys, key=lambda x: len(neighbors_dic[x]), reverse=True)
        if not general_backtracking(list_of_countreys, color_dic, 0, assiment, legal_coloring_func, neighbors_dic):
            return None
    return color_dic

