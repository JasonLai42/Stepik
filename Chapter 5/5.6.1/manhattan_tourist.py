fd = open("dataset_317331_10.txt", "r")
inputs = fd.readlines()
nm = inputs[0]
f = inputs[1:]

def get_nm(nm):
    nums = nm.split(' ')
    return int(nums[0]), int(nums[1])

def get_matrix(text_arr):
    grid = []
    for text in text_arr:
        new_text = text.strip('\n')
        nodes = new_text.split(' ')
        for index, node_str in enumerate(nodes):
            nodes[index] = int(node_str)
        grid.append(nodes)
    return grid

def get_matrices(text_arr):
    down = []
    right = []
    divide = -1
    for index, text in enumerate(text_arr):
        if text.strip('\n') == '-':
            divider = index
            break
    if divider != -1:
        down = get_matrix(text_arr[:divider])
        right = get_matrix(text_arr[divider + 1:])
    return down, right

def get_longest_path(n, m, down, right):
    node_maxes = dict()
    node_maxes[(0, 0)] = 0
    for i in range(1, n + 1):
        node_maxes[(i, 0)] = node_maxes[(i - 1, 0)] + down[i - 1][0]
    for j in range(1, m + 1):
        node_maxes[(0, j)] = node_maxes[(0, j - 1)] + right[0][j - 1]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            node_maxes[(i, j)] = max(node_maxes[(i - 1, j)] + down[i - 1][j], node_maxes[(i , j - 1)] + right[i][j - 1])
    print(node_maxes[(n, m)])
    

n, m = get_nm(nm.strip('\n'))
down, right = get_matrices(f)
get_longest_path(n, m, down, right)