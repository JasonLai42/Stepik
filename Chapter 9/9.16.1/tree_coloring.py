fd = open("dataset_317419_6.txt", "r")
inputs = fd.readlines()
dash_index = 0
for index, line in enumerate(inputs):
    if line == '-\n':
        dash_index = index
f = inputs[0:dash_index]
d = inputs[dash_index + 1:]

node_colors = dict()
tree = dict()
full_mapping = []
    
def add_leaf_colors(leaves):
    global node_colors
    for leaf in leaves:
        leaf_color = leaf.strip('\n').split(': ')
        node_colors[leaf_color[0]] = leaf_color[1]
    
def construct_tree(nodes):
    global tree
    for node in nodes:
        node_children = node.strip('\n').split(' -> ')
        if node_children[1] == "{}":
            continue
        tree[node_children[0]] = node_children[1].split(',')
        
def color_tree():
    global node_colors
    global tree
    while not not tree:
        nodes_to_pop = []
        for node in tree.items():
            not_ripe = 0
            is_red = 0
            is_blue = 0
            for child in node[1]:
                color = node_colors.get(child, "DNE")
                if color == "DNE":
                    not_ripe = 1
                    break
                elif color == "red":
                    is_red = 1
                elif color == "blue":
                    is_blue = 1
                else:
                    is_red = 1
                    is_blue = 1
                    break
            if not_ripe == 1:
                continue
            elif is_red == 1 and is_blue == 1:
                node_colors[node[0]] = "purple"
            elif is_red == 1 and is_blue == 0:
                node_colors[node[0]] = "red"
            else:
                node_colors[node[0]] = "blue"
            nodes_to_pop.append(node[0])
                
        for node in nodes_to_pop:
            tree.pop(node)
        
def get_output():
    global node_colors
    global full_mapping
    for pair in node_colors.items():
        full_mapping.append(pair[0] + ": " + pair[1])
    full_mapping = sorted(full_mapping)
    
add_leaf_colors(d)
construct_tree(f)
color_tree()
get_output()
with open('output.txt', 'w') as filehandle:
    for listitem in full_mapping:
        filehandle.write('%s\n' % listitem)