fd = open("dataset_317296_2.txt", "r")
f = fd.readlines()

# To keep track where forking branches are
graph_dict = dict()
node_degrees = dict()
def get_graph_dict(text_arr):
    global graph_dict
    global nodes
    for text in text_arr:
        text = text.strip('\n')
        branch = text.split(' -> ')
        children = branch[1].split(',')
        graph_dict[branch[0]] = children
        if branch[0] in node_degrees:
            node_degrees[branch[0]][1] += len(children)
        else:
            node_degrees[branch[0]] = [0, len(children)]
        for child in children:
            if child in node_degrees:
                node_degrees[child][0] += 1
            else:
                node_degrees[child] = [1, 0]

nodes = []
def get_graph_nodes():
    global node_degrees
    global nodes
    for key in node_degrees.keys():
        nodes.append(key)

def get_cycle(node, start_node, curr_path):
    global graph_dict
    if node in graph_dict:
        # Given that this is an isolated cycle where nodes are 1-in-1-out
        curr_path += node + ' -> '
        next_node = graph_dict[node][0]
        del graph_dict[node]
        return get_cycle(next_node, start_node, curr_path)
    else:
        # We deleted the start node to this cycle so if the current_node isn't here, then it must be the start
        if node == start_node:
            curr_path += node
            return [curr_path]
        else:
            return []

def get_maximal_non_branching():
    global graph_dict
    global node_degrees
    global nodes
    path_arrays = []
    for node in nodes:
        degrees = node_degrees[node]
        if degrees[0] != degrees[1]:
            if degrees[1] > 0:
                for next_node in graph_dict[node]:
                    path = [node, next_node]
                    current_node = next_node
                    while node_degrees[current_node][0] == node_degrees[current_node][1]:
                        path.append(graph_dict[current_node][0])
                        current_node = graph_dict[current_node][0]
                    path_arrays.append(path)
                    
    for path in path_arrays:
        for node in path:
            if node in graph_dict:
                del graph_dict[node]
                
    cyclic_nodes = []
    cycles = []
    for key in graph_dict.keys():
        cyclic_nodes.append(key)
    for node in cyclic_nodes:
        if node in graph_dict:
            cycle = get_cycle(node, node, "")
            cycles += cycle
                
    non_branching_paths = []
    for path in path_arrays:
        current_path = ""
        for index, node in enumerate(path):
            current_path += node
            if index != len(path)-1:
                current_path += " -> "
        non_branching_paths.append(current_path)
    return non_branching_paths + cycles

get_graph_dict(f)
get_graph_nodes()
all_paths = get_maximal_non_branching()
with open('output.txt', 'w') as filehandle:
    for listitem in all_paths:
        filehandle.write('%s\n' % listitem)