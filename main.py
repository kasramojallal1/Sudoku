class Node:
    def __init__(self, number, color, x, y):
        global n_dimension, colors

        self.number = number
        self.color = color
        self.available_numbers = []
        self.available_colors = []
        self.x = x
        self.y = y

        for i in range(1, n_dimension + 1):
            self.available_numbers.append(str(i))

        for color in colors:
            self.available_colors.append(color)

    def init_availability(self):
        if self.number in self.available_numbers:
            self.available_numbers.remove(self.number)

        # if self.color in self.available_colors:
        #     self.available_colors.remove(self.color)

    def get_info(self):
        return str(self.number) + str(self.color)


def if_goal(grid):
    global n_dimension

    # for i in range(n_dimension):
    #     for j in range(n_dimension):
    #
    #         number = grid[i][j].number
    #
    #         for k in range(n_dimension):
    #             if k == j:
    #                 continue
    #             if number == grid[i][k].number:
    #                 return 'failure'
    #
    #         for p in range(n_dimension):
    #             if p == i:
    #                 continue
    #             if number == grid[p][j].number:
    #                 return 'failure'

    for node_list in grid:
        for node in node_list:

            x = node.x
            y = node.y
            neighbours = []

            for node_list2 in grid:
                for node2 in node_list2:
                    if node2.x == x and node2.y == y:
                        continue
                    if node2.x == x and node2.y != y:
                        neighbours.append(node2)
                    if node2.y == y and node2.x != x:
                        neighbours.append(node2)

            for node3 in neighbours:
                if node3.number == node.number:
                    return 'fail'


            if node.number == '*':
                return 'fail'


    return 'goal_reached'


def update_node(grid, node):
    global n_dimension, color_values

    x = node.x
    y = node.y

    # number
    for i in range(n_dimension):
        if i == y:
            continue
        if grid[x][i].number in node.available_numbers:
            node.available_numbers.remove(grid[x][i].number)

    for i in range(n_dimension):
        if i == x:
            continue
        if grid[i][y].number in node.available_numbers:
            node.available_numbers.remove(grid[i][y].number)

    # # color
    # try:
    #     node2 = grid[x - 1][y]
    #     if node2.color in node.available_colors:
    #         node.available_colors.remove(node2.color)
    # except IndexError:
    #     pass
    #
    # try:
    #     node2 = grid[x + 1][y]
    #     if node2.color in node.available_colors:
    #         node.available_colors.remove(node2.color)
    # except IndexError:
    #     pass
    #
    # try:
    #     node2 = grid[x][y - 1]
    #     if node2.color in node.available_colors:
    #         node.available_colors.remove(node2.color)
    # except IndexError:
    #     pass
    #
    # try:
    #     node2 = grid[x][y + 1]
    #     if node2.color in node.available_colors:
    #         node.available_colors.remove(node2.color)
    # except IndexError:
    #     pass


def show_grid(grid):
    global n_dimension

    for i in range(n_dimension):
        for j in range(n_dimension):
            print(grid[i][j].number + grid[i][j].color, end=' ')
        print('')


def show_availability(grid):
    global n_dimension

    for i in range(n_dimension):
        for j in range(n_dimension):
            node = grid[i][j]
            print(str(node.available_numbers) + '*' + str(node.available_colors), end='  *  ')
        print('')


def init_nodes(grid):
    global n_dimension
    node_grid = [[] for i in range(n_dimension)]

    for i in range(n_dimension):
        for j in range(n_dimension):
            string = grid[i][j]
            number = string[0]
            color = string[1]
            node = Node(number, color, i, j)
            node.init_availability()
            node_grid[i].append(node)

    for node_list in node_grid:
        for node in node_list:
            update_node(node_grid, node)

    return node_grid


def get_inputs():
    f = open('test_case.txt', "r")

    string = f.readline()
    string = string.split()
    m = int(string[0])
    n = int(string[1])

    string = f.readline()
    string = string.split()
    colors = []
    for i in range(len(string)):
        colors.append(string[i])

    color_values = {'r': 1,
                    'g': 2,
                    'b': 3,
                    'y': 4,
                    'p': 5}

    grid = [[] for i in range(n)]

    for i in range(n):
        string = f.readline()
        string = string.split()
        grid[i] = string


    return grid, colors, n, color_values


def get_degree(grid, node):
    count = 0
    x = node.x
    y = node.y

    neighbours = []

    for node_list in grid:
        for node in node_list:
            if node.x == x and node.y == y:
                continue
            if node.x == x and node.y != y:
                neighbours.append(node)
            if node.y == y and node.x != x:
                neighbours.append(node)

    for node in neighbours:
        if node.number == '*':
            count += 1

    return count


def select_mrv_degree(grid):
    mrv_selected = 1000
    degree_selected = -1000

    for node_list in node_grid:
        for node in node_list:
            if node.number == '*':
                if len(node.available_numbers) + len(node.available_colors) < mrv_selected:
                    mrv_selected = len(node.available_numbers) + len(node.available_colors)

    mrv_champions = []

    for node_list in node_grid:
        for node in node_list:
            if node.number == '*':
                if len(node.available_numbers) + len(node.available_colors) == mrv_selected:
                    mrv_champions.append(node)

    for node in mrv_champions:
        if get_degree(grid, node) > degree_selected:
            degree_selected = get_degree(grid, node)

    for node in mrv_champions:
        if get_degree(grid, node) == degree_selected:
            return node


def assign_number(node):
    if len(node.available_numbers) >= 1:
        return node.available_numbers[0]
    else:
        return 'noting left'



def main_function(list_grid):

    grid = list_grid[-1]

    if if_goal(grid) == 'goal_reached':
        print('---------goal-----------------')
        show_grid(grid)
        # show_availability(grid)
        exit()

    node = select_mrv_degree(grid)
    node_sel = node
    value = assign_number(node)
    node.number = value
    number_sel = value

    x = node.x
    y = node.y

    neighbours = []

    for node_list in grid:
        for node in node_list:
            if node.x == x and node.y == y:
                continue
            if node.x == x and node.y != y:
                neighbours.append(node)
            if node.y == y and node.x != x:
                neighbours.append(node)

    for selected_node in neighbours:
        update_node(grid, selected_node)

    show_grid(grid)
    print('-------------------')
    # show_availability(grid)

    for node_list in grid:
        for node in node_list:
            if len(node.available_numbers) == 0:
                if node.number == '*':
                    list_grid.pop()
                    back_track(list_grid, node_sel, number_sel)


    list_grid.append(grid)
    actions.append([node_sel, number_sel])
    main_function(list_grid)


def back_track(grid_list1, node, number):

    print('****************************backtrack****************************************')

    grid = grid_list1[-1]

    x = node.x
    y = node.y
    neighbours = []

    node.available_numbers.remove(number)

    # if len(node.available_numbers) == 0:
    #     grid_list1.pop()

    for node_list in grid:
        for node in node_list:
            if node.x == x and node.y == y:
                continue
            if node.x == x and node.y != y:
                neighbours.append(node)
            if node.y == y and node.x != x:
                neighbours.append(node)

    for node2 in neighbours:
        node2.available_numbers.append(number)

    main_function(grid_list1)




if __name__ == '__main__':
    my_grid, colors, n_dimension, color_values = get_inputs()
    node_grid = init_nodes(my_grid)

    show_grid(node_grid)
    print('-------------------')
    # show_availability(node_grid)

    my_grids = [node_grid]
    actions = []

    main_function(my_grids)
