import math
f = open("dataset_317335_10.txt", "r")
inputs = f.readlines()
v = inputs[0].strip('\n')
w = inputs[1].strip('\n')

PAM250_raw = [
'   A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y\n',
'A  2 -2  0  0 -3  1 -1 -1 -1 -2 -1  0  1  0 -2  1  1  0 -6 -3\n',
'C -2 12 -5 -5 -4 -3 -3 -2 -5 -6 -5 -4 -3 -5 -4  0 -2 -2 -8  0\n',
'D  0 -5  4  3 -6  1  1 -2  0 -4 -3  2 -1  2 -1  0  0 -2 -7 -4\n',
'E  0 -5  3  4 -5  0  1 -2  0 -3 -2  1 -1  2 -1  0  0 -2 -7 -4\n',
'F -3 -4 -6 -5  9 -5 -2  1 -5  2  0 -3 -5 -5 -4 -3 -3 -1  0  7\n',
'G  1 -3  1  0 -5  5 -2 -3 -2 -4 -3  0  0 -1 -3  1  0 -1 -7 -5\n',
'H -1 -3  1  1 -2 -2  6 -2  0 -2 -2  2  0  3  2 -1 -1 -2 -3  0\n',
'I -1 -2 -2 -2  1 -3 -2  5 -2  2  2 -2 -2 -2 -2 -1  0  4 -5 -1\n',
'K -1 -5  0  0 -5 -2  0 -2  5 -3  0  1 -1  1  3  0  0 -2 -3 -4\n',
'L -2 -6 -4 -3  2 -4 -2  2 -3  6  4 -3 -3 -2 -3 -3 -2  2 -2 -1\n',
'M -1 -5 -3 -2  0 -3 -2  2  0  4  6 -2 -2 -1  0 -2 -1  2 -4 -2\n',
'N  0 -4  2  1 -3  0  2 -2  1 -3 -2  2  0  1  0  1  0 -2 -4 -2\n',
'P  1 -3 -1 -1 -5  0  0 -2 -1 -3 -2  0  6  0  0  1  0 -1 -6 -5\n',
'Q  0 -5  2  2 -5 -1  3 -2  1 -2 -1  1  0  4  1 -1 -1 -2 -5 -4\n',
'R -2 -4 -1 -1 -4 -3  2 -2  3 -3  0  0  0  1  6  0 -1 -2  2 -4\n',
'S  1  0  0  0 -3  1 -1 -1  0 -3 -2  1  1 -1  0  2  1 -1 -2 -3\n',
'T  1 -2  0  0 -3  0 -1  0  0 -2 -1  0  0 -1 -1  1  3  0 -5 -3\n',
'V  0 -2 -2 -2 -1 -1 -2  4 -2  2  2 -2 -1 -2 -2 -1  0  4 -6 -2\n',
'W -6 -8 -7 -7  0 -7 -3 -5 -3 -2 -4 -4 -6 -5  2 -2 -5 -6 17  0\n',
'Y -3  0 -4 -4  7 -5  0 -1 -4 -1 -2 -2 -5 -4 -4 -3 -3 -2  0 10'
]
indel_penalty = -5

def get_pam_matrix(text_raw):
    pam_list = []
    for text in text_raw:
        row = []
        new_text = text.strip('\n').split(' ')
        for word in new_text:
            if word != '':
                row.append(word)
        pam_list.append(row)
    PAM250_matrix = dict()
    for row in pam_list[1:]:
        for index in range(1, len(row)):
            PAM250_matrix[(row[0], pam_list[0][index-1])] = int(row[index])
    return PAM250_matrix

def get_score_matrix(v, w, PAM250, indel_penalty):
    score_matrix = dict()
    score_matrix[(0, 0)] = 0
    for i in range(1, len(v) + 1):
        score_matrix[(i, 0)] = score_matrix[(i - 1, 0)] + indel_penalty 
    for j in range(1, len(w) + 1):
        score_matrix[(0, j)] = score_matrix[(0, j - 1)] + indel_penalty 
        
    max_score = -math.inf
    max_i = len(v)
    max_j = len(w)
    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            insertion_val = score_matrix[(i, j - 1)] + indel_penalty
            deletion_val = score_matrix[(i - 1, j)] + indel_penalty
            match_val = score_matrix[(i - 1, j - 1)] + PAM250[(v[i - 1], w[j - 1])]
            # Free ride: Add 0 to max() to connect source to every node
            score_matrix[(i, j)] = max(0, insertion_val, deletion_val, match_val)
            # Free ride: Get the highest score in our entire matrix and set the sink to this value to connect sink to every node
            # Max i and j keep track of the end of the local alignment
            if score_matrix[(i, j)] > max_score:
                max_score = score_matrix[(i, j)]
                max_i = i
                max_j = j
    score_matrix[(len(v), len(w))] = max_score
    return score_matrix, max_i, max_j
       
def find_alignment(indel_penalty, PAM250, score_matrix, v, w, i, j, new_v, new_w):
    # We find start of local alignment if we hit a node where the score is 0 (we can take a free ride from source to this node)
    if (i == 0 and j == 0) or score_matrix[(i, j)] == 0:
        return new_v, new_w
    else:
        if i == 0:
            return find_alignment(indel_penalty, PAM250, score_matrix, v, w, i, j - 1, '-' + new_v, w[j-1] + new_w)
        elif j == 0:
            return find_alignment(indel_penalty, PAM250, score_matrix, v, w, i - 1, j, v[i-1] + new_v, '-' + new_w)
        else:
            if score_matrix[(i, j)] - indel_penalty == score_matrix[(i - 1, j)]:
                return find_alignment(indel_penalty, PAM250, score_matrix, v, w, i - 1, j, v[i-1] + new_v, '-' + new_w)
            elif score_matrix[(i, j)] - indel_penalty == score_matrix[(i, j - 1)]:
                return find_alignment(indel_penalty, PAM250, score_matrix, v, w, i, j - 1, '-' + new_v, w[j-1] + new_w)
            else:
                return find_alignment(indel_penalty, PAM250, score_matrix, v, w, i - 1, j - 1, v[i-1] + new_v, w[j-1] + new_w)

PAM250 = get_pam_matrix(PAM250_raw)
score_matrix, max_i, max_j = get_score_matrix(v, w, PAM250, indel_penalty)
aligned_v, aligned_w = find_alignment(indel_penalty, PAM250, score_matrix, v, w, max_i, max_j, "", "")
output_list = [score_matrix[(len(v), len(w))], aligned_v, aligned_w]
with open('output.txt', 'w') as filehandle:
    for listitem in output_list:
        filehandle.write('%s\n' % listitem)