import math
# f = open("patterns.txt", "r")
inputs = [
    'PLEASANTLY\n',
    'MEANLY'
]
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
indel_penalty = -5

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

BLOSUM62 = get_blosum_matrix(BLOSUM62_raw)

def get_middle_column_scores(v, w):
    global BLOSUM62
    global indel_penalty
    middle_column  = []
    last_edges = []
    
    score_matrix = dict()
    score_matrix[(0, 0)] = 0
    for i in range(1, len(v) + 1):
        score_matrix[(i, 0)] = score_matrix[(i - 1, 0)] + indel_penalty 
    for j in range(1, len(w) + 1):
        score_matrix[(0, j)] = score_matrix[(0, j - 1)] + indel_penalty 
        if j == len(w):
            middle_column.append(score_matrix[(0, j)])
            last_edges.append("right")
        
    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            insertion_val = score_matrix[(i, j - 1)] + indel_penalty
            deletion_val = score_matrix[(i - 1, j)] + indel_penalty
            match_val = score_matrix[(i - 1, j - 1)] + BLOSUM62[(v[i - 1], w[j - 1])]
            score_matrix[(i, j)] = max(insertion_val, deletion_val, match_val)
            if j == len(w):
                middle_column.append(score_matrix[(i, j)])
                if score_matrix[(i, j)] == insertion_val:
                    last_edges.append("right")
                elif score_matrix[(i, j)] == deletion_val:
                    last_edges.append("down")
                else:
                    last_edges.append("diagonal")

    return middle_column, last_edges

def get_middle_edge(v, w, top, bottom, left, right):
    # Middle column is the floor of half the size of w
    # In case of odd number divided by 2, we have to ensure that we are calculating the scores from the source and sink
    # for the SAME middle column hence the floor and ceil to find the middle column's index
    source_midpoint = math.floor((right + left) / 2)
    sink_midpoint = math.ceil((right + left) / 2)
    
    # Find the middle column scores from source
    source_middle, source_last_edge = get_middle_column_scores(v, w[:source_midpoint])
    
    # Find the middle column scores from sink
    sink_middle, sink_last_edge = get_middle_column_scores(v[::-1], w[::-1][:sink_midpoint])
    sink_middle.reverse()
    sink_last_edge.reverse()
    
    middle_node_vert = 0
    highest_score = -math.inf
    for index in range(0, len(source_middle)):
        if (source_middle[index] + sink_middle[index]) > highest_score:
            middle_node_vert = index
            highest_score = source_middle[index] + sink_middle[index]
    
    middle_node = (middle_node_vert, source_midpoint)
    
    middle_node_dest = ()
    if sink_last_edge[middle_node_vert] == "right":
        middle_node_dest = (middle_node[0], middle_node[1] + 1)
    elif sink_last_edge[middle_node_vert] == "down":
        middle_node_dest = (middle_node[0] + 1, middle_node[1])
    else: 
        middle_node_dest = (middle_node[0] + 1, middle_node[1] + 1)
        
    return middle_node, middle_node_dest

def linear_space_alignment(v, w, top, bottom, left, right):
    if left == right:
        print([v[top:bottom], '-'*(bottom - top)])
        return
    if top == bottom:
        print(['-'*(right - left), w[left:right]])
        return
    
    middle = math.floor((left + right) / 2)
    mid_edge_source, mid_edge_dest = get_middle_edge(v, w, top, bottom, left, right)
    mid_node_vert = mid_edge_source[0]
    
    linear_space_alignment(v, w, top, mid_node_vert, left, middle)
    print(mid_edge_dest)
    if mid_edge_source[1] + 1 == mid_edge_dest[1]:
        middle += 1
    if mid_edge_source[0] + 1 == mid_edge_dest[0]:
        mid_node_vert += 1 
    linear_space_alignment(v, w, mid_node_vert, bottom, middle, right)

linear_space_alignment(v, w, 0, len(v), 0, len(w))