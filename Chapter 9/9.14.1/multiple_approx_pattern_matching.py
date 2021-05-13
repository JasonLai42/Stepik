fd = open("dataset_317417_10.txt", "r")
inputs = fd.readlines()
f = inputs[0]
d = inputs[1]
n = int(inputs[2].strip('\n'))

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
        rotations_array.append((rotate(text, index), len(text) - index - 2))
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
    
def count_rest(text, path, n):
    if n < 0:
        return
    else:
        if len(text) == 1:
            if BWT_matrix[path][0] == text[0]:
                pattern_indices.append(index_in_text[path])
                return
            else:
                if n - 1 >= 0:
                    pattern_indices.append(index_in_text[path])
                return
    
    if BWT_matrix[path][0] == text[0]:
        count_rest(text[1:], BWT_matrix[path], n)
    else:
        count_rest(text[1:], BWT_matrix[path], n-1)
        
def count_occurrences(text, n):
    if len(text) >= 1:
        global BWT_matrix
        for key in BWT_matrix:
            if BWT_matrix[key][0] == text[0]:
                count_rest(text[1:], BWT_matrix[key], n)
            else:
                count_rest(text[1:], BWT_matrix[key], n-1)
        return
    
def all_pattern_occurrences(text, n):
    global pattern_counts
    patterns = text.split(' ')
    for pattern in patterns:
        count_occurrences(pattern[::-1], n)

construct_BWT_matrix(BWT)
all_pattern_occurrences(d, n)
pattern_indices = sorted(pattern_indices)
with open('output.txt', 'w') as filehandle:
    for listitem in pattern_indices:
        filehandle.write('%s ' % listitem)