### to implement

def general_backtracking(list_of_items, dict_items_to_vals, index,
                             set_of_assignments, legal_assignment_func,
                             *args):
        '''A naive function that get some parameters and solve any kind of placeing problam if set in the right
         order.
         the function run over an growing index recursively. the function try to place each assime val in the index
         place of the place spot and than check if the assignment is legal if so it perform the assignment
         and call the function recursively for  the index+1 . if there is no legal options so the function will
         withdrawal to the last point when it had a legal option.
         if the index get to the len of the items we try to place them if the function fales to do so
         it will return False'''
        if index == len(list_of_items):
            return True
        for assigm_val in set_of_assignments:
                old_val = dict_items_to_vals[list_of_items[index]]

                if not legal_assignment_func(dict_items_to_vals, list_of_items[index], assigm_val,*args):
                    continue
                dict_items_to_vals[list_of_items[index]] = assigm_val
                if general_backtracking(list_of_items, dict_items_to_vals, index + 1, set_of_assignments
                        , legal_assignment_func,*args):
                    return True
                dict_items_to_vals[list_of_items[index]] = old_val
        return False


