fd = open("dataset_317408_7.txt", "r")
inputs = fd.readlines()
str1 = inputs[0]
str2 = inputs[1]

f1 = str1.strip('\n') + str2.strip('\n')
f2 = str2.strip('\n') + str1.strip('\n')

root = dict()
shortest = f1
passed_hashtag = 0

def add_suffix(suffix):
    global shortest
    global passed_hashtag
    
    possible_shortest = ""
    keep_searching = 1
    
    current_node = root
    for character in suffix:
        if current_node.get(character, "DNE") == "DNE": 
            if passed_hashtag == 1 and keep_searching == 1 and len(possible_shortest) <= len(shortest):
                possible_shortest += character
                shortest = possible_shortest
            keep_searching = 0
            
            current_node[character] = (passed_hashtag, dict())
            current_node = current_node.get(character)[1]
        else: 
            if current_node.get(character)[0] == 0:
                if passed_hashtag == 1:
                    possible_shortest += character
            else:
                keep_searching = 0
            current_node = current_node.get(character)[1]

def construct_tree(text, strsize):
    global shortest
    global passed_hashtag
    
    root.clear()
    passed_hashtag = 0
    for index, character in enumerate(text):
        if index >= strsize:
            passed_hashtag = 1
        add_suffix(text[index:])

construct_tree(f1, len(str1))
construct_tree(f2, len(str2))
with open('output.txt', 'w') as filehandle:
        filehandle.write('%s' % shortest)