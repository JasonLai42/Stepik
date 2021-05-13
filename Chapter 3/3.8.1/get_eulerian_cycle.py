fd = open("dataset_317290_2.txt", "r")
f = fd.readlines()

edges = dict()
nodes = []
def get_edges(text_arr):
    global edges
    global nodes
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
            
    eulerian_cycle_str = ""
    for node in cycle:
        eulerian_cycle_str += node + "->"
    return eulerian_cycle_str[:-2]

get_edges(f)
eulerian_cycle = get_eulerian_cycle()
with open('output.txt', 'w') as filehandle:
    filehandle.write('%s\n' % eulerian_cycle)