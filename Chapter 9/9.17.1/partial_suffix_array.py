fd = open("dataset_317420_2.txt", "r")
inputs = fd.readlines()
f = inputs[0].strip('\n')
d = int(inputs[1].strip('\n'))

suffix_array = []
partial_array = []

def construct_array(text):
    global suffix_array
    for index, character in enumerate(text):
        suffix_array.append((text[index:], index))
        
def get_partial_array():
    global suffix_array
    global partial_array
    for index, pair in enumerate(suffix_array):
        if pair[1] % d == 0:
            partial_array.append(str(index) + "," + str(pair[1]))

construct_array(f[:-1])
suffix_array.append(('', len(f) - 1))
suffix_array = sorted(suffix_array, key=lambda x: x[0])
suffix_array = [(suffix[0] + '$', suffix[1]) for suffix in suffix_array]
get_partial_array()
with open('output.txt', 'w') as filehandle:
    for listitem in partial_array:
        filehandle.write('%s\n' % listitem)