import math
f = open("dataset_317336_7.txt", "r")
inputs = f.readlines()
v = inputs[0].strip('\n')
w = inputs[1].strip('\n')

match_cost = 1
edit_cost = -2

def get_score_matrix(v, w):
    global match_cost
    global edit_cost
    score_matrix = dict()
    score_matrix[(0, 0)] = 0
    for i in range(1, len(v) + 1):
        score_matrix[(i, 0)] = 0
    for j in range(1, len(w) + 1):
        score_matrix[(0, j)] = 0
    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            match = edit_cost
            if v[i - 1] == w[j - 1]:
                match = match_cost
            
            insertion_val = score_matrix[(i, j - 1)] + edit_cost
            deletion_val = score_matrix[(i - 1, j)] + edit_cost
            match_val = score_matrix[(i - 1, j - 1)] + match
            score_matrix[(i, j)] = max(match_val, insertion_val, deletion_val)  
    max_i = 0
    max_j = 0
    highest_score = -math.inf
    # Scores for suffixes of v will be on the last row
    for j in range(1, len(w) + 1):
        if score_matrix[(len(v), j)] > highest_score:
            highest_score = score_matrix[(len(v), j)]
            max_i = len(v)
            max_j = j
    return score_matrix, max_i, max_j
       
def find_alignment(score_matrix, v, w, i, j, new_v, new_w):
    global match_cost
    global edit_cost
    # Only backtrack until we hit the end of w's prefix
    if j == 0:
        return new_v, new_w
    else:
        if i == 0:
            return find_alignment(score_matrix, v, w, i, j - 1, '-' + new_v, w[j-1] + new_w)
        else:
            if score_matrix[(i, j)] - edit_cost == score_matrix[(i - 1, j)]:
                return find_alignment(score_matrix, v, w, i - 1, j, v[i-1] + new_v, '-' + new_w)
            elif score_matrix[(i, j)] - edit_cost == score_matrix[(i, j - 1)]:
                return find_alignment(score_matrix, v, w, i, j - 1, '-' + new_v, w[j-1] + new_w)
            else:
                return find_alignment(score_matrix, v, w, i - 1, j - 1, v[i-1] + new_v, w[j-1] + new_w)

score_matrix, i, j = get_score_matrix(v, w)
aligned_v, aligned_w = find_alignment(score_matrix, v, w, i, j, "", "")
output_list = [score_matrix[(i, j)], aligned_v, aligned_w]
with open('output.txt', 'w') as filehandle:
    for listitem in output_list:
        filehandle.write('%s\n' % listitem)