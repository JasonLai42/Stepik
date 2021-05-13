fd = open("dataset_317413_8.txt", "r")
inputs = fd.readlines()
f = inputs[0]
d = inputs[1]

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
pattern_counts = []
    
def construct_BWT_matrix(text):
    global BTW_matrix
    first_column = sorted(text)
    for index, character in enumerate(first_column):
        BWT_matrix[(character, first_col_counts[character])] = (text[index], last_col_counts[text[index]])
        first_col_counts[character] += 1
        last_col_counts[text[index]] += 1
    
def count_rest(text, top, bottom):
    if len(text) < 1:
        return bottom[1] - top[1] + 1
        
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
        return 0
    else:
        return count_rest(text[1:], next_top, next_bot)
        
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
            return 0
        return count_rest(text[1:], top, bottom)
    
def all_pattern_occurrences(text):
    global pattern_counts
    patterns = text.split(' ')
    for pattern in patterns:
        pattern_counts.append(count_occurrences(pattern[::-1]))

construct_BWT_matrix(f.strip('\n'))
all_pattern_occurrences(d.strip('\n'))
with open('output.txt', 'w') as filehandle:
    for listitem in pattern_counts:
        filehandle.write('%s ' % listitem)