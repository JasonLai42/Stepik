fd = open("dataset_317295_4.txt", "r")
inputs = fd.readlines()
f = inputs[1:]
nums = inputs[0].strip('\n').split(' ')
n = nums[0]
m = nums[1]

left_ends = []
right_ends = []
def get_end_lists(text_arr):
    global left_ends
    global right_ends
    for text in text_arr:
        text = text.strip('\n')
        ends = text.split('|')
        left_ends.append(ends[0])
        right_ends.append(ends[1])

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


get_end_lists(f)
paired_comp = get_composition(int(n), int(m))
with open('output.txt', 'w') as filehandle:
    filehandle.write('%s\n' % paired_comp)