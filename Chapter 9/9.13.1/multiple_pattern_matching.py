fd = open("dataset_317416_4.txt", "r")
f = fd.readline()
d = fd.readlines()[1:]

# Convert string to BWT

# Will store the different rotations of text; the ending character of that rotation is what is appended to BWT, so store the 
# index of that character (in the original string) as well so we can get the index where patterns (suffixes) start
rotations_array = []
BWT = ""

def rotate(text, n):
    first_half = text[0:len(text) - n] 
    second_half = text[len(text) - n:]
    return second_half + first_half
    
def construct_BWT_matrix(text):
    global rotations_array
    for index, character in enumerate(text):
        rotations_array.append((rotate(text, index), len(text) - index - 1))
    rotations_array = sorted(rotations_array, key=lambda x: x[0])
    
def get_BWT_string():
    global rotations_array
    global BWT
    for rotation in rotations_array:
        BWT += rotation[0][len(rotation[0])-1]

construct_BWT_matrix(f.strip('\n') + '$')
get_BWT_string()

# Get the indices

first_col_counts = {
    'A' : 1,
    'T' : 1,
    'C' : 1,
    'G' : 1,
    '$' : 1
}

last_col_counts = {
    'A' : 1,
    'T' : 1,
    'C' : 1,
    'G' : 1,
    '$' : 1
}

BWT_matrix = dict()
index_in_text = dict()
pattern_indices = []
    
def construct_BWT_matrix(text):
    global BTW_matrix
    first_column = sorted(text)
    for index, character in enumerate(first_column):
        BWT_matrix[(character, first_col_counts[character])] = (text[index], last_col_counts[text[index]])
        # rotations_array was sorted in the order of the BWT, so the second part of this elements tuple is this character's 
        # index in the original string; we can store it in the index_to_text dictionary for fast lookup of this character's 
        # index
        index_in_text[(text[index], last_col_counts[text[index]])] = rotations_array[index][1]
        first_col_counts[character] += 1
        last_col_counts[text[index]] += 1
    
def count_rest(text, top, bottom):
    if len(text) < 1:
        index = top[1]
        while(index <= bottom[1]):
            pattern_indices.append(index_in_text[(top[0], index)])
            index += 1
        return
        
    next_top = ()
    next_bot = ()
    
    top_index = top[1]
    bot_index = bottom[1]
    top_found = 0
    bot_found = 0        
    while top_index <= bot_index and (top_found == 0 or bot_found == 0):
        if top_found == 0 and BWT_matrix[(top[0], top_index)][0] == text[0]:
            next_top = BWT_matrix[(top[0], top_index)]
            top_found = 1
        elif top_found == 0:
            top_index += 1
            
        if bot_found == 0 and BWT_matrix[(bottom[0], bot_index)][0] == text[0]:
            next_bot = BWT_matrix[(bottom[0], bot_index)]
            bot_found = 1
        elif bot_found == 0:
            bot_index -= 1
    if top_found == 0 and bot_found == 0:
        return
    else:
        count_rest(text[1:], next_top, next_bot)
        
def count_occurrences(text):
    if len(text) >= 1:
        global BWT_matrix
        top = ()
        bottom = ()
        for key in BWT_matrix:
            if BWT_matrix[key][0] == text[0]:
                top = BWT_matrix[key]
                break
        for key in reversed(BWT_matrix):
            if BWT_matrix[key][0] == text[0]:
                bottom = BWT_matrix[key]
                break
        if not top or not bottom:
            return
        count_rest(text[1:], top, bottom)
        return
    
def all_pattern_occurrences(patterns):
    global pattern_counts
    for pattern in patterns:
        count_occurrences(pattern.strip('\n')[::-1])

construct_BWT_matrix(BWT)
all_pattern_occurrences(d)
pattern_indices = sorted(pattern_indices)
with open('output.txt', 'w') as filehandle:
    for listitem in pattern_indices:
        filehandle.write('%s ' % listitem)