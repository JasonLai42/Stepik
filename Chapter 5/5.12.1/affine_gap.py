import math
f = open("dataset_317337_8.txt", "r")
inputs = f.readlines()
v = inputs[0].strip('\n')
w = inputs[1].strip('\n')

BLOSUM62_raw = [
'   A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y\n',
'A  4  0 -2 -1 -2  0 -2 -1 -1 -1 -1 -2 -1 -1 -1  1  0  0 -3 -2\n',
'C  0  9 -3 -4 -2 -3 -3 -1 -3 -1 -1 -3 -3 -3 -3 -1 -1 -1 -2 -2\n',
'D -2 -3  6  2 -3 -1 -1 -3 -1 -4 -3  1 -1  0 -2  0 -1 -3 -4 -3\n',
'E -1 -4  2  5 -3 -2  0 -3  1 -3 -2  0 -1  2  0  0 -1 -2 -3 -2\n',
'F -2 -2 -3 -3  6 -3 -1  0 -3  0  0 -3 -4 -3 -3 -2 -2 -1  1  3\n',
'G  0 -3 -1 -2 -3  6 -2 -4 -2 -4 -3  0 -2 -2 -2  0 -2 -3 -2 -3\n',
'H -2 -3 -1  0 -1 -2  8 -3 -1 -3 -2  1 -2  0  0 -1 -2 -3 -2  2\n',
'I -1 -1 -3 -3  0 -4 -3  4 -3  2  1 -3 -3 -3 -3 -2 -1  3 -3 -1\n',
'K -1 -3 -1  1 -3 -2 -1 -3  5 -2 -1  0 -1  1  2  0 -1 -2 -3 -2\n',
'L -1 -1 -4 -3  0 -4 -3  2 -2  4  2 -3 -3 -2 -2 -2 -1  1 -2 -1\n',
'M -1 -1 -3 -2  0 -3 -2  1 -1  2  5 -2 -2  0 -1 -1 -1  1 -1 -1\n',
'N -2 -3  1  0 -3  0  1 -3  0 -3 -2  6 -2  0  0  1  0 -3 -4 -2\n',
'P -1 -3 -1 -1 -4 -2 -2 -3 -1 -3 -2 -2  7 -1 -2 -1 -1 -2 -4 -3\n',
'Q -1 -3  0  2 -3 -2  0 -3  1 -2  0  0 -1  5  1  0 -1 -2 -2 -1\n',
'R -1 -3 -2  0 -3 -2  0 -3  2 -2 -1  0 -2  1  5 -1 -1 -3 -3 -2\n',
'S  1 -1  0  0 -2  0 -1 -2  0 -2 -1  1 -1  0 -1  4  1 -2 -3 -2\n',
'T  0 -1 -1 -1 -2 -2 -2 -1 -1 -1 -1  0 -1 -1 -1  1  5  0 -2 -2\n',
'V  0 -1 -3 -2 -1 -3 -3  3 -2  1  1 -3 -2 -2 -3 -2  0  4 -3 -1\n',
'W -3 -2 -4 -3  1 -2 -2 -3 -3 -2 -1 -4 -4 -2 -3 -3 -2 -3 11  2\n',
'Y -2 -2 -3 -2  3 -3  2 -1 -2 -1 -1 -2 -3 -1 -2 -2 -2 -1  2  7'
]
gap_open_cost = -11
gap_widen_cost = -1

def get_blosum_matrix(text_raw):
    blosum_list = []
    for text in text_raw:
        row = []
        new_text = text.strip('\n').split(' ')
        for word in new_text:
            if word != '':
                row.append(word)
        blosum_list.append(row)
    BLOSUM62_matrix = dict()
    for row in blosum_list[1:]:
        for index in range(1, len(row)):
            BLOSUM62_matrix[(row[0], blosum_list[0][index-1])] = int(row[index])
    return BLOSUM62_matrix

def get_score_matrix(v, w, BLOSUM62):
    global gap_open_cost
    global gap_widen_cost
    
    backtrack = dict()
    
    lower_matrix = dict()
    middle_matrix = dict()
    upper_matrix = dict()
    
    # Initialize matrices
    lower_matrix[(0, 0)] = 0
    middle_matrix[(0, 0)] = 0
    upper_matrix[(0, 0)] = 0
    for i in range(1, len(v) + 1):
        if i > 1:
            upper_matrix[(i, 0)] = upper_matrix[(i - 1, 0)] + gap_widen_cost
            middle_matrix[(i, 0)] = middle_matrix[(i - 1, 0)] + gap_widen_cost
        else:
            upper_matrix[(i, 0)] = gap_open_cost
            middle_matrix[(i, 0)] = gap_open_cost
    for j in range(1, len(w) + 1):
        if j > 1:
            lower_matrix[(0, j)] = lower_matrix[(0, j - 1)] + gap_widen_cost
            middle_matrix[(0, j)] = middle_matrix[(0, j - 1)] + gap_widen_cost
        else:
            lower_matrix[(0, j)] = gap_open_cost
            middle_matrix[(0, j)] = gap_open_cost
            
    # Finalize scoring matrix
    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            lower_matrix[(i, j)] = max(lower_matrix[(i - 1, j)] + gap_widen_cost, middle_matrix[(i - 1, j)] + gap_open_cost)
            upper_matrix[(i, j)] = max(upper_matrix[(i, j - 1)] + gap_widen_cost, middle_matrix[(i, j - 1)] + gap_open_cost)
            middle_matrix[(i, j)] = max(lower_matrix[(i, j)], middle_matrix[(i - 1, j - 1)] + BLOSUM62[(v[i - 1], w[j - 1])], upper_matrix[(i, j)])
            if middle_matrix[(i, j)] == lower_matrix[(i, j)]:
                backtrack[(i, j)] = 'down'
            elif middle_matrix[(i, j)] == middle_matrix[(i - 1, j - 1)] + BLOSUM62[(v[i - 1], w[j - 1])]:
                backtrack[(i, j)] = 'diagonal'
            elif middle_matrix[(i, j)] == upper_matrix[(i, j)]:
                backtrack[(i, j)] = 'right'
    
    return middle_matrix, backtrack
       
def find_alignment(backtrack, score_matrix, v, w, i, j, new_v, new_w):
    if i == 0 and j == 0:
        return new_v, new_w
    else:
        if i == 0:
            return find_alignment(backtrack, score_matrix, v, w, i, j - 1, '-' + new_v, w[j-1] + new_w)
        elif j == 0:
            return find_alignment(backtrack, BLOSUM62, score_matrix, v, w, i - 1, j, v[i-1] + new_v, '-' + new_w)
        else:
            if backtrack[(i, j)] == 'down':
                return find_alignment(backtrack, score_matrix, v, w, i - 1, j, v[i-1] + new_v, '-' + new_w)
            elif backtrack[(i, j)] == 'right':
                return find_alignment(backtrack, score_matrix, v, w, i, j - 1, '-' + new_v, w[j-1] + new_w)
            else:
                return find_alignment(backtrack, score_matrix, v, w, i - 1, j - 1, v[i-1] + new_v, w[j-1] + new_w)

BLOSUM62 = get_blosum_matrix(BLOSUM62_raw)
score_matrix, backtrack = get_score_matrix(v, w, BLOSUM62)
aligned_v, aligned_w = find_alignment(backtrack, score_matrix, v, w, len(v), len(w), "", "")
output_list = [score_matrix[(len(v), len(w))], aligned_v, aligned_w]
with open('output.txt', 'w') as filehandle:
    for listitem in output_list:
        filehandle.write('%s\n' % listitem)
# NOTE: IT DOESN'T WORK ALL OF THE TIME; SOMETIMES A STRAY LETTER IS IN THE GAP