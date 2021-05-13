fd = open("dataset_317408_4.txt", "r")
f = fd.readline()

root = dict()
edges = []

def add_suffix(suffix):
    current_node = root
    for character in suffix:
        if current_node.get(character, "DNE") == "DNE": 
            current_node[character] = dict()
            temp = current_node.get(character)
            current_node = temp
        else: 
            current_node = current_node.get(character)

def construct_tree():
    for index, character in enumerate(f.strip('\n')):
        add_suffix(f[index:])
            
def print_edges(node, edge):
    if len(node) == 1:
        for first, second in node.items():
            print_edges(second, edge + first)
    else:
        if not not edge:
            edges.append(edge.strip('\n'))
        for first, second in node.items():
            print_edges(second, first)

construct_tree()
print_edges(root, "")
with open('output.txt', 'w') as filehandle:
    for listitem in edges:
        filehandle.write('%s\n' % listitem)