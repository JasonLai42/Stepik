import sys
sys.setrecursionlimit(1500)

f = open("dataset_317333_5.txt", "r")
inputs = f.readlines()
v = inputs[0].strip('\n')
w = inputs[1].strip('\n')

def LCSBackTrack(v, w):
    backtrack = dict()
    max_seq = dict()
    for i in range(0, len(v) + 1):
        max_seq[(i, 0)] = 0
    for j in range(0, len(w) + 1):
        max_seq[(0, j)] = 0
    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            match = 0
            if v[i - 1] == w[j - 1]:
                match = 1
            max_seq[(i, j)] = max(max_seq[(i - 1, j)], max_seq[(i, j - 1)], max_seq[(i - 1, j - 1)] + match)
            if max_seq[(i, j)] == max_seq[(i - 1, j)]:
                backtrack[(i, j)] = 'down'
            elif max_seq[(i, j)] == max_seq[(i, j - 1)]:
                backtrack[(i, j)] = 'right'
            elif max_seq[(i, j)] == max_seq[(i - 1, j - 1)] + match:
                backtrack[(i, j)] = 'diagonal'
    return backtrack
       
def outputLCS(backtrack, v, i, j):
    if i == 0 or j == 0:
        return ""
    
    if backtrack[(i, j)] == 'down':
        return outputLCS(backtrack, v, i - 1, j)
    elif backtrack[(i, j)] == 'right':
        return outputLCS(backtrack, v, i, j - 1)
    else:
        return outputLCS(backtrack, v, i - 1, j - 1) + v[i-1]

backtrack = LCSBackTrack(v, w)
LCS = outputLCS(backtrack, v, len(v), len(w))
print(LCS)