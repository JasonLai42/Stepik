f = open("dataset_317342_3.txt", "r")
inputs = f.readlines()

def get_graph(graph_raw):
    graph = dict()
    incoming_edges = dict()
    non_candidates = dict()
    for edge_str in graph_raw:
        edge = edge_str.strip('\n').split(' -> ')
        destinations = edge[1].split(',')
        for destination in destinations:
            if graph.get(edge[0], "DNE") == "DNE":
                graph[edge[0]] = [destination]
            else:
                graph[edge[0]].append(destination)
            if incoming_edges.get(destination, "DNE") == "DNE":
                incoming_edges[destination] = 1
            else:
                incoming_edges[destination] += 1
            non_candidates[destination] = 1
            
    return graph, incoming_edges, non_candidates

def get_topo_order(graph, incoming_edges, non_candidates):
    ordering = []
    candidates = []
    for source, destination in graph.items():
        if non_candidates.get(source, "DNE") == "DNE":
            candidates.append(source)
    while len(candidates) > 0:
        curr_node = candidates[0]
        candidates.pop(0)
        ordering.append(curr_node)
        if graph.get(curr_node, "DNE") == "DNE":
            continue
        else:
            for dest in graph[curr_node]:
                incoming_edges[dest] -= 1
                if incoming_edges[dest] <= 0:
                    candidates.append(dest)
                    del incoming_edges[dest]
            del graph[curr_node]
    if len(graph) != 0:
        return "the input graph is not a DAG"
    else:
        return ordering
    

graph, incoming_edges, non_candidates = get_graph(inputs)
# print(graph)
# print(non_candidates)
ordering = get_topo_order(graph, incoming_edges, non_candidates)
with open('output.txt', 'w') as filehandle:
    for listitem in ordering:
        filehandle.write('%s, ' % listitem)