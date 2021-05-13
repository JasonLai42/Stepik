fd = open("dataset_317406_8.txt", "r")
f = fd.readlines()

root = dict()
indices = []

def construct_trie():
    new_node_num = 1
    for pattern in f[1:]:
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

def test_string(text_suffix, node):
    if not node:
        return 1
    
    if not text_suffix or node.get(text_suffix[0], "DNE") == "DNE":
        return 0
    else:
        return test_string(text_suffix[1:], node.get(text_suffix[0])[2])

def iterate_text(text):
    for index, character in enumerate(text):
        if test_string(text[index:], root) == 1:
            indices.append(index)

construct_trie()
iterate_text(f[0].strip('\n'))
with open('output.txt', 'w') as filehandle:
    for listitem in indices:
        filehandle.write('%s ' % listitem)