fd = open("dataset_317290_7.txt", "r")
inputs = fd.readlines()
f = inputs[1:]
n = inputs[0]

adjacency_list = dict()
def get_adjacency_list(text_arr, k):
    global adjacency_list
    size = k - 1
    for text in text_arr:
        text = text.strip('\n')
        komer_branch = text[0:size]
        komer_leaf = text[1:]
        # If we haven't seen this komer yet, add a branch for it in adjacency list
        if adjacency_list.get(komer_branch, "DNE") == "DNE":
            # We don't add it if it's the last komer in the string
            adjacency_list[komer_branch] = []
        adjacency_list[komer_branch].append(komer_leaf)

branch_strings = []
def get_branches():
    global adjacency_list
    global branch_strings
    for k, v in adjacency_list.items():
        branch_str = k + " -> "
        for leaf in sorted(v):
            branch_str += leaf + ","
        branch_str = branch_str[0:-1]
        branch_strings.append(branch_str)
    branch_strings = sorted(branch_strings)

edges = dict()
nodes = []
node_degrees = dict()
def get_edges(text_arr):
    global edges
    global nodes
    global node_degrees
    for text in text_arr:
        new_text = text.strip('\n')
        edge = new_text.split(" -> ")
        source = edge[0]
        destinations = edge[1].split(",")        
        edges[source] = destinations
        nodes.append(source)
        # Sink stuff
        if source in node_degrees:
            node_degrees[source][1] += len(destinations)
        else:
            node_degrees[source] = [0, len(destinations)]
        for dest in destinations:
            if dest in node_degrees:
                node_degrees[dest][0] += 1
            else:
                node_degrees[dest] = [1, 0]
        
def find_sink():
    global node_degrees
    sink = ""
    sink_link = ""
    for k, v in node_degrees.items():
        if v[0] != v[1]:
            if v[0] > v[1]:
                sink = k
            else:
                sink_link = k
        if sink != "" and sink_link != "":
            break
    if sink in edges:
        edges[sink].append(sink_link)
    else:
        edges[sink] = [sink_link]
    return sink
        
def get_eulerian_path(sink):
    global edges
    global nodes
    start_node = list(edges.keys())[0]
    cycle = [start_node]

    # We'll eventually find a cycle
    cycle_not_found = True
    current_node = start_node
    while cycle_not_found:
        cycle.append(edges[current_node][0])
        
        # Pop this edge from the dictionary of edges
        edges[current_node].pop(0)
        # If there are no more edges starting from current_node, we can't visit current_node anymore so delete it
        if len(edges[current_node]) == 0:
            del edges[current_node]
            
        # If the last node we appended is equal to the first, we have a cycle so stop
        if cycle[-1] in edges:
            current_node = cycle[-1]
        else:
            break
    
    # Start random walks from each node in cycle until there are no more edges left
    while len(edges) > 0:
        for index in range(0, len(cycle)):
            if cycle[index] in edges:
                current_node = cycle[index]
                temp_cycle = [current_node]
                while True:
                    temp_cycle.append(edges[current_node][0])

                    if len(edges[current_node]) == 1:
                        del edges[current_node]
                    else:
                        edges[current_node] = edges[current_node][1:]

                    if temp_cycle[-1] in edges:
                        current_node = temp_cycle[-1]
                    else:
                        break

                cycle = cycle[:index] + temp_cycle + cycle[index + 1:]
                break 
            
    # Get the path from the cycle by finding where the sink is and cutting off the lower half and appending to upper 
    path = []
    for index, node in enumerate(cycle):
        if node == sink:
            path = cycle[index + 1:] + cycle[1:index + 1]
            break
    return path

def get_komer_comp(eulerian_path):
    komer_comp = ""
    for index, komer in enumerate(eulerian_path):
        if index == len(eulerian_path) - 1:
            komer_comp += komer
        else:
            komer_comp += komer[0]
    return komer_comp

get_adjacency_list(f, int(n))
get_branches()
get_edges(branch_strings)
sink = find_sink()
eulerian_path = get_eulerian_path(sink)
komer_comp = get_komer_comp(eulerian_path)
with open('output.txt', 'w') as filehandle:
    filehandle.write('%s\n' % komer_comp)