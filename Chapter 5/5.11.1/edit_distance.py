f = open("dataset_317336_3.txt", "r")
inputs = f.readlines()
v = inputs[0].strip('\n')
w = inputs[1].strip('\n')

def get_edit_distance(v, w):
    edit_distance = 0
    score_matrix = dict()
    score_matrix[(0, 0)] = 0
    for i in range(1, len(v) + 1):
        score_matrix[(i, 0)] = i
    for j in range(1, len(w) + 1):
        score_matrix[(0, j)] = j
    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            if v[i - 1] == w[j - 1]:
                score_matrix[(i, j)] = score_matrix[(i - 1, j - 1)]
            else:
                insertion_val = score_matrix[(i, j - 1)] + 1
                deletion_val = score_matrix[(i - 1, j)] + 1
                mismatch_val = score_matrix[(i - 1, j - 1)] + 1
                score_matrix[(i, j)] = min(insertion_val, deletion_val, mismatch_val)
    return score_matrix[(len(v), len(w))]
       
edit_distance = get_edit_distance(v, w)
print(edit_distance)