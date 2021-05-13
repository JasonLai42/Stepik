fd = open("dataset_317290_11.txt", "r")
n = fd.readline().strip('\n')

def get_binaries(k):
    size = 2**k
    bin_format = "{:0" + str(k) + "b}"
    binaries = []
    for index in range(0, size):
        binaries.append(bin_format.format(index))
    return binaries

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
        
def get_eulerian_cycle():
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
            
            
    return cycle

def get_universal_str(eulerian_cycle):
    universal_str = ""
    for index, komer in enumerate(eulerian_cycle):
        if index == len(eulerian_cycle) - 1:
            break
        else:
            universal_str += komer[0]
    return universal_str

f = get_binaries(int(n))
get_adjacency_list(f, int(n))
get_branches()
get_edges(branch_strings)
eulerian_cycle = get_eulerian_cycle()
universal_str = get_universal_str(eulerian_cycle)
with open('output.txt', 'w') as filehandle:
    filehandle.write('%s\n' % universal_str)