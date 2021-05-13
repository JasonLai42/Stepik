fd = open("dataset_317291_16.txt", "r")
inputs = fd.readlines()
f = inputs[1:]
nums = inputs[0].strip('\n').split(' ')
n = nums[0]
m = nums[1]

align_dict = dict()
def get_align_dict(text_arr):
    global align_dict
    for text in text_arr:
        text = text.strip('\n')
        ends = text.split('|')
        if ends[0][1:] in align_dict:
            align_dict[ends[0][1:]].append((ends[1][1:], (ends[0],ends[1])))
        else:
            align_dict[ends[0][1:]] = [(ends[1][1:], (ends[0],ends[1]))]
    
ordering_dict = dict()
start_read = ()
def align_read_pairs(text_arr):
    global align_dict
    global ordering_dict
    global start_read
    for text in text_arr:
        text = text.strip('\n')
        ends = text.split('|')
        if ends[0][:-1] in align_dict:
            match_not_found = True
            for index, right_end in enumerate(align_dict[ends[0][:-1]]):
                if ends[1][:-1] == right_end[0]:
                    ordering_dict[right_end[1]] = (ends[0],ends[1])
                    align_dict[ends[0][:-1]].pop(index)
                    if len(align_dict[ends[0][:-1]]) == 0:
                        del align_dict[ends[0][:-1]]
                    match_not_found = False
                    break
            if match_not_found:
                start_read = (ends[0],ends[1])
        else:
            start_read = (ends[0],ends[1])

left_ends = []
right_ends = []
def get_end_lists():
    global align_dict
    global ordering_dict
    global start_read
    global left_ends
    global right_ends
    current_pair = start_read
    while len(ordering_dict) > 0:
        left_ends.append(current_pair[0])
        right_ends.append(current_pair[1])
        temp_pair = current_pair
        current_pair = ordering_dict[current_pair]
        del ordering_dict[temp_pair]
    for k, v in align_dict.items():
        for pairs in v:
            left_ends.append(pairs[1][0])
            right_ends.append(pairs[1][1])

def get_composition(i, k):
    global left_ends
    global right_ends
    composition = left_ends[0]
    for end in left_ends[1:]:
        composition += end[i-1]
    for end in right_ends[len(right_ends)-k-1:-1]:
        composition += end[0]
    composition += right_ends[-1]
    return composition


get_align_dict(f)
align_read_pairs(f)
get_end_lists()
paired_comp = get_composition(int(n), int(m))
with open('output.txt', 'w') as filehandle:
    filehandle.write('%s\n' % paired_comp)