root = dict()

def construct_trie():
    f = open("dataset_317406_4.txt", "r")

    new_node_num = 1
    for pattern in f:
        current_node = root
        parent_num = 0
        for character in pattern.strip('\n'):
            if current_node.get(character, "DNE") == "DNE": 
                current_node[character] = (parent_num, new_node_num, dict())
                temp = current_node.get(character)[2]
                current_node = temp
                parent_num = new_node_num
                new_node_num += 1
            else: 
                parent_num = current_node.get(character)[1]
                current_node = current_node.get(character)[2]

    f.close()
    
def iterate_trie(node):
    for first, second in node.items():
        print(second[0],'->',second[1],':' + first, sep='')
        iterate_trie(second[2])

construct_trie()
iterate_trie(root)