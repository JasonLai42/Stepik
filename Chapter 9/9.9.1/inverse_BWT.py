fd = open("dataset_317412_10.txt", "r")
f = fd.readline()

first_col_counts = {
    'A' : 0,
    'T' : 0,
    'C' : 0,
    'G' : 0,
    '$' : 0
}

last_col_counts = {
    'A' : 0,
    'T' : 0,
    'C' : 0,
    'G' : 0,
    '$' : 0
}

BWT_matrix = dict()
original_str = ""
    
# Note, the matrix is actually reversed in the dictionary i.e. the last column is key and first column is value
def construct_BWT_matrix(text):
    global BTW_matrix
    first_column = sorted(text)
    for index, character in enumerate(first_column):
        BWT_matrix[(text[index], last_col_counts[text[index]])] = (character, first_col_counts[character])
        first_col_counts[character] += 1
        last_col_counts[text[index]] += 1
    
def get_original_string(text):
    global BWT_matrix
    global original_str
    
    current_key = ('$', 0)
    i = 0
    while(i < len(text)):
        original_str += BWT_matrix[current_key][0]
        current_key = BWT_matrix[current_key]
        i += 1
        

construct_BWT_matrix(f.strip('\n'))
get_original_string(f.strip('\n'))
with open('output.txt', 'w') as filehandle:
        filehandle.write('%s' % original_str)