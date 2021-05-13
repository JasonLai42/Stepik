fd = open("dataset_317424_8.txt", "r")
inputs = fd.readlines()
f = inputs[0].strip('\n')
d = inputs[1].strip('\n')
e = inputs[2].strip('\n')

root = dict()
edges = []

def construct_tree(text, sfx_arr_str, lcp_str):
    suffix_array = sfx_arr_str.split(', ')
    lcp = lcp_str.split(', ')
    last_branch = root
    for index, pos in enumerate(suffix_array):
        suffix = text[int(pos):]
        lcp_val = int(lcp[index])
        current_node = root
        if lcp_val > 0:
            for character in suffix[0:lcp_val]:
                current_node = current_node.get(character)
        for character in suffix[lcp_val:]:
                current_node[character] = dict()
                current_node = current_node.get(character)

def print_edges(node, edge):
    if len(node) == 1:
        for first, second in node.items():
            print_edges(second, edge + first)
    else:
        if not not edge:
            edges.append(edge.strip('\n'))
        for first, second in node.items():
            print_edges(second, first)
       
construct_tree(f, d, e)
print_edges(root, "")
with open('output.txt', 'w') as filehandle:
    for listitem in edges:
        filehandle.write('%s\n' % listitem)