f = open("dataset_317333_7.txt", "r")
inputs = f.readlines()
start = int(inputs[0].strip('\n'))
end = int(inputs[1].strip('\n'))
graph_raw = inputs[2:]

edge_weights = dict()
sources_for_node = dict()

def get_graph(graph_raw):
    global edge_weights
    global incoming_edges
    for edge_str in graph_raw:
        edge = edge_str.strip('\n').split('->')
        edge = edge[:-1] + edge[1].split(':')
        # edge is [source, destination, weight]
        for index, value in enumerate(edge):
            edge[index] = int(value)
        edge_weights[(edge[0], edge[1])] = edge[2]
        if sources_for_node.get(edge[1], "DNE") == "DNE":
            sources_for_node[edge[1]] = [edge[0]]
        else:
            sources_for_node[edge[1]].append(edge[0])
    
node_maxes = dict()

def get_longest_path(start, end):
    global node_maxes
    node_maxes[start] = [0, -1]
    for index in range(start, end + 1):
        if sources_for_node.get(index, "DNE") != "DNE":
            max_val = -1
            src = -1
            for source in sources_for_node[index]:
                if node_maxes[source][0] + edge_weights[(source, index)] > max_val:
                    max_val = node_maxes[source][0] + edge_weights[(source, index)]
                    src = source
            node_maxes[index] = [max_val, src]

def backtrack(next_node, path):
    global node_maxes
    if next_node == -1:
        return path[1:]
    else:
        return backtrack(node_maxes[next_node][1], [node_maxes[next_node][1]] + path)
        
def format_path(end, path):
    output_list = []
    output_list.append(node_maxes[end][0])
    path_str = str(path[0])
    for index in range(1, len(path)):
        path_str += '->' + str(path[index])
    output_list.append(path_str)
    return output_list

get_graph(graph_raw)
get_longest_path(start, end)
path = backtrack(end, [end])
output_list = format_path(end, path)
with open('output.txt', 'w') as filehandle:
    for listitem in output_list:
        filehandle.write('%s\n' % listitem)