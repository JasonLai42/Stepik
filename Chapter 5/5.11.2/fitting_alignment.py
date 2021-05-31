import math
f = open("dataset_317336_5.txt", "r")
inputs = f.readlines()
v = inputs[0].strip('\n')
w = inputs[1].strip('\n')

match_cost = 1
edit_cost = -1

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
            score_matrix[(i, j)] = max(insertion_val, deletion_val, match_val)
      
    max_score = -math.inf
    max_i = 0
    for i in range(len(w), len(v) + 1):
        if score_matrix[(i, len(w))] > max_score:
            max_score = score_matrix[(i, len(w))]
            max_i = i
    return score_matrix, max_i
       
def find_alignment(score_matrix, v, w, i, j, new_v, new_w):
    global edit_cost
    # We find start of local alignment if we hit a node where the score is 0 (we can take a free ride from source to this node)
    if j == 0:
        return new_v, new_w
    else:
        if i == 0:
            return find_alignment(score_matrix, v, w, i, j - 1, '-' + new_v, w[j-1] + new_w)
        elif j == 0:
            return find_alignment(score_matrix, v, w, i - 1, j, v[i-1] + new_v, '-' + new_w)
        else:
            if score_matrix[(i, j)] - edit_cost == score_matrix[(i - 1, j)]:
                return find_alignment(score_matrix, v, w, i - 1, j, v[i-1] + new_v, '-' + new_w)
            elif score_matrix[(i, j)] - edit_cost == score_matrix[(i, j - 1)]:
                return find_alignment(score_matrix, v, w, i, j - 1, '-' + new_v, w[j-1] + new_w)
            else:
                return find_alignment(score_matrix, v, w, i - 1, j - 1, v[i-1] + new_v, w[j-1] + new_w)

score_matrix, max_i = get_score_matrix(v, w)
aligned_v, aligned_w = find_alignment(score_matrix, v, w, max_i, len(w), "", "")
output_list = [score_matrix[(max_i, len(w))], aligned_v, aligned_w]
with open('output.txt', 'w') as filehandle:
    for listitem in output_list:
        filehandle.write('%s\n' % listitem)