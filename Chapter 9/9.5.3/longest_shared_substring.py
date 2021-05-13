fd = open("dataset_317408_6.txt", "r")
inputs = fd.readlines()
str1 = inputs[0]
str2 = inputs[1]

f = str1.strip('\n') + str2.strip('\n')

root = dict()
longest = ""
passed_hashtag = 0

def add_suffix(suffix):
    global longest
    global passed_hashtag
    
    possible_longest = ""
    keep_searching = 1
    
    current_node = root
    for character in suffix:
        if current_node.get(character, "DNE") == "DNE": 
            current_node[character] = (passed_hashtag, dict())
            temp = current_node.get(character)[1]
            current_node = temp
            keep_searching = 0
        else: 
            if current_node.get(character)[0] == 0:
                if keep_searching == 1 and passed_hashtag == 1:
                    possible_longest += character
            else:
                keep_searching = 0
            current_node = current_node.get(character)[1]
            
        if keep_searching == 1 and len(possible_longest) >= len(longest):
                longest = possible_longest

def construct_tree():
    global longest
    global passed_hashtag
    
    for index, character in enumerate(f):
        if index >= len(str1):
            passed_hashtag = 1
        add_suffix(f[index:])
    with open('output.txt', 'w') as filehandle:
        filehandle.write('%s' % longest)

construct_tree()