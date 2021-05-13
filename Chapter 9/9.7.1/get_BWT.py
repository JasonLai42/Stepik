fd = open("dataset_317410_5.txt", "r")
f = fd.readline()

rotations_array = []
BWT = ""

def rotate(text, n):
    first_half = text[0:len(text) - n] 
    second_half = text[len(text) - n:]
    return second_half + first_half
    
def construct_BWT_matrix(text):
    global rotations_array
    for index, character in enumerate(text):
        rotations_array.append(rotate(text, index))
    rotations_array = sorted(rotations_array)
    
def get_BWT_string():
    global rotations_array
    global BWT
    for rotation in rotations_array:
        BWT += rotation[len(rotation)-1]

construct_BWT_matrix(f.strip('\n'))
get_BWT_string()
with open('output.txt', 'w') as filehandle:
        filehandle.write('%s' % BWT)