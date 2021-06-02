import math
f = open("dataset_317339_5.txt", "r")
inputs = f.readlines()
v = inputs[0].strip('\n')
w = inputs[1].strip('\n')
u = inputs[2].strip('\n')

def get_entropy_score(column):
    character_occurrences = dict()
    for character in column:
        if character == '-':
            continue
        if character_occurrences.get(character, "DNE") == "DNE":
            character_occurrences[character] = 1
        else:
            character_occurrences[character] += 1
    score = 0
    for key, value in character_occurrences.items():
        score += (value * math.log(value, 2))
    return score

def LCSBackTrack(v, w, u):
    backtrack = dict()
    max_seq = [[[0 for k in range(len(u)+1)] for j in range(len(w)+1)] for i in range(len(v)+1)]
    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            for k in range(1, len(u) + 1):
#                 max_seq[i][j][k] = max(max_seq[i-1][j][k] + get_entropy_score([v[i-1], '-', '-']),
#                                          max_seq[i][j-1][k] + get_entropy_score(['-', w[j-1], '-']),
#                                          max_seq[i][j][k-1] + get_entropy_score(['-', '-', u[k-1]]),
#                                          max_seq[i-1][j-1][k] + get_entropy_score([v[i-1], w[j-1], '-']),
#                                          max_seq[i-1][j][k-1] + get_entropy_score([v[i-1], '-', u[k-1]]),
#                                          max_seq[i][j-1][k-1] + get_entropy_score(['-', w[j-1], u[k-1]]),
#                                          max_seq[i-1][j-1][k-1] + get_entropy_score([v[i-1], w[j-1], u[k-1]]))
                match = 0
                if v[i - 1] == w[j - 1] == u[k - 1]:
                    match = 1
                scores = [max_seq[i-1][j][k],
                          max_seq[i][j-1][k],
                          max_seq[i][j][k-1],
                          max_seq[i-1][j-1][k],
                          max_seq[i-1][j][k-1],
                          max_seq[i][j-1][k-1],
                          max_seq[i-1][j-1][k-1] + match]
                max_seq[i][j][k] = max(scores)
                for index, value in enumerate(scores):
                    if max_seq[i][j][k] == value:
                        backtrack[(i, j, k)] = index + 1
                
    return backtrack, max_seq[len(v)][len(w)][len(u)]
       
def outputLCS(backtrack, v, i, j):
    if i == 0 or j == 0:
        return ""
    
    if backtrack[(i, j)] == 'down':
        return outputLCS(backtrack, v, i - 1, j)
    elif backtrack[(i, j)] == 'right':
        return outputLCS(backtrack, v, i, j - 1)
    else:
        return outputLCS(backtrack, v, i - 1, j - 1) + v[i-1]
    
def find_alignment(backtrack, v, w, u, i, j, k, new_v, new_w, new_u):
    if i == 0 and j == 0 and k == 0:
        return new_v, new_w, new_u
    else:
        if i == 0:
            if j == 0:
                return find_alignment(backtrack, v, w, u, i, j, k - 1, '-' + new_v, '-' + new_w, u[k-1] + new_u)
            elif k == 0:
                return find_alignment(backtrack, v, w, u, i, j - 1, k, '-' + new_v, w[j-1] + new_w, '-' + new_u)
            else:
                return find_alignment(backtrack, v, w, u, i, j - 1, k - 1, '-' + new_v, w[j-1] + new_w, u[k-1] + new_u)
        elif j == 0:
            if i == 0:
                return find_alignment(backtrack, v, w, u, i, j, k - 1, '-' + new_v, '-' + new_w, u[k-1] + new_u)
            elif k == 0:
                return find_alignment(backtrack, v, w, u, i - 1, j, k, v[i-1] + new_v, '-' + new_w, '-' + new_u)
            else:
                return find_alignment(backtrack, v, w, u, i - 1, j, k - 1, v[i-1] + new_v, '-' + new_w, u[k-1] + new_u)
        elif k == 0:
            if i == 0:
                return find_alignment(backtrack, v, w, u, i, j - 1, k, '-' + new_v, w[j-1] + new_w, '-' + new_u)
            elif j == 0:
                return find_alignment(backtrack, v, w, u, i - 1, j, k, v[i-1] + new_v, '-' + new_w, '-' + new_u)
            else:
                return find_alignment(backtrack, v, w, u, i, j, k - 1, v[i-1] + new_v, w[j-1] + new_w, '-' + new_u)
        else:
            if backtrack[(i, j, k)] == 1:
                return find_alignment(backtrack, v, w, u, i - 1, j, k, v[i-1] + new_v, '-' + new_w, '-' + new_u)
            elif backtrack[(i, j, k)] == 2:
                return find_alignment(backtrack, v, w, u, i, j - 1, k, '-' + new_v, w[j-1] + new_w, '-' + new_u)
            elif backtrack[(i, j, k)] == 3:
                return find_alignment(backtrack, v, w, u, i, j, k - 1, '-' + new_v, '-' + new_w, u[k-1] + new_u)
            elif backtrack[(i, j, k)] == 4:
                return find_alignment(backtrack, v, w, u, i - 1, j - 1, k, v[i-1] + new_v, w[j-1] + new_w, '-' + new_u)
            elif backtrack[(i, j, k)] == 5:
                return find_alignment(backtrack, v, w, u, i - 1, j, k - 1, v[i-1] + new_v, '-' + new_w, u[k-1] + new_u)
            elif backtrack[(i, j, k)] == 6:
                return find_alignment(backtrack, v, w, u, i, j - 1, k - 1, '-' + new_v, w[j-1] + new_w, u[k-1] + new_u)
            else:
                return find_alignment(backtrack, v, w, u, i - 1, j - 1, k - 1, v[i-1] + new_v, w[j-1] + new_w, u[k-1] + new_u)
    
backtrack, sink_score = LCSBackTrack(v, w, u)
aligned_v, aligned_w, aligned_u = find_alignment(backtrack, v, w, u, len(v), len(w), len(u), "", "", "")
output_list = [sink_score, aligned_v, aligned_w, aligned_u]
with open('output.txt', 'w') as filehandle:
    for listitem in output_list:
        filehandle.write('%s\n' % listitem)